import asyncio
import time
from datetime import datetime

# Local Module Imports
import bt_scanner
import wifi_topology_check
import usb_presence

# --- TRUST POLICY CONFIGURATION ---
REQUIRED_SCORE = 3  # High Security Mode: All 3 signals required
POLL_INTERVAL = 10  # Seconds between checks

def doob_protocol_lockdown(reason):
    """
    DIGITAL OUT OF BOUNDS (DOOB) PROTOCOL
    Triggers immediate network isolation.
    """
    timestamp = datetime.now().isoformat()
    print("\n" + "!"*60)
    print("🚨🚨 SECURITY ALERT: PHYSICAL PRESENCE VERIFICATION FAILED 🚨🚨")
    print(f"TIMESTAMP: {timestamp}")
    print(f"REASON: {reason}")
    print("ACTION: DIGITAL OUT-OF-BOUNDS (DOOB) TRIGGERED")
    print("STATUS: Network Isolated (Simulated)")
    print("!"*60 + "\n")
    # In TRL 6 Prototype: os.system("nmcli networking off") 

async def run_trust_mesh():
    print("\n=== Physical-Digital Trust Mesh (PPL) Engine ===")
    print(f"Target Score: {REQUIRED_SCORE}/3")
    print("Initializing Sensors...\n")

    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] --- Starting Trust Cycle ---")
        
        # 1. USB Check (Fast hardware poll)
        usb_safe = usb_presence.check_usb_presence()
        print(f"   > USB Check: {'PASS' if usb_safe else 'FAIL'}")
        
        # 2. WiFi Topology (RF Fingerprint)
        wifi_safe, _ = wifi_topology_check.check_wifi_topology()
        print(f"   > WiFi Check: {'PASS' if wifi_safe else 'FAIL'}")
        
        # 3. Bluetooth (Async scan)
        bt_safe, bt_rssi = await bt_scanner.check_bluetooth_presence()
        print(f"   > BT Check:  {'PASS' if bt_safe else 'FAIL'} (RSSI: {bt_rssi})")

        # Calculate Aggregate Score
        score = 0
        failures = []
        
        if usb_safe: score += 1
        else: failures.append("USB_MISSING")
            
        if wifi_safe: score += 1
        else: failures.append("BAD_WIFI_TOPOLOGY")
            
        if bt_safe: score += 1
        else: failures.append("BT_BEACON_ABSENT")

        # Enforce Policy
        if score < REQUIRED_SCORE:
            doob_protocol_lockdown(f"Trust Score {score}/{REQUIRED_SCORE} | Failures: {failures}")
        else:
            print(f"✅ TRUST VERIFIED (Score {score}). Session Active.\n")

        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(run_trust_mesh())
    except KeyboardInterrupt:
        print("\nSystem Halting.")
