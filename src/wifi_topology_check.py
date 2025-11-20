import subprocess
import re

# --- CONFIGURATION ---
# [PROTECTED] LIST OF TRUSTED BSSIDS (MAC ADDRESSES) FOR YOUR ROUTERS
# Run 'sudo iw dev wlan0 scan' to find yours.
KNOWN_BSSID_LIST = [
    "AA:BB:CC:DD:EE:FF", 
    "11:22:33:44:55:66"
]  
MINIMUM_MATCHES = 1 

def check_wifi_topology(known_bssids: list = KNOWN_BSSID_LIST) -> tuple[bool, list]:
    """
    Scans visible Wi-Fi networks to ensure the device is in a known location
    by fingerprinting the BSSIDs (Hardware MACs) of nearby routers.
    """
    print("   [WiFi] Scanning environment topology...")
    
    # Command to scan for Access Points using standard Linux 'iw' tool
    command = ["/usr/sbin/iw", "dev", "wlan0", "scan", "ap"] 
    found_bssids = []
    
    try:
        # Execute scan
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print(f"   [WiFi] Warning: 'iw' command failed. Ensure permissions.")
            return False, []

        # Regex to find BSSIDs in the output
        bssid_regex = re.compile(r'BSS\s+([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})')
        all_detected_bssids = bssid_regex.findall(result.stdout)
        
        # Normalize and Compare
        normalized_known = [b.replace(':', '').upper() for b in known_bssids]
        
        for detected in all_detected_bssids:
            clean_detected = detected.replace(':', '').upper()
            if clean_detected in normalized_known:
                if detected not in found_bssids:
                    found_bssids.append(detected)
        
        success = len(found_bssids) >= MINIMUM_MATCHES
        return success, found_bssids

    except Exception as e:
        print(f"   [WiFi] Error during scan: {e}")
        return False, []

if __name__ == "__main__":
    print("Running Standalone Test...")
    res, networks = check_wifi_topology()
    print(f"Result: {res}")
