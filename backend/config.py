"""
Configuration for the Adaptive Network Switching System.
Real-time network intelligence for Windows systems.
"""

# =============================================================================
# WMCDA Weights — Normalized scoring criteria
# =============================================================================
DEFAULT_WEIGHTS = {
    "signal_strength": 0.25,
    "bandwidth": 0.20,
    "latency": 0.20,
    "reliability": 0.15,
    "security": 0.10,
    "cost_efficiency": 0.10,
}

WEIGHT_PROFILES = {
    "balanced": {
        "signal_strength": 0.25,
        "bandwidth": 0.20,
        "latency": 0.20,
        "reliability": 0.15,
        "security": 0.10,
        "cost_efficiency": 0.10,
    },
    "streaming": {
        "signal_strength": 0.15,
        "bandwidth": 0.35,
        "latency": 0.20,
        "reliability": 0.15,
        "security": 0.05,
        "cost_efficiency": 0.10,
    },
    "gaming": {
        "signal_strength": 0.15,
        "bandwidth": 0.15,
        "latency": 0.35,
        "reliability": 0.20,
        "security": 0.05,
        "cost_efficiency": 0.10,
    },
    "enterprise": {
        "signal_strength": 0.10,
        "bandwidth": 0.15,
        "latency": 0.15,
        "reliability": 0.25,
        "security": 0.25,
        "cost_efficiency": 0.10,
    },
    "cost_sensitive": {
        "signal_strength": 0.15,
        "bandwidth": 0.15,
        "latency": 0.15,
        "reliability": 0.10,
        "security": 0.05,
        "cost_efficiency": 0.40,
    },
    "iot": {
        "signal_strength": 0.20,
        "bandwidth": 0.10,
        "latency": 0.15,
        "reliability": 0.30,
        "security": 0.15,
        "cost_efficiency": 0.10,
    },
}

# =============================================================================
# Normalization Ranges (for mapping raw → [0, 1])
# =============================================================================
NORMALIZATION = {
    "signal_strength": {"min": 0, "max": 100},         # Percentage (0–100%)
    "bandwidth": {"min": 0, "max": 1000},               # Mbps (measured throughput)
    "latency": {"min": 1, "max": 500},                   # ms (lower is better → inverted)
    "reliability": {"min": 0, "max": 100},                # % (packet delivery ratio)
    "security": {"min": 0, "max": 4},                     # Security level 0–4
    "cost_efficiency": {"min": 0, "max": 1},              # 0–1 (free=1, metered=0.5, etc.)
}

# Security level mapping from authentication type
SECURITY_LEVELS = {
    "Open": 0,
    "WEP": 1,
    "WPA-Personal": 2,
    "WPA2-Personal": 3,
    "WPA3-Personal": 4,
    "WPA2-Enterprise": 3,
    "WPA3-Enterprise": 4,
}

# Radio type → generation label
RADIO_GENERATIONS = {
    "802.11b": "WiFi 1",
    "802.11a": "WiFi 2",
    "802.11g": "WiFi 3",
    "802.11n": "WiFi 4",
    "802.11ac": "WiFi 5",
    "802.11ax": "WiFi 6",
    "802.11be": "WiFi 7",
}

# =============================================================================
# Auto-Switch Configuration
# =============================================================================
AUTO_SWITCH = {
    "enabled": True,
    "scan_interval_seconds": 10,         # How often to re-scan
    "quality_threshold": 0.30,           # Switch if current score drops below this
    "hysteresis_margin": 0.08,           # Candidate must beat current by this much
    "min_switch_interval_seconds": 30,   # Prevent flapping
    "only_known_networks": True,         # Only auto-switch to saved profiles
    "latency_test_host": "8.8.8.8",     # Default ping target
    "latency_test_count": 4,            # Number of pings
    "bandwidth_sample_duration": 2,      # Seconds to sample throughput
}

# =============================================================================
# Server
# =============================================================================
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
DATABASE_PATH = "network_history.db"
