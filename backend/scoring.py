"""
WMCDA Scoring Engine — Real Network Edition
=============================================
Scores real WiFi networks using:
  - Actual signal strength (from netsh)
  - Measured throughput (from psutil byte counters)
  - Measured latency (from ICMP ping)
  - Calculated reliability (packet loss %)
  - Security level (from authentication type)
  - Cost efficiency (free WiFi = high, metered = low)

Formula:
    CNS = Σ(wi × Ni) / Σ(wi)

    Where Ni are normalized metrics [0, 1] and wi are profile-specific weights.
"""

from config import NORMALIZATION, SECURITY_LEVELS, WEIGHT_PROFILES, DEFAULT_WEIGHTS
from typing import List, Optional


def normalize(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """
    Min-max normalize a value to [0, 1].
    If invert=True, lower raw values score higher (for latency).
    """
    if max_val == min_val:
        return 0.5
    clamped = max(min_val, min(value, max_val))
    n = (clamped - min_val) / (max_val - min_val)
    return round(1.0 - n if invert else n, 4)


def compute_network_score(network: dict, weights: dict, latency_ms: float = 50,
                          throughput_mbps: float = 0, packet_loss: float = 0) -> dict:
    """
    Score a single network using WMCDA.
    
    Args:
        network: dict from scanner with ssid, signal_percent, authentication, etc.
        weights: dict of metric weights (from profile)
        latency_ms: measured average latency
        throughput_mbps: measured throughput
        packet_loss: measured packet loss percentage
    
    Returns:
        dict with normalized metrics, component scores, and composite score
    """
    bounds = NORMALIZATION
    
    # 1. Normalize each metric
    signal_norm = normalize(
        network.get("signal_percent", 0),
        bounds["signal_strength"]["min"],
        bounds["signal_strength"]["max"],
    )
    
    # Use the max of measured throughput and the link rate for bandwidth
    link_rate = network.get("receive_rate_mbps", 0) or 0
    effective_bandwidth = max(throughput_mbps, 0)
    # If we have a link rate from the connected network, use it as fallback
    if effective_bandwidth < 1 and link_rate > 0:
        effective_bandwidth = link_rate * 0.6  # Typical real throughput is ~60% of link rate
    # For non-connected networks, estimate from signal and radio type
    if effective_bandwidth < 1:
        effective_bandwidth = _estimate_bandwidth(network)
    
    bandwidth_norm = normalize(
        effective_bandwidth,
        bounds["bandwidth"]["min"],
        bounds["bandwidth"]["max"],
    )
    
    latency_norm = normalize(
        latency_ms,
        bounds["latency"]["min"],
        bounds["latency"]["max"],
        invert=True,  # Lower latency = better
    )
    
    # Reliability from packet loss (100% delivery = perfect)
    reliability = 100.0 - packet_loss
    reliability_norm = normalize(
        reliability,
        bounds["reliability"]["min"],
        bounds["reliability"]["max"],
    )
    
    # Security level from authentication type
    auth = network.get("authentication", "Open")
    security_level = SECURITY_LEVELS.get(auth, 1)
    security_norm = normalize(
        security_level,
        bounds["security"]["min"],
        bounds["security"]["max"],
    )
    
    # Cost efficiency: WiFi is generally free (1.0), unless it's a hotspot
    cost_eff = 1.0 if network.get("is_known", False) else 0.7
    cost_norm = normalize(
        cost_eff,
        bounds["cost_efficiency"]["min"],
        bounds["cost_efficiency"]["max"],
    )
    
    normalized = {
        "signal_strength": signal_norm,
        "bandwidth": bandwidth_norm,
        "latency": latency_norm,
        "reliability": reliability_norm,
        "security": security_norm,
        "cost_efficiency": cost_norm,
    }
    
    # 2. Weighted scoring
    component_scores = {}
    for metric, norm_val in normalized.items():
        w = weights.get(metric, 0)
        component_scores[metric] = round(w * norm_val, 4)
    
    total_weight = sum(weights.values())
    composite = sum(component_scores.values()) / total_weight if total_weight > 0 else 0
    composite = round(composite, 4)
    
    # 3. Generate recommendation
    recommendation = _get_recommendation(composite, network["ssid"])
    
    return {
        "ssid": network.get("ssid", ""),
        "bssid": network.get("bssid", ""),
        "signal_percent": network.get("signal_percent", 0),
        "radio_type": network.get("radio_type", ""),
        "generation": network.get("generation", ""),
        "band": network.get("band", ""),
        "channel": network.get("channel", 0),
        "authentication": auth,
        "encryption": network.get("encryption", ""),
        "is_known": network.get("is_known", False),
        "is_current": network.get("is_current", False),
        "effective_bandwidth_mbps": round(effective_bandwidth, 2),
        "latency_ms": round(latency_ms, 1),
        "packet_loss_percent": round(packet_loss, 1),
        "reliability_percent": round(reliability, 1),
        "security_level": security_level,
        "normalized_metrics": normalized,
        "component_scores": component_scores,
        "composite_score": composite,
        "recommendation": recommendation,
    }


def score_all_networks(
    networks: List[dict],
    profile: str = "balanced",
    latency_ms: float = 50,
    throughput_mbps: float = 0,
    packet_loss: float = 0,
) -> List[dict]:
    """
    Score and rank all visible networks.
    
    Note: Latency/throughput/packet_loss are measured for the CURRENT connection.
    Non-connected networks get estimated values based on signal strength.
    """
    weights = WEIGHT_PROFILES.get(profile, DEFAULT_WEIGHTS)
    scored = []
    
    for net in networks:
        if not net.get("ssid"):
            continue
        
        # Use real measurements for the currently connected network
        if net.get("is_current"):
            net_latency = latency_ms
            net_throughput = throughput_mbps
            net_loss = packet_loss
        else:
            # Estimate for non-connected networks
            net_latency = _estimate_latency(net)
            net_throughput = 0  # Can't measure without connecting
            net_loss = _estimate_packet_loss(net)
        
        score = compute_network_score(
            net, weights, net_latency, net_throughput, net_loss
        )
        scored.append(score)
    
    # Sort by composite score (highest first)
    scored.sort(key=lambda x: x["composite_score"], reverse=True)
    
    # Assign ranks
    for i, s in enumerate(scored):
        s["rank"] = i + 1
    
    return scored


def get_formula_explanation(profile: str = "balanced") -> str:
    """Return human-readable formula for the given profile."""
    weights = WEIGHT_PROFILES.get(profile, DEFAULT_WEIGHTS)
    parts = []
    for metric, w in weights.items():
        label = metric.replace("_", " ").title()
        parts.append(f"({w:.2f} × {label})")
    
    formula_str = " + ".join(parts)
    total = sum(weights.values())
    
    return (
        f"Composite Network Score (CNS) = [{formula_str}] / {total:.2f}\n\n"
        f"Profile: {profile}\n"
        f"All metrics normalized to [0, 1] where 1 = best.\n"
        f"Latency is inverted (lower ms = higher score).\n"
        f"Data source: Real-time Windows netsh + psutil measurements."
    )


# ============================================================================
# ESTIMATION HELPERS (for non-connected networks)
# ============================================================================

def _estimate_bandwidth(network: dict) -> float:
    """Estimate potential bandwidth from signal strength and radio type."""
    signal = network.get("signal_percent", 0)
    radio = network.get("radio_type", "")
    
    # Max theoretical speeds by radio type
    max_speeds = {
        "802.11b": 11,
        "802.11a": 54,
        "802.11g": 54,
        "802.11n": 300,
        "802.11ac": 1300,
        "802.11ax": 2400,
        "802.11be": 5000,
    }
    
    max_speed = max_speeds.get(radio, 100)
    # Real throughput is roughly signal_% × max_speed × 0.4
    estimated = (signal / 100) * max_speed * 0.4
    return max(1, estimated)


def _estimate_latency(network: dict) -> float:
    """Estimate latency from signal strength (weaker signal = higher latency)."""
    signal = network.get("signal_percent", 0)
    if signal >= 80:
        return 15
    elif signal >= 60:
        return 30
    elif signal >= 40:
        return 60
    elif signal >= 20:
        return 120
    else:
        return 250


def _estimate_packet_loss(network: dict) -> float:
    """Estimate packet loss from signal strength."""
    signal = network.get("signal_percent", 0)
    if signal >= 70:
        return 0
    elif signal >= 50:
        return 2
    elif signal >= 30:
        return 8
    elif signal >= 15:
        return 20
    else:
        return 40


def _get_recommendation(score: float, ssid: str) -> str:
    """Generate human-readable recommendation."""
    if score >= 0.85:
        return f"🟢 Excellent — {ssid} delivers top-tier performance."
    elif score >= 0.70:
        return f"🔵 Good — {ssid} provides reliable connectivity."
    elif score >= 0.55:
        return f"🟡 Adequate — {ssid} works for basic tasks."
    elif score >= 0.40:
        return f"🟠 Weak — {ssid} may experience lag or drops."
    else:
        return f"🔴 Poor — {ssid} is unreliable. Avoid if possible."
