"""
PRISM-Edge: Covert Safety, Duress Beacon & Data Protection Subsystem
Designed for women safety, gender-based violence prevention, and rural emergency response.
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple

class EmergencyBeaconEngine:
    """
    Handles duress-aware covert SOS signals, silent panic triggers,
    and automatic tamper-wiping of sensitive personal logs.
    """
    def __init__(self, normal_pin: str = "1234", duress_pin: str = "9999"):
        self.normal_pin_hash: str = hashlib.sha256(normal_pin.encode()).hexdigest()
        self.duress_pin_hash: str = hashlib.sha256(duress_pin.encode()).hexdigest()
        self.emergency_contacts: List[Dict[str, str]] = []
        self.active_sos_events: List[Dict[str, Any]] = []

    def register_emergency_contact(self, name: str, phone: str, relation: str) -> None:
        self.emergency_contacts.append({
            "name": name,
            "phone": phone,
            "relation": relation
        })

    def process_pin_entry(self, entered_pin: str, current_gps: Tuple[float, float] = (23.8103, 90.4125)) -> Dict[str, Any]:
        pin_hash = hashlib.sha256(entered_pin.encode()).hexdigest()

        if pin_hash == self.duress_pin_hash:
            # DURESS ACTIVATION: App appears to unlock normal empty screen, but silently broadcasts SOS
            sos_payload = self.trigger_silent_sos(
                trigger_source="COVERT_DURESS_PIN",
                gps_coords=current_gps,
                metadata="Silent coercion alert triggered by operator."
            )
            return {
                "auth_status": "SUCCESS_NORMAL_VIEW",
                "covert_alert_dispatched": True,
                "sos_id": sos_payload["sos_id"]
            }
        elif pin_hash == self.normal_pin_hash:
            return {
                "auth_status": "SUCCESS_NORMAL_VIEW",
                "covert_alert_dispatched": False,
                "sos_id": None
            }
        else:
            return {
                "auth_status": "AUTH_FAILED",
                "covert_alert_dispatched": False,
                "sos_id": None
            }

    def trigger_silent_sos(self, trigger_source: str, gps_coords: Tuple[float, float], metadata: str = "") -> Dict[str, Any]:
        sos_id = f"SOS-{int(time.time()*1000):X}"
        sos_event = {
            "sos_id": sos_id,
            "timestamp": time.time(),
            "trigger_source": trigger_source,
            "gps_latitude": gps_coords[0],
            "gps_longitude": gps_coords[1],
            "metadata": metadata,
            "status": "DISPATCHED_TO_MESH_AND_AUTHORITIES",
            "notified_responders": len(self.emergency_contacts)
        }
        self.active_sos_events.append(sos_event)
        return sos_event
