# Physical-Digital Trust Mesh (PoC)

**Project:** Supply Chain Resilience via Physical Presence Lockout (PPL)  
**Grant Target:** DASA Open Call  
**Status:** TRL 4 (Feasibility Prototype)

## Overview
The Trust Mesh solves the problem of remote credential theft (phishing/keylogging) by tying digital access permissions to verifiable physical reality. This Python implementation creates an "Orchestration Layer" that continuously verifies three hardware signals:

1.  **Bluetooth Presence:** Proximity of a trusted beacon (e.g., user's watch/tag).
2.  **Wi-Fi Topology:** Verification of the specific RF environment (BSSID fingerprinting).
3.  **USB Hardware:** Presence of a physical security key (Air-gapped verification).

If the aggregated **Trust Score** drops below the threshold, the **DOOB (Digital Out Of Bounds)** protocol is triggered, severing network access immediately.

## Requirements
* **OS:** Linux (Developed on Linux Mint/Ubuntu)
* **Hardware:** Bluetooth Adapter, Wi-Fi Card.
* **Python Libraries:**
    ```bash
    pip install bleak
    ```

## Usage

1.  **Configuration:** * Update `src/bt_scanner.py` with your Beacon MAC address.
    * Update `src/wifi_topology_check.py` with your trusted Router BSSIDs.
    * Update `src/usb_presence.py` with your USB Vendor:Product ID.

2.  **Run the Orchestrator:**
    ```bash
    python3 src/orchestrator.py
    ```

## DASA Relevance
This codebase demonstrates the **Feasibility** of the PPL concept. It proves that low-cost, commodity hardware signals can be orchestrated to create a high-assurance security layer without requiring expensive new infrastructure.
