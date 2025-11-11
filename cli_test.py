#!/usr/bin/env python3
"""
SecureOS Flash - Command Line Interface (Test Version)

Simple CLI to test the framework with Samsung backend.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core import ProtocolManager
from backends.samsung import SamsungBackend


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    print("=" * 60)
    print("SecureOS Flash - Universal Android Flash Tool")
    print("🏴‍☠️ For Everyone. Free Forever.")
    print("=" * 60)
    print()
    
    # Initialize protocol manager
    manager = ProtocolManager()
    
    # Register Samsung backend (Heimdall)
    samsung = SamsungBackend()
    manager.register_backend(samsung)
    
    print("🔍 Detecting device...")
    print()
    
    # Detect device
    device = manager.detect_device()
    
    if not device:
        print("❌ No compatible device detected")
        print()
        print("Make sure:")
        print("  • Device is connected via USB")
        print("  • Device is in Download Mode (Samsung)")
        print("  • Heimdall is installed on your system")
        print()
        return 1
    
    print(f"✅ Device detected!")
    print(f"   Manufacturer: {device.manufacturer}")
    print(f"   Model: {device.model}")
    print(f"   USB VID: {device.usb_vendor_id}")
    print()
    
    # Initialize session
    print("🔌 Initializing session...")
    if not manager.init_session():
        print("❌ Failed to initialize session")
        return 1
    
    print("✅ Session initialized")
    print()
    
    # Get partition list
    print("📋 Available partitions:")
    partitions = manager.get_partition_list()
    for partition in partitions:
        print(f"   • {partition}")
    print()
    
    # Example: Backup bootloader
    print("💾 Testing backup functionality...")
    backup_file = "/tmp/secureos-test-backup.img"
    print(f"   Backing up BOOTLOADER to {backup_file}")
    
    # Note: This is just a test - actual backup may fail if no BOOTLOADER partition
    # That's okay, we're testing the framework
    result = manager.backup_partition("BOOTLOADER", backup_file)
    
    if result.success:
        print(f"✅ Backup successful: {result.message}")
    else:
        print(f"⚠️  Backup test: {result.message}")
        if result.error:
            print(f"   Error: {result.error}")
    print()
    
    # End session
    print("🔚 Ending session...")
    manager.end_session(reboot=False)
    print("✅ Session ended")
    print()
    
    print("=" * 60)
    print("Framework test complete!")
    print("Next steps:")
    print("  • Build GUI")
    print("  • Add fastboot backend")
    print("  • Add backup/restore UI")
    print("  • Add setup guides")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
