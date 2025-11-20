import asyncio
from bleak import BleakScanner

# --- CONFIGURATION ---
# [PROTECTED] REPLACE WITH YOUR BEACON MAC ADDRESS
# Example: "AA:BB:CC:DD:EE:FF"
TARGET_BEACON_ID = "00:00:00:00:00:00" 

# Signal strength threshold (dBm). Closer to 0 is stronger.
MIN_RSSI_THRESHOLD = -75  

async def check_bluetooth_presence(target_id: str = TARGET_BEACON_ID, min_rssi: int = MIN_RSSI_THRESHOLD) -> tuple[bool, int]:
    """
    Scans for a specific BLE device and checks if signal strength is strong enough.
    Returns: (Passed_Check: bool, RSSI_Value: int)
    """
    print(f"   [BT] Scanning for target beacon...")
    try:
        # Scan for 5 seconds
        devices = await BleakScanner.discover(timeout=5.0)
        
        for device in devices:
            # Normalize address to upper case for comparison
            if device.address.upper() == target_id.upper():
                rssi = device.rssi
                # print(f"   [BT] Device Found. RSSI: {rssi} dBm") # Debug line
                
                if rssi >= min_rssi:
                    return True, rssi
                else:
                    return False, rssi
        
        return False, -999
        
    except Exception as e:
        print(f"   [BT] Error: {e}")
        return False, -999

# Quick Test
if __name__ == "__main__":
    print("Running Standalone Test...")
    res, val = asyncio.run(check_bluetooth_presence())
    print(f"Result: {res} (Signal: {val})")
