#!/usr/bin/env python3
"""
SecureOS Flash - GUI Application

User-friendly interface for flashing bootloaders and ROMs.
Built for everyone - grandma to power user.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import threading
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core import ProtocolManager, DeviceInfo
from backends.samsung import SamsungBackend


class SecureOSFlashGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureOS Flash - Universal Android Flash Tool 🏴‍☠️")
        self.root.geometry("800x600")
        
        # Protocol manager
        self.manager = ProtocolManager()
        self.manager.register_backend(SamsungBackend())
        
        self.device_info = None
        
        # Build UI
        self.create_ui()
        
        # Auto-detect on start
        self.detect_device()
    
    def create_ui(self):
        """Build the main UI"""
        
        # Header
        header = tk.Frame(self.root, bg="#2d2d2d", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="SecureOS Flash 🏴‍☠️",
            font=("Arial", 24, "bold"),
            bg="#2d2d2d",
            fg="#00ff00"
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            header,
            text="One tool. Any device. Any ROM. Free forever.",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#888888"
        )
        subtitle.pack()
        
        # Main content area
        content = tk.Frame(self.root, bg="#1a1a1a")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Device detection area
        self.device_frame = tk.LabelFrame(
            content,
            text="Device Status",
            font=("Arial", 12, "bold"),
            bg="#1a1a1a",
            fg="#ffffff",
            padx=10,
            pady=10
        )
        self.device_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.device_status = tk.Label(
            self.device_frame,
            text="🔍 Detecting device...",
            font=("Arial", 11),
            bg="#1a1a1a",
            fg="#ffaa00",
            anchor=tk.W
        )
        self.device_status.pack(fill=tk.X)
        
        self.device_details = tk.Label(
            self.device_frame,
            text="",
            font=("Arial", 9),
            bg="#1a1a1a",
            fg="#888888",
            anchor=tk.W,
            justify=tk.LEFT
        )
        self.device_details.pack(fill=tk.X)
        
        detect_btn = tk.Button(
            self.device_frame,
            text="🔄 Refresh Device",
            command=self.detect_device,
            bg="#444444",
            fg="#ffffff",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        detect_btn.pack(pady=(10, 0))
        
        # Actions area
        actions_frame = tk.LabelFrame(
            content,
            text="Actions",
            font=("Arial", 12, "bold"),
            bg="#1a1a1a",
            fg="#ffffff",
            padx=10,
            pady=10
        )
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Flash bootloader button
        flash_frame = tk.Frame(actions_frame, bg="#1a1a1a")
        flash_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            flash_frame,
            text="⚡ Flash Bootloader:",
            font=("Arial", 11, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        ).pack(side=tk.LEFT)
        
        self.flash_btn = tk.Button(
            flash_frame,
            text="Select Bootloader & Flash",
            command=self.flash_bootloader,
            bg="#00aa00",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.flash_btn.pack(side=tk.RIGHT)
        
        # Backup button
        backup_frame = tk.Frame(actions_frame, bg="#1a1a1a")
        backup_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            backup_frame,
            text="💾 Backup Device:",
            font=("Arial", 11, "bold"),
            bg="#1a1a1a",
            fg="#0088ff"
        ).pack(side=tk.LEFT)
        
        self.backup_btn = tk.Button(
            backup_frame,
            text="Create Safety Backup",
            command=self.backup_device,
            bg="#0066cc",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.backup_btn.pack(side=tk.RIGHT)
        
        # Help button
        help_frame = tk.Frame(actions_frame, bg="#1a1a1a")
        help_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            help_frame,
            text="📚 Need Help?",
            font=("Arial", 11, "bold"),
            bg="#1a1a1a",
            fg="#ffaa00"
        ).pack(side=tk.LEFT)
        
        help_btn = tk.Button(
            help_frame,
            text="Setup Guide",
            command=self.show_setup_guide,
            bg="#ff8800",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        help_btn.pack(side=tk.RIGHT)
        
        # Progress area
        self.progress_frame = tk.Frame(content, bg="#1a1a1a")
        self.progress_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 9),
            bg="#1a1a1a",
            fg="#888888"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate'
        )
        
        # Footer
        footer = tk.Frame(self.root, bg="#2d2d2d", height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            footer,
            text="Built with ❤️ by Barrer Software | Privacy First • Security as a Right | Open Source Forever",
            font=("Arial", 8),
            bg="#2d2d2d",
            fg="#666666"
        ).pack(pady=10)
    
    def detect_device(self):
        """Detect connected device"""
        self.device_status.config(text="🔍 Detecting device...", fg="#ffaa00")
        self.device_details.config(text="")
        self.flash_btn.config(state=tk.DISABLED)
        self.backup_btn.config(state=tk.DISABLED)
        
        def detect():
            device = self.manager.detect_device()
            
            if device:
                self.device_info = device
                self.root.after(0, self.on_device_detected, device)
            else:
                self.device_info = None
                self.root.after(0, self.on_device_not_found)
        
        threading.Thread(target=detect, daemon=True).start()
    
    def on_device_detected(self, device: DeviceInfo):
        """Device was detected"""
        self.device_status.config(
            text=f"✅ Device detected: {device.manufacturer} {device.model}",
            fg="#00ff00"
        )
        
        details = f"ID: {device.device_id}\n"
        details += f"USB: {device.usb_vendor_id}:{device.usb_product_id}\n"
        details += f"Bootloader: {'Locked' if device.bootloader_locked else 'Unlocked'}"
        
        self.device_details.config(text=details)
        
        # Enable buttons
        self.flash_btn.config(state=tk.NORMAL)
        self.backup_btn.config(state=tk.NORMAL)
        
        # Initialize session
        self.manager.init_session()
    
    def on_device_not_found(self):
        """No device detected"""
        self.device_status.config(
            text="❌ No compatible device detected",
            fg="#ff4444"
        )
        
        details = "Make sure:\n"
        details += "• Device is connected via USB\n"
        details += "• Device is in Download Mode (Samsung)\n"
        details += "• USB debugging is enabled\n"
        details += "• Heimdall is installed"
        
        self.device_details.config(text=details)
    
    def flash_bootloader(self):
        """Flash bootloader to device"""
        if not self.device_info:
            messagebox.showerror("Error", "No device connected!")
            return
        
        # Ask for confirmation
        result = messagebox.askyesno(
            "Flash Bootloader",
            "⚠️ WARNING ⚠️\n\n"
            "Flashing a bootloader can:\n"
            "• Void your warranty\n"
            "• Brick your device if done incorrectly\n"
            "• Erase all data\n\n"
            "A safety backup will be created first.\n\n"
            "Continue?"
        )
        
        if not result:
            return
        
        # Select bootloader file
        filename = filedialog.askopenfilename(
            title="Select Bootloader Image",
            filetypes=[
                ("Image files", "*.img *.bin"),
                ("All files", "*.*")
            ]
        )
        
        if not filename:
            return
        
        # Flash in background thread
        self.show_progress("Creating safety backup...")
        
        def flash():
            # This will auto-backup first
            result = self.manager.flash_bootloader(filename, auto_backup=True)
            self.root.after(0, self.on_flash_complete, result)
        
        threading.Thread(target=flash, daemon=True).start()
    
    def backup_device(self):
        """Backup device partitions"""
        if not self.device_info:
            messagebox.showerror("Error", "No device connected!")
            return
        
        # Select backup location
        filename = filedialog.asksaveasfilename(
            title="Save Backup As",
            defaultextension=".img",
            filetypes=[("Image files", "*.img"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        self.show_progress("Backing up device...")
        
        def backup():
            result = self.manager.backup_partition("BOOTLOADER", filename)
            self.root.after(0, self.on_backup_complete, result)
        
        threading.Thread(target=backup, daemon=True).start()
    
    def show_setup_guide(self):
        """Show setup guide window"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Setup Guide")
        guide_window.geometry("600x500")
        guide_window.configure(bg="#1a1a1a")
        
        # Header
        tk.Label(
            guide_window,
            text="📚 How to Prepare Your Device",
            font=("Arial", 16, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        ).pack(pady=20)
        
        # Instructions
        text = tk.Text(
            guide_window,
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Arial", 10),
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        guide_text = """
For Samsung Devices (Download Mode):

1. Enable Developer Options
   • Go to Settings → About Phone
   • Tap "Build Number" 7 times
   • You'll see "You are now a developer!"

2. Enable USB Debugging
   • Go to Settings → Developer Options
   • Toggle "USB Debugging" ON

3. Enable OEM Unlocking
   • In Developer Options
   • Toggle "OEM Unlocking" ON
   • (May be grayed out on carrier-locked devices)

4. Enter Download Mode
   • Power off device completely
   • Press and hold: Volume UP + Volume DOWN
   • While holding, plug in USB cable
   • Press Volume UP to confirm
   • Screen should show "Downloading..."

5. Connect to Computer
   • Device should be detected automatically
   • Click "Refresh Device" if needed

⚠️ Important Notes:
• Flashing voids warranty
• Always backup your data first
• Ensure battery is charged (>50%)
• Use a good quality USB cable
• Don't disconnect during flash

Need more help? Visit:
https://github.com/barrersoftware/secureos-flash
        """
        
        text.insert("1.0", guide_text)
        text.config(state=tk.DISABLED)
        
        tk.Button(
            guide_window,
            text="Got it!",
            command=guide_window.destroy,
            bg="#00aa00",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            padx=30,
            pady=10
        ).pack(pady=(0, 20))
    
    def show_progress(self, message):
        """Show progress indicator"""
        self.progress_label.config(text=message)
        self.progress_bar.pack(fill=tk.X, pady=10)
        self.progress_bar.start()
    
    def hide_progress(self):
        """Hide progress indicator"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
    
    def on_flash_complete(self, result):
        """Flash operation completed"""
        self.hide_progress()
        
        if result.success:
            messagebox.showinfo(
                "Success!",
                f"✅ {result.message}\n\n"
                "Device will reboot automatically."
            )
        else:
            messagebox.showerror(
                "Flash Failed",
                f"❌ {result.message}\n\n"
                f"Error: {result.error or 'Unknown error'}"
            )
    
    def on_backup_complete(self, result):
        """Backup operation completed"""
        self.hide_progress()
        
        if result.success:
            messagebox.showinfo("Success!", f"✅ {result.message}")
        else:
            messagebox.showerror(
                "Backup Failed",
                f"❌ {result.message}\n\n"
                f"Error: {result.error or 'Unknown error'}"
            )


def main():
    root = tk.Tk()
    app = SecureOSFlashGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
