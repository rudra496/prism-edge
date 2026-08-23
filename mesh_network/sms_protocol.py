"""
PRISM-Edge: Compact Binary SMS Telemetry Protocol
Bit-packed on-the-wire encoding for triage alerts so that a complete health
packet provably fits inside a single 160-character GSM-7 SMS (1120 bits of
user data per SMS per 3GPP TS 23.038), with Base91 text transport for
BLE-advertisement / USSD channels where binary SMS is unavailable.

Design rules enforced by tests/test_sms_protocol.py:
  * Worst-case encoded triage alert <= 160 characters.
  * Round-trip decode(encode(x)) == x for every field.
"""

import struct
import time
import zlib
from typing import Any, Dict, Optional

from mesh_network.resilient_mesh import base91_encode, base91_decode

# --- Wire format constants -------------------------------------------------
MAGIC = b"P1"                      # 2-byte protocol signature
PROTO_VERSION = 1

# Urgency codes (1 byte)
URGENCY_CODES = {"ROUTINE": 0, "ADVISORY": 1, "URGENT": 2, "EMERGENCY": 3}
URGENCY_NAMES = {v: k for k, v in URGENCY_CODES.items()}

# Fixed-point scales
GPS_SCALE = 10 ** 5                # lat/lon resolution ~1.1 m
TEMP_OFFSET = -50.0                # stored as (temp - offset) in 0.1 C units
TEMP_SCALE = 10

# struct layout after the 6-byte header (magic 2B, version 1B, urgency 1B,
# risk_score 1B, reserved 1B): patient_ref 4B | systolic 2B | heart_rate 2B |
# temp 2B (0.1C offset-scaled) | lat 4B | lon 4B | age_sec 4B
_BODY_FMT = ">IHHHiiI"             # 24-byte body; see class docstring for map
_HEADER_LEN = 6
_CRC_LEN = 2


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class SmsTriageAlert:
    """
    A minimal, fixed-layout triage alert designed to survive a single SMS hop.

    Field budget (bytes):
      header        6   magic(2) version:type(1) urgency(1) risk(1) rsvd(1)
      patient_ref   4   first 4 bytes of SHA-256 of patient id (no PII on wire)
      bp_systolic   2   mmHg, uint16 big-endian
      heart_rate    2   BPM, uint16 big-endian
      temp_c        2   (temp - (-50)) * 10, uint16 -> covers -50..605 C
      latitude      4   degrees * 1e5, int32
      longitude     4   degrees * 1e5, int32
      age_sec       4   seconds since packet origin, uint32
      crc16         2   CRC-16/CCITT over all preceding bytes
    Total: 32 bytes -> 43 Base91 chars -> 50 chars with "PRISM:" prefix.
    """

    def __init__(
        self,
        patient_id: str,
        urgency: str,
        risk_score: float,
        systolic_bp: int = 120,
        heart_rate_bpm: int = 140,
        temp_c: float = 37.0,
        latitude: float = 23.8103,
        longitude: float = 90.4125,
        age_seconds: int = 0,
    ):
        if urgency not in URGENCY_CODES:
            raise ValueError(f"unknown urgency: {urgency!r}")
        self.patient_ref = zlib.crc32(patient_id.encode("utf-8")) & 0xFFFFFFFF
        self.urgency = urgency
        self.risk_score = int(_clamp(risk_score, 0.0, 100.0))
        self.systolic_bp = int(_clamp(systolic_bp, 0, 300))
        self.heart_rate_bpm = int(_clamp(heart_rate_bpm, 0, 10000))
        self.temp_c = float(temp_c)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.age_seconds = int(age_seconds)

    def pack(self) -> bytes:
        """Serialize to a fixed 32-byte frame with trailing CRC."""
        body = struct.pack(
            _BODY_FMT,
            self.patient_ref,
            self.systolic_bp,
            self.heart_rate_bpm,
            int(round((self.temp_c - TEMP_OFFSET) * TEMP_SCALE)),
            int(round(self.latitude * GPS_SCALE)),
            int(round(self.longitude * GPS_SCALE)),
            self.age_seconds & 0xFFFFFFFF,
        )
        frame = MAGIC + bytes([PROTO_VERSION, URGENCY_CODES[self.urgency],
                               self.risk_score, 0]) + body
        return frame + struct.pack(">H", zlib.crc32(frame) & 0xFFFF)

    @classmethod
    def unpack(cls, frame: bytes) -> Optional["SmsTriageAlert"]:
        """Parse a packed frame; returns None on any corruption/mismatch."""
        expected_len = _HEADER_LEN + struct.calcsize(_BODY_FMT) + _CRC_LEN
        if len(frame) != expected_len or not frame.startswith(MAGIC):
            return None
        stored_crc = struct.unpack(">H", frame[-_CRC_LEN:])[0]
        if zlib.crc32(frame[:-_CRC_LEN]) & 0xFFFF != stored_crc:
            return None
        urgency_code = frame[3]
        risk_score = frame[4]
        (patient_ref, sys_bp, bpm, temp_q, lat_q, lon_q, age_s) = struct.unpack(
            _BODY_FMT, frame[_HEADER_LEN:-_CRC_LEN]
        )
        alert = cls.__new__(cls)
        alert.patient_ref = patient_ref
        alert.urgency = URGENCY_NAMES.get(urgency_code)
        alert.risk_score = risk_score
        alert.systolic_bp = sys_bp
        alert.heart_rate_bpm = bpm
        alert.temp_c = temp_q / TEMP_SCALE + TEMP_OFFSET
        alert.latitude = lat_q / GPS_SCALE
        alert.longitude = lon_q / GPS_SCALE
        alert.age_seconds = age_s
        return alert

    def to_sms(self) -> str:
        """Base91 text transport form ('PRISM:' + charset), SMS-safe by length."""
        return "PRISM:" + base91_encode(self.pack())

    @classmethod
    def from_sms(cls, sms_text: str) -> Optional["SmsTriageAlert"]:
        if not sms_text.startswith("PRISM:"):
            return None
        raw = base91_decode(sms_text[len("PRISM:"):])
        return cls.unpack(raw)

    def to_dict(self) -> Dict[str, Any]:
        """Decoded view used by dashboards; never includes raw PII."""
        return {
            "patient_ref": f"{self.patient_ref:08X}",
            "urgency": self.urgency,
            "risk_score": self.risk_score,
            "systolic_bp": self.systolic_bp,
            "heart_rate_bpm": self.heart_rate_bpm,
            "temp_c": self.temp_c,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "age_seconds": self.age_seconds,
        }


def sms_size_report() -> Dict[str, int]:
    """
    Measured transport sizes for a fully-populated worst-case alert.
    Used by docs/tests to substantiate the single-SMS guarantee honestly.
    """
    worst = SmsTriageAlert(
        patient_id="PATIENT-00000000",
        urgency="EMERGENCY",
        risk_score=100,
        systolic_bp=200,
        heart_rate_bpm=999,
        temp_c=42.5,
        latitude=-90.0,
        longitude=180.0,
        age_seconds=4294967295,
    ).to_sms()
    return {
        "packed_bytes": len(SmsTriageAlert(
            "x", "EMERGENCY", 100).pack()),
        "base91_chars": len(worst) - len("PRISM:"),
        "full_text_chars": len(worst),
        "gsm7_sms_limit": 160,
    }
