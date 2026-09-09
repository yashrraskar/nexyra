#!/usr/bin/env python3
"""
MAHASync - The Digital Bridge (SIH 2026)
Master Local Demo Runner

Starts all independent departmental services and the MahaSync interoperability gateway:
- Port 8000: Revenue Department API & Visual Portal
- Port 8001: Agriculture Department API & Visual Portal
- Port 8082: MahaSync Core Interoperability Gateway & Citizen Portal
"""

import sys
import os
import time
import subprocess
import signal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

processes = []

def cleanup(signum=None, frame=None):
    print("\n[MahaSync] Stopping all microservices...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=2)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass
    print("[MahaSync] All services stopped cleanly.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    os.chdir(BASE_DIR)
    python_exe = sys.executable

    print("=" * 70)
    print("      MAHASync – The Digital Bridge (SIH 2026 Prototype)      ")
    print("  'One Citizen • One Profile • One Platform • Connected Gov'  ")
    print("=" * 70)
    print("\n[1/3] Starting Revenue Department System (Port 8000)...")
    p_rev = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "goverment_systems.revenue.main:app", "--host", "127.0.0.1", "--port", "8000", "--log-level", "warning"],
        cwd=str(BASE_DIR)
    )
    processes.append(p_rev)

    print("[2/3] Starting Agriculture Department System (Port 8001)...")
    p_agri = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "goverment_systems.agriculture.main:app", "--host", "127.0.0.1", "--port", "8001", "--log-level", "warning"],
        cwd=str(BASE_DIR)
    )
    processes.append(p_agri)

    print("[3/3] Starting MahaSync Interoperability Core & Citizen Portal (Port 8082)...")
    p_core = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8082", "--log-level", "info"],
        cwd=str(BASE_DIR)
    )
    processes.append(p_core)

    time.sleep(2)
    print("\n" + "=" * 70)
    print("                  ALL SERVICES ACTIVE AND READY!              ")
    print("=" * 70)
    print("  🌐 Citizen Portal:       http://127.0.0.1:8082/portal")
    print("  🏛️ Revenue Dept Portal:  http://127.0.0.1:8000/revenue/portal")
    print("  🌾 Agriculture Portal:   http://127.0.0.1:8001/agriculture/portal")
    print("  📚 Swagger API Docs:     http://127.0.0.1:8082/docs")
    print("=" * 70)
    print("  Demo Flow:")
    print("  1. Open http://127.0.0.1:8082/portal in your browser.")
    print("  2. Review Rahul's dashboard and the active Agriculture Subsidy application.")
    print("  3. Click 'Allow & Verify Automatically' on the DPDP Consent card.")
    print("  4. Watch real-time multi-department verification in the Tracking tab.")
    print("  5. Inspect Revenue and Agriculture portals to observe independent states.")
    print("=" * 70)
    print("Press Ctrl+C to terminate all services.\n")

    try:
        while True:
            time.sleep(1)
            # Check if any process died unexpectedly
            for p in processes:
                if p.poll() is not None:
                    print(f"[MahaSync] Warning: A subprocess exited with code {p.returncode}")
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
