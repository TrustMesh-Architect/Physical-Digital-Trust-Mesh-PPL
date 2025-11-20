import subprocess

# --- CONFIGURATION ---
# [PROTECTED] REPLACE WITH YOUR USB DEVICE ID
# Run 'lsusb' to find yours. Format is VENDOR:PRODUCT
TARGET_USB_ID = "1234:5678" 

def check_usb_presence(target_id: str = TARGET_USB_ID) -> bool:
    """
    Checks if a specific USB device is physically plugged in via lsusb.
    This acts as a physical 'ignition key' for the session.
    """
    print(f"   [USB] Verifying Security Key...")
    command = ["lsusb"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=5)
        
        if target_id in result.stdout:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"   [USB] Error: {e}")
        return False

if __name__ == "__main__":
    print("Running Standalone Test...")
    print(f"Result: {check_usb_presence()}")
