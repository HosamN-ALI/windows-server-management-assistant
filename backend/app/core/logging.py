import sys
from pathlib import Path
from loguru import logger
from app.core.config import get_settings

def setup_logging():
    """Configure logging for the application"""
    settings = get_settings()
    
    # Remove default logger
    logger.remove()
    
    # Add console logging
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # Add file logging
    log_file = Path(settings.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Add audit logging for security events
    audit_log_file = log_file.parent / "audit.log"
    logger.add(
        audit_log_file,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | AUDIT | {message}",
        filter=lambda record: "AUDIT" in record["extra"],
        rotation="10 MB",
        retention="90 days"
    )
    
    logger.info("Logging system initialized")

def get_audit_logger():
    """Get logger for audit events"""
    return logger.bind(AUDIT=True)

def log_command_execution(user: str, command: str, success: bool, output: str = ""):
    """Log command execution for audit purposes"""
    audit_logger = get_audit_logger()
    status = "SUCCESS" if success else "FAILED"
    audit_logger.info(f"USER:{user} | COMMAND:{command} | STATUS:{status} | OUTPUT:{output[:200]}")

def log_security_event(event_type: str, user: str, details: str):
    """Log security-related events"""
    audit_logger = get_audit_logger()
    audit_logger.warning(f"SECURITY_EVENT:{event_type} | USER:{user} | DETAILS:{details}")

def log_pentest_activity(user: str, tool: str, target: str, action: str):
    """Log penetration testing activities"""
    audit_logger = get_audit_logger()
    audit_logger.info(f"PENTEST | USER:{user} | TOOL:{tool} | TARGET:{target} | ACTION:{action}")
