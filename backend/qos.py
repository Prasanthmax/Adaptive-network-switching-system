"""
QoS Traffic Routing — Windows DSCP Policy Manager
====================================================
Applies Differentiated Services Code Point (DSCP) values using
Windows PowerShell 'New-NetQosPolicy' / 'Remove-NetQosPolicy'.

Each usage profile maps to a specific DSCP marking:
  - Gaming     → DSCP 46 (Expedited Forwarding — lowest latency)
  - Streaming  → DSCP 34 (Assured Forwarding 41 — high throughput)
  - Enterprise → DSCP 26 (Assured Forwarding 31 — reliable delivery)
  - IoT        → DSCP 10 (Assured Forwarding 11 — background traffic)
  - Balanced   → DSCP 0  (Best Effort — no special treatment)
  - Cost Sens. → DSCP 0  (Best Effort)
"""

import subprocess
import sys
from typing import Optional

# Windows-only flag to hide console windows during subprocess calls
_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

# DSCP values mapped to each usage profile
PROFILE_DSCP = {
    "gaming":         46,   # EF  — Expedited Forwarding
    "streaming":      34,   # AF41 — Assured Forwarding (high throughput)
    "enterprise":     26,   # AF31 — Assured Forwarding (reliable)
    "iot":            10,   # AF11 — Background / low priority
    "balanced":        0,   # BE  — Best Effort
    "cost_sensitive":  0,   # BE  — Best Effort
}

POLICY_NAME = "AdaptiveNetSwitch_QoS"


def _run_powershell(command: str) -> dict:
    """Run a PowerShell command silently and return result."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            creationflags=_NO_WINDOW,
        )
        return {
            "success": result.returncode == 0,
            "stdout": (result.stdout or "").strip(),
            "stderr": (result.stderr or "").strip(),
        }
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e)}


def apply_qos_policy(profile: str) -> dict:
    """
    Apply a Windows QoS policy matching the given usage profile.

    Steps:
      1. Remove any existing policy with our name.
      2. If the profile has a non-zero DSCP, create a new policy.
    """
    dscp = PROFILE_DSCP.get(profile, 0)

    # Step 1 — Remove old policy (ignore errors if it doesn't exist)
    remove_cmd = f'Remove-NetQosPolicy -Name "{POLICY_NAME}" -Confirm:$false -ErrorAction SilentlyContinue'
    _run_powershell(remove_cmd)

    # Step 2 — Apply new policy only if DSCP > 0
    if dscp > 0:
        create_cmd = (
            f'New-NetQosPolicy -Name "{POLICY_NAME}" '
            f'-DSCPAction {dscp} '
            f'-NetworkProfile All '
            f'-Default '
            f'-ErrorAction Stop'
        )
        result = _run_powershell(create_cmd)
        return {
            "applied": result["success"],
            "profile": profile,
            "dscp": dscp,
            "policy_name": POLICY_NAME,
            "message": result["stdout"] if result["success"] else result["stderr"],
        }

    return {
        "applied": True,
        "profile": profile,
        "dscp": 0,
        "policy_name": POLICY_NAME,
        "message": "Best Effort — no QoS policy needed.",
    }


def remove_qos_policy() -> dict:
    """Remove the adaptive network QoS policy."""
    remove_cmd = f'Remove-NetQosPolicy -Name "{POLICY_NAME}" -Confirm:$false -ErrorAction SilentlyContinue'
    result = _run_powershell(remove_cmd)
    return {
        "removed": True,
        "message": result["stdout"] or "Policy removed (or did not exist).",
    }


def get_current_qos() -> dict:
    """Query the current QoS policies on this machine."""
    result = _run_powershell(
        f'Get-NetQosPolicy -Name "{POLICY_NAME}" -ErrorAction SilentlyContinue | '
        f'Select-Object Name, DSCPAction, NetworkProfile | Format-List'
    )
    if result["success"] and result["stdout"]:
        return {"exists": True, "details": result["stdout"]}
    return {"exists": False, "details": "No adaptive QoS policy active."}
