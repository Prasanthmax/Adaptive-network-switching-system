"""
Pydantic models for the real-network Adaptive Network Switching System.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum


class UsageProfile(str, Enum):
    BALANCED = "balanced"
    STREAMING = "streaming"
    GAMING = "gaming"
    ENTERPRISE = "enterprise"
    COST_SENSITIVE = "cost_sensitive"
    IOT = "iot"


class ScanRequest(BaseModel):
    profile: UsageProfile = UsageProfile.BALANCED


class SwitchRequest(BaseModel):
    ssid: str = Field(..., description="SSID of the network to switch to")


class AutoSwitchConfig(BaseModel):
    enabled: bool = True
    quality_threshold: float = Field(0.30, ge=0, le=1)
    hysteresis_margin: float = Field(0.08, ge=0, le=0.5)
    scan_interval_seconds: int = Field(10, ge=5, le=120)


class MonitorControl(BaseModel):
    action: str = Field(..., description="start, stop, or configure")
    profile: Optional[str] = None
    auto_switch: Optional[AutoSwitchConfig] = None
