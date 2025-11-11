"""
SecureOS Flash - Samsung Backend

Implements flash operations for Samsung devices using Heimdall protocol.
Based on the open source Heimdall tool.
"""

import subprocess
import logging
import os
from typing import List, Optional

from ...core.flash_backend import FlashBackend, DeviceInfo, FlashResult


logger = logging.getLogger(__name__)


class SamsungBackend(FlashBackend):
    """
    Samsung device flash backend using Heimdall protocol (Odin 3).
    
    Supports Samsung Galaxy devices that use Download Mode.
    """
    
    # Samsung USB Vendor ID
    SAMSUNG_VID = "04e8"
    
    # Common Samsung Product IDs for Download Mode
    SAMSUNG_PIDS = [
        "6601",  # Galaxy S
        "685d",  # Galaxy S2
        "68c3",  # Droid Charge
        # Add more as discovered
    ]
    
    def __init__(self, heimdall_path: Optional[str] = None):
        """
        Initialize Samsung backend.
        
        Args:
            heimdall_path: Path to heimdall binary (None = use system PATH)
        """
        self.heimdall_path = heimdall_path or "heimdall"
        self.device_connected = False
        self.session_active = False
    
    def detect_device(self) -> Optional[DeviceInfo]:
        """
        Detect Samsung device in Download Mode.
        
        Returns:
            DeviceInfo if Samsung device found, None otherwise
        """
        try:
            # Use heimdall detect command
            result = subprocess.run(
                [self.heimdall_path, "detect"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and "Device detected" in result.stdout:
                logger.info("Samsung device detected via Heimdall")
                
                # TODO: Parse actual device info from heimdall output
                # For now, return generic info
                device_info = DeviceInfo(
                    manufacturer="Samsung",
                    model="Unknown Model",  # Parse from heimdall
                    device_id="samsung-download-mode",
                    usb_vendor_id=self.SAMSUNG_VID,
                    usb_product_id="unknown",
                    bootloader_locked=False,  # In download mode = unlocked
                    oem_unlock_enabled=True,
                    usb_debugging_enabled=True
                )
                
                self.device_connected = True
                return device_info
            
        except subprocess.TimeoutExpired:
            logger.warning("Heimdall detect timed out")
        except FileNotFoundError:
            logger.error(f"Heimdall binary not found: {self.heimdall_path}")
        except Exception as e:
            logger.error(f"Error detecting Samsung device: {e}")
        
        return None
    
    def init_session(self) -> bool:
        """
        Initialize Heimdall session with Samsung device.
        
        Returns:
            True if session started
        """
        if not self.device_connected:
            logger.error("No Samsung device connected")
            return False
        
        # Heimdall doesn't require explicit session init like some protocols
        # Session is implicit when device is in Download Mode
        logger.info("Samsung session ready (Download Mode)")
        self.session_active = True
        return True
    
    def backup_partition(self, partition_name: str, output_file: str) -> FlashResult:
        """
        Backup partition from Samsung device.
        
        Uses heimdall download command to read partition.
        
        Args:
            partition_name: Partition to backup
            output_file: Where to save backup
            
        Returns:
            FlashResult
        """
        if not self.session_active:
            return FlashResult(
                success=False,
                message="No active session",
                error="Call init_session() first"
            )
        
        try:
            # Heimdall download-pit for partition table
            # For actual partitions, use heimdall download --PARTITION
            cmd = [
                self.heimdall_path,
                "download",
                f"--{partition_name.upper()}",
                output_file
            ]
            
            logger.info(f"Backing up {partition_name} to {output_file}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for large partitions
            )
            
            if result.returncode == 0:
                return FlashResult(
                    success=True,
                    message=f"Backup of {partition_name} complete"
                )
            else:
                return FlashResult(
                    success=False,
                    message=f"Backup failed",
                    error=result.stderr
                )
                
        except Exception as e:
            return FlashResult(
                success=False,
                message="Backup failed",
                error=str(e)
            )
    
    def flash_partition(self, partition_name: str, image_file: str) -> FlashResult:
        """
        Flash partition on Samsung device.
        
        Uses heimdall flash command.
        
        Args:
            partition_name: Partition to flash
            image_file: Image file to flash
            
        Returns:
            FlashResult
        """
        if not self.session_active:
            return FlashResult(
                success=False,
                message="No active session",
                error="Call init_session() first"
            )
        
        if not os.path.exists(image_file):
            return FlashResult(
                success=False,
                message="Image file not found",
                error=f"File does not exist: {image_file}"
            )
        
        try:
            # Heimdall flash --PARTITION file.img
            cmd = [
                self.heimdall_path,
                "flash",
                f"--{partition_name.upper()}",
                image_file
            ]
            
            logger.info(f"Flashing {partition_name} with {image_file}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for large images
            )
            
            if result.returncode == 0:
                return FlashResult(
                    success=True,
                    message=f"Flash of {partition_name} complete"
                )
            else:
                return FlashResult(
                    success=False,
                    message=f"Flash failed",
                    error=result.stderr
                )
                
        except Exception as e:
            return FlashResult(
                success=False,
                message="Flash failed",
                error=str(e)
            )
    
    def flash_bootloader(self, bootloader_file: str) -> FlashResult:
        """
        Flash bootloader on Samsung device.
        
        Args:
            bootloader_file: Bootloader image
            
        Returns:
            FlashResult
        """
        # On Samsung, bootloader is typically the "BOOTLOADER" partition
        return self.flash_partition("BOOTLOADER", bootloader_file)
    
    def get_partition_list(self) -> List[str]:
        """
        Get list of partitions from Samsung device.
        
        Reads PIT (Partition Information Table) to get partition list.
        
        Returns:
            List of partition names
        """
        try:
            # Download PIT to temp file
            pit_file = "/tmp/secureos-samsung-pit.bin"
            
            result = subprocess.run(
                [self.heimdall_path, "download-pit", "--output", pit_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # TODO: Parse PIT file to extract partition names
                # For now, return common Samsung partitions
                return [
                    "BOOTLOADER",
                    "BOOT",
                    "RECOVERY",
                    "SYSTEM",
                    "USERDATA",
                    "CACHE"
                ]
            
        except Exception as e:
            logger.error(f"Error getting partition list: {e}")
        
        return []
    
    def end_session(self, reboot: bool = True) -> bool:
        """
        End session and optionally reboot device.
        
        Args:
            reboot: Whether to reboot device
            
        Returns:
            True if successful
        """
        if reboot:
            try:
                # Heimdall will auto-reboot after successful flash
                # No explicit reboot command needed
                logger.info("Device will reboot automatically")
            except Exception as e:
                logger.warning(f"Reboot command failed: {e}")
        
        self.session_active = False
        self.device_connected = False
        return True
    
    def get_backend_name(self) -> str:
        """Get backend name."""
        return "Samsung (Heimdall)"
    
    def supports_device(self, device_info: DeviceInfo) -> bool:
        """
        Check if this backend supports the device.
        
        Args:
            device_info: Device information
            
        Returns:
            True if Samsung device
        """
        return device_info.manufacturer.lower() == "samsung"
