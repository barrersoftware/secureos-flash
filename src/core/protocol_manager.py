"""
SecureOS Flash - Protocol Manager

Manages detection and selection of appropriate flash backend
based on connected device.
"""

from typing import List, Optional
import logging

from .flash_backend import FlashBackend, DeviceInfo, FlashResult


logger = logging.getLogger(__name__)


class ProtocolManager:
    """
    Central manager that detects devices and routes operations
    to the appropriate backend (Samsung, Fastboot, MediaTek, etc.)
    """
    
    def __init__(self):
        self.backends: List[FlashBackend] = []
        self.active_backend: Optional[FlashBackend] = None
        self.current_device: Optional[DeviceInfo] = None
    
    def register_backend(self, backend: FlashBackend):
        """
        Register a flash backend.
        
        Args:
            backend: FlashBackend implementation to register
        """
        self.backends.append(backend)
        logger.info(f"Registered backend: {backend.get_backend_name()}")
    
    def detect_device(self) -> Optional[DeviceInfo]:
        """
        Detect connected device by trying all registered backends.
        
        Returns:
            DeviceInfo if device detected, None otherwise
        """
        logger.info("Scanning for devices...")
        
        for backend in self.backends:
            logger.debug(f"Trying backend: {backend.get_backend_name()}")
            device_info = backend.detect_device()
            
            if device_info:
                logger.info(f"Device detected: {device_info.manufacturer} {device_info.model}")
                logger.info(f"Using backend: {backend.get_backend_name()}")
                
                self.active_backend = backend
                self.current_device = device_info
                return device_info
        
        logger.warning("No compatible device detected")
        return None
    
    def init_session(self) -> bool:
        """
        Initialize session with detected device.
        
        Returns:
            True if session initialized successfully
        """
        if not self.active_backend:
            logger.error("No active backend - detect device first")
            return False
        
        logger.info("Initializing session...")
        return self.active_backend.init_session()
    
    def backup_partition(self, partition_name: str, output_file: str) -> FlashResult:
        """
        Backup a partition using active backend.
        
        Args:
            partition_name: Partition to backup
            output_file: Where to save backup
            
        Returns:
            FlashResult
        """
        if not self.active_backend:
            return FlashResult(
                success=False,
                message="No device connected",
                error="Call detect_device() first"
            )
        
        logger.info(f"Backing up partition: {partition_name}")
        return self.active_backend.backup_partition(partition_name, output_file)
    
    def flash_partition(self, partition_name: str, image_file: str) -> FlashResult:
        """
        Flash a partition using active backend.
        
        Args:
            partition_name: Partition to flash
            image_file: Image to flash
            
        Returns:
            FlashResult
        """
        if not self.active_backend:
            return FlashResult(
                success=False,
                message="No device connected",
                error="Call detect_device() first"
            )
        
        logger.info(f"Flashing partition: {partition_name}")
        return self.active_backend.flash_partition(partition_name, image_file)
    
    def flash_bootloader(self, bootloader_file: str, auto_backup: bool = True) -> FlashResult:
        """
        Flash bootloader with optional automatic backup.
        
        Args:
            bootloader_file: Bootloader image to flash
            auto_backup: Create safety backup first (recommended)
            
        Returns:
            FlashResult
        """
        if not self.active_backend:
            return FlashResult(
                success=False,
                message="No device connected",
                error="Call detect_device() first"
            )
        
        # Automatic safety backup
        if auto_backup:
            logger.info("Creating safety backup before flashing...")
            backup_result = self.backup_partition(
                "bootloader",
                f"/tmp/secureos-backup-bootloader-{self.current_device.device_id}.img"
            )
            
            if not backup_result.success:
                logger.warning("Backup failed - proceeding anyway")
        
        logger.info("Flashing bootloader...")
        return self.active_backend.flash_bootloader(bootloader_file)
    
    def get_partition_list(self) -> List[str]:
        """
        Get list of partitions from active backend.
        
        Returns:
            List of partition names
        """
        if not self.active_backend:
            return []
        
        return self.active_backend.get_partition_list()
    
    def end_session(self, reboot: bool = True) -> bool:
        """
        End session with device.
        
        Args:
            reboot: Whether to reboot device
            
        Returns:
            True if successful
        """
        if not self.active_backend:
            return False
        
        logger.info("Ending session...")
        result = self.active_backend.end_session(reboot)
        
        if result:
            self.active_backend = None
            self.current_device = None
        
        return result
    
    def get_device_info(self) -> Optional[DeviceInfo]:
        """
        Get information about currently connected device.
        
        Returns:
            DeviceInfo or None
        """
        return self.current_device
