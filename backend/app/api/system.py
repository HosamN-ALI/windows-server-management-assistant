from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

from app.core.security import get_current_active_user
from app.services.system_service import SystemService
from app.dependencies import get_system_service
from app.core.config import get_settings

router = APIRouter(prefix="/system", tags=["system"])

class PowerShellRequest(BaseModel):
    script: str
    require_confirmation: bool = True

class SoftwareRequest(BaseModel):
    package_name: str
    manager: str = "chocolatey"

class ServiceRequest(BaseModel):
    service_name: str
    action: str

@router.get("/info")
async def get_system_info():
    """Get system information"""
    service = SystemService(get_settings())
    info = await service.get_system_info()
    return info

@router.post("/powershell")
async def execute_powershell(
    request: PowerShellRequest,
    current_user = Depends(get_current_active_user),
    system_service: SystemService = Depends(get_system_service)
):
    """Execute PowerShell script"""
    return await system_service.execute_powershell(
        request.script,
        current_user.username,
        request.require_confirmation
    )

@router.post("/software/install")
async def install_software(
    request: SoftwareRequest,
    current_user = Depends(get_current_active_user),
    system_service: SystemService = Depends(get_system_service)
):
    """Install software package"""
    return await system_service.install_software(
        request.package_name,
        request.manager,
        current_user.username
    )

@router.post("/software/uninstall")
async def uninstall_software(
    request: SoftwareRequest,
    current_user = Depends(get_current_active_user),
    system_service: SystemService = Depends(get_system_service)
):
    """Uninstall software package"""
    return await system_service.uninstall_software(
        request.package_name,
        request.manager,
        current_user.username
    )

@router.post("/service")
async def manage_service(
    request: ServiceRequest,
    current_user = Depends(get_current_active_user),
    system_service: SystemService = Depends(get_system_service)
):
    """Manage Windows service"""
    return await system_service.manage_service(
        request.service_name,
        request.action,
        current_user.username
    )

@router.get("/software/installed/{manager}")
async def get_installed_software(
    manager: str,
    current_user = Depends(get_current_active_user),
    system_service: SystemService = Depends(get_system_service)
):
    """Get list of installed software"""
    return await system_service.get_installed_software(manager)
