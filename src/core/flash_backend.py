"""
SecureOS Flash - Backend Abstraction Interface

This defines the interface that all flash backends must implement.
Each backend (Samsung, Fastboot, MediaTek) implements this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DeviceInfo:
    """Information about connected device"""
    manufacturer: str
    model: str
    device_id: str
    usb_vendor_id: str
    usb_product_id: str
    bootloader_locked: bool
    oem_unlock_enabled: bool
    usb_debugging_enabled: bool


@dataclass
class FlashResult:
    """Result of a flash operation"""
    success: bool
    message: str
    error: Optional[str] = None


class FlashBackend(ABC):
    """
    Abstract base class for all flash backends.
    
    Each manufacturer (Samsung, Google, MediaTek) implements this interface
    to provide flash capabilities using their specific protocols.
    """
    
    @abstractmethod
    def detect_device(self) -> Optional[DeviceInfo]:
        """
        Detect if a compatible device is connected.
        
        Returns:
            DeviceInfo if device detected, None otherwise
        """
        pass
    
    @abstractmethod
    def init_session(self) -> bool:
        """
        Initialize communication session with device.
        
        Returns:
            True if session started successfully
        """
        pass
    
    @abstractmethod
    def backup_partition(self, partition_name: str, output_file: str) -> FlashResult:
        """
        Backup a partition from device to file.
        
        Args:
            partition_name: Name of partition (e.g., 'boot', 'recovery', 'bootloader')
            output_file: Path to save backup file
            
        Returns:
            FlashResult with success status and message
        """
        pass
    
    @abstractmethod
    def flash_partition(self, partition_name: str, image_file: str) -> FlashResult:
        """
        Flash an image file to a partition.
        
        Args:
            partition_name: Name of partition to flash
            image_file: Path to image file
            
        Returns:
            FlashResult with success status and message
        """
        pass
    
    @abstractmethod
    def flash_bootloader(self, bootloader_file: str) -> FlashResult:
        """
        Flash a bootloader to device.
        
        Args:
            bootloader_file: Path to bootloader image
            
        Returns:
            FlashResult with success status and message
        """
        pass
    
    @abstractmethod
    def get_partition_list(self) -> List[str]:
        """
        Get list of available partitions on device.
        
        Returns:
            List of partition names
        """
        pass
    
    @abstractmethod
    def end_session(self, reboot: bool = True) -> bool:
        """
        End communication session with device.
        
        Args:
            reboot: Whether to reboot device after session
            
        Returns:
            True if session ended successfully
        """
        pass
    
    @abstractmethod
    def get_backend_name(self) -> str:
        """
        Get the name of this backend.
        
        Returns:
            Backend name (e.g., "Samsung", "Fastboot", "MediaTek")
        """
        pass
    
    @abstractmethod
    def supports_device(self, device_info: DeviceInfo) -> bool:
        """
        Check if this backend supports the given device.
        
        Args:
            device_info: Device information
            
        Returns:
            True if backend can handle this device
        """
        pass
