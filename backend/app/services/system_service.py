import asyncio
import json
import psutil
import platform
from typing import Dict, Any
from loguru import logger

from app.core.config import Settings
from app.core.logging import log_command_execution, log_security_event

class SystemService:
    """Windows system management service"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.powershell_path = "powershell.exe"
        self.chocolatey_path = settings.CHOCOLATEY_PATH
        self.winget_path = settings.WINGET_PATH
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            system_info = {
                'os': {
                    'name': platform.system(),
                    'version': platform.version(),
                    'release': platform.release(),
                    'architecture': platform.architecture()[0],
                    'machine': platform.machine(),
                    'processor': platform.processor()
                },
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'percent': psutil.virtual_memory().percent,
                    'used': psutil.virtual_memory().used
                },
                'disk': [],
                'cpu': {
                    'count': psutil.cpu_count(),
                    'percent': psutil.cpu_percent(interval=1),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'network': [],
                'processes': len(psutil.pids()),
                'boot_time': psutil.boot_time()
            }
            
            # Get disk information
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    system_info['disk'].append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': partition_usage.total,
                        'used': partition_usage.used,
                        'free': partition_usage.free,
                        'percent': (partition_usage.used / partition_usage.total) * 100
                    })
                except PermissionError:
                    continue
            
            # Get network interfaces
            for interface, addresses in psutil.net_if_addrs().items():
                interface_info = {'name': interface, 'addresses': []}
                for addr in addresses:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                system_info['network'].append(interface_info)
            
            return system_info
            
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            return {'error': str(e)}
    
    async def execute_powershell(self, script: str, user: str = "system", require_confirmation: bool = True) -> Dict[str, Any]:
        """Execute PowerShell script with security controls"""
        try:
            # Security check
            if require_confirmation and self.settings.REQUIRE_CONFIRMATION_FOR_PRIVILEGED:
                dangerous_keywords = [
                    'Remove-Item', 'Delete', 'Format-Volume', 'Clear-Host',
                    'Stop-Service', 'Disable-Service', 'Set-ExecutionPolicy',
                    'Invoke-Expression', 'Invoke-Command', 'New-Object',
                    'Registry', 'HKLM:', 'HKCU:'
                ]
                
                if any(keyword.lower() in script.lower() for keyword in dangerous_keywords):
                    log_security_event(
                        "DANGEROUS_POWERSHELL_BLOCKED",
                        user,
                        f"Script: {script[:100]}..."
                    )
                    return {
                        'success': False,
                        'error': 'Script contains potentially dangerous operations. Manual confirmation required.',
                        'requires_confirmation': True
                    }
            
            # Execute PowerShell script
            cmd = [
                self.powershell_path,
                '-ExecutionPolicy', self.settings.POWERSHELL_EXECUTION_POLICY,
                '-Command', script
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            success = process.returncode == 0
            output = stdout.decode('utf-8', errors='ignore') if stdout else ''
            error = stderr.decode('utf-8', errors='ignore') if stderr else ''
            
            # Log command execution
            log_command_execution(user, f"PowerShell: {script[:50]}...", success, output[:200])
            
            return {
                'success': success,
                'output': output,
                'error': error,
                'return_code': process.returncode
            }
            
        except Exception as e:
            logger.error(f"PowerShell execution error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def install_software(self, package_name: str, manager: str = "chocolatey", user: str = "system") -> Dict[str, Any]:
        """Install software using package managers"""
        try:
            if manager.lower() == "chocolatey":
                cmd = [self.chocolatey_path, "install", package_name, "-y"]
            elif manager.lower() == "winget":
                cmd = [self.winget_path, "install", package_name, "--accept-package-agreements", "--accept-source-agreements"]
            else:
                return {
                    'success': False,
                    'error': f'Unsupported package manager: {manager}'
                }
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            success = process.returncode == 0
            output = stdout.decode('utf-8', errors='ignore') if stdout else ''
            error = stderr.decode('utf-8', errors='ignore') if stderr else ''
            
            # Log installation
            log_command_execution(user, f"Install {package_name} via {manager}", success, output[:200])
            
            return {
                'success': success,
                'output': output,
                'error': error,
                'package': package_name,
                'manager': manager
            }
            
        except Exception as e:
            logger.error(f"Software installation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'package': package_name,
                'manager': manager
            }
    
    async def uninstall_software(self, package_name: str, manager: str = "chocolatey", user: str = "system") -> Dict[str, Any]:
        """Uninstall software using package managers"""
        try:
            if manager.lower() == "chocolatey":
                cmd = [self.chocolatey_path, "uninstall", package_name, "-y"]
            elif manager.lower() == "winget":
                cmd = [self.winget_path, "uninstall", package_name]
            else:
                return {
                    'success': False,
                    'error': f'Unsupported package manager: {manager}'
                }
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            success = process.returncode == 0
            output = stdout.decode('utf-8', errors='ignore') if stdout else ''
            error = stderr.decode('utf-8', errors='ignore') if stderr else ''
            
            # Log uninstallation
            log_command_execution(user, f"Uninstall {package_name} via {manager}", success, output[:200])
            
            return {
                'success': success,
                'output': output,
                'error': error,
                'package': package_name,
                'manager': manager
            }
            
        except Exception as e:
            logger.error(f"Software uninstallation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'package': package_name,
                'manager': manager
            }
    
    async def manage_service(self, service_name: str, action: str, user: str = "system") -> Dict[str, Any]:
        """Manage Windows services"""
        try:
            valid_actions = ['start', 'stop', 'restart', 'status']
            if action.lower() not in valid_actions:
                return {
                    'success': False,
                    'error': f'Invalid action. Valid actions: {", ".join(valid_actions)}'
                }
            
            if action.lower() == 'status':
                script = f"Get-Service -Name '{service_name}' | Select-Object Name, Status, StartType | ConvertTo-Json"
            elif action.lower() == 'start':
                script = f"Start-Service -Name '{service_name}'"
            elif action.lower() == 'stop':
                script = f"Stop-Service -Name '{service_name}'"
            elif action.lower() == 'restart':
                script = f"Restart-Service -Name '{service_name}'"
            
            result = await self.execute_powershell(script, user, require_confirmation=action != 'status')
            
            if result['success'] and action.lower() == 'status':
                try:
                    service_info = json.loads(result['output'])
                    result['service_info'] = service_info
                except json.JSONDecodeError:
                    pass
            
            return result
            
        except Exception as e:
            logger.error(f"Service management error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'service': service_name,
                'action': action
            }
    
    async def get_installed_software(self, manager: str = "chocolatey") -> Dict[str, Any]:
        """Get list of installed software"""
        try:
            if manager.lower() == "chocolatey":
                cmd = [self.chocolatey_path, "list", "--local-only"]
            elif manager.lower() == "winget":
                cmd = [self.winget_path, "list", "--accept-source-agreements"]
            else:
                return {
                    'success': False,
                    'error': f'Unsupported package manager: {manager}'
                }
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            success = process.returncode == 0
            output = stdout.decode('utf-8', errors='ignore') if stdout else ''
            error = stderr.decode('utf-8', errors='ignore') if stderr else ''
            
            # Parse output based on manager
            packages = []
            if success and output:
                if manager.lower() == "chocolatey":
                    lines = output.split('\n')
                    for line in lines:
                        if ' ' in line and not line.startswith('Chocolatey'):
                            parts = line.split(' ', 1)
                            if len(parts) >= 2:
                                packages.append({
                                    'name': parts[0],
                                    'version': parts[1].strip()
                                })
                elif manager.lower() == "winget":
                    # Parse winget output
                    lines = output.split('\n')
                    for line in lines[2:]:  # Skip header lines
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                packages.append({
                                    'name': parts[0],
                                    'version': parts[1] if len(parts) > 1 else 'Unknown'
                                })
            
            return {
                'success': success,
                'packages': packages,
                'output': output,
                'error': error,
                'manager': manager
            }
            
        except Exception as e:
            logger.error(f"Get installed software error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'manager': manager
            }
