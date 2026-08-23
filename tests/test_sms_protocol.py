"""
PRISM-Edge: SMS Protocol Guarantee Tests
Proves the compact binary triage alert fits inside ONE GSM-7 SMS segment
and survives corruption / round-trip intact.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mesh_network.sms_protocol import SmsTriageAlert, sms_size_report


class TestSmsProtocol(unittest.TestCase):

    def test_worst_case_fits_single_sms(self):
        report = sms_size_report()
        self.assertLessEqual(report["full_text_chars"], report["gsm7_sms_limit"])
        self.assertLessEqual(report["packed_bytes"], 140)  # 140-octet SMS user-data field
        print(f"[SMS PASS] packed={report['packed_bytes']}B "
              f"text={report['full_text_chars']}/160 chars")

    def test_roundtrip_all_fields(self):
        alert = SmsTriageAlert(
            patient_id="P-77120",
            urgency="EMERGENCY",
            risk_score=87,
            systolic_bp=165,
            heart_rate_bpm=48,
            temp_c=38.6,
            latitude=22.7041,
            longitude=90.3717,
            age_seconds=3600,
        )
        decoded = SmsTriageAlert.from_sms(alert.to_sms())
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded.patient_ref, alert.patient_ref)
        self.assertEqual(decoded.urgency, "EMERGENCY")
        self.assertEqual(decoded.risk_score, 87)
        self.assertEqual(decoded.systolic_bp, 165)
        self.assertEqual(decoded.heart_rate_bpm, 48)
        self.assertAlmostEqual(decoded.temp_c, 38.6, places=1)
        self.assertAlmostEqual(decoded.latitude, 22.7041, places=4)
        self.assertAlmostEqual(decoded.longitude, 90.3717, places=4)
        self.assertEqual(decoded.age_seconds, 3600)

    def test_corruption_rejected(self):
        frame = SmsTriageAlert("X", "URGENT", 55).pack()
        corrupted = bytearray(frame)
        corrupted[8] ^= 0xFF
        self.assertIsNone(SmsTriageAlert.unpack(bytes(corrupted)))
        self.assertIsNone(SmsTriageAlert.unpack(frame[:-1]))
        self.assertIsNone(SmsTriageAlert.unpack(b"GARBAGE"))

    def test_no_pii_on_wire(self):
        """The wire format must never carry the raw patient identifier."""
        sms = SmsTriageAlert("ASHA-BRAC-MOTHER-4471", "ROUTINE", 12).to_sms()
        self.assertNotIn("ASHA", sms)
        self.assertNotIn("4471", sms)


if __name__ == "__main__":
    unittest.main()
