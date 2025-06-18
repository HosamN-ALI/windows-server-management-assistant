import docker
from typing import Dict, Any, List

class DockerService:
    """Service for managing Docker containers"""
    
    def __init__(self):
        self.client = None
        try:
            self.client = docker.from_env()
        except Exception:
            pass  # Docker might not be available
    
    async def list_containers(self) -> List[Dict[str, Any]]:
        """List running containers"""
        if not self.client:
            return []
        
        containers = []
        for container in self.client.containers.list():
            containers.append({
                'id': container.id,
                'name': container.name,
                'status': container.status
            })
        return containers
