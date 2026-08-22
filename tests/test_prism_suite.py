"""
PRISM-Edge: Comprehensive Unit & Integration Test Suite
Validates 100% compliance across all 7 competition tracks and architectural modules.
"""

import unittest
import numpy as np
import time
import sys
import os

# Add parent path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_engine.acoustic_biomarker import AcousticBiomarkerAnalyzer
from core_engine.clinical_triage import ClinicalTriageEngine
from core_engine.climate_analytics import ClimateResilienceEngine
from mesh_network.resilient_mesh import MeshPacket, ResilientMeshRouter, base91_encode, base91_decode
from privacy_security.crypto_vault import DifferentialPrivacyEngine, LocalCryptoVault, MerkleAuditTree
from privacy_security.sos_security import EmergencyBeaconEngine
from inclusion_upskill.skill_graph import BlindJobMatcher
from inclusion_upskill.voice_education import VoiceEduEngine

class TestPrismEdgeSuite(unittest.TestCase):

    def setUp(self):
        self.biomarker = AcousticBiomarkerAnalyzer(sample_rate=16000)
        self.clinical = ClinicalTriageEngine()
        self.climate = ClimateResilienceEngine()
        self.dp = DifferentialPrivacyEngine(epsilon=0.5)
        self.vault = LocalCryptoVault()
        self.merkle = MerkleAuditTree()
        self.beacon = EmergencyBeaconEngine()
        self.matcher = BlindJobMatcher()
        self.edu = VoiceEduEngine()

    def test_01_acoustic_biomarker_analysis(self):
        # Generate synthetic 1-second audio signal (16000 samples)
        t = np.linspace(0, 1.0, 16000, endpoint=False)
        # Sine wave with harmonics + slight modulation
        signal = 0.5 * np.sin(2 * np.pi * 220 * t) + 0.2 * np.sin(2 * np.pi * 440 * t)
        res = self.biomarker.analyze_audio_buffer(signal)

        self.assertIn("vitality_index", res)
        self.assertIn("dysphoria_risk_score", res)
        self.assertIn("clinical_status", res)
        self.assertGreaterEqual(res["vitality_index"], 0.0)
        self.assertLessEqual(res["vitality_index"], 100.0)
        self.assertIn("mean_f0_hz", res["features"])
        print(f"[TEST 1 PASS] Biomarker Analysis: Vitality={res['vitality_index']}, Status={res['clinical_status']}")

    def test_02_clinical_maternal_and_pediatric_triage(self):
        # Maternal emergency check
        patient_emergency = {
            "systolic_bp": 165,
            "diastolic_bp": 115,
            "gestational_weeks": 32,
            "symptoms": ["severe_headache", "blurred_vision"],
            "hemoglobin_g_dl": 10.5
        }
        res_mat = self.clinical.evaluate_maternal_risk(patient_emergency)
        self.assertEqual(res_mat["triage_urgency"], "EMERGENCY")
        self.assertGreater(res_mat["composite_risk_score"], 60.0)

        # Pediatric IMCI check
        child_sick = {
            "age_months": 8,
            "temperature_c": 39.4,
            "respiratory_rate_bpm": 55,
            "symptoms": ["chest_indrawing"],
            "muac_mm": 110
        }
        res_ped = self.clinical.evaluate_pediatric_imci(child_sick)
        self.assertIn(res_ped["triage_color"], ["RED", "YELLOW"])
        self.assertEqual(res_ped["muac_classification"], "Severe Malnutrition")
        print("[TEST 2 PASS] Clinical Decision Engine: IMCI & EmONC triages accurate.")

    def test_03_climate_and_crop_resilience(self):
        telemetry = {
            "temperature_c": 34.0,
            "humidity_pct": 85.0,
            "rainfall_3h_mm": 65.0,
            "soil_moisture_pct": 88.0
        }
        climate_res = self.climate.calculate_micro_climate_risk(telemetry)
        self.assertEqual(climate_res["urgency"], "EMERGENCY")
        self.assertIn("FLASH FLOOD", climate_res["status"])

        crop_res = self.climate.diagnose_crop_pathology("Rice", ["yellow_lesions_leaf_tip", "bacterial_ooze"])
        self.assertIn("Bacterial Leaf Blight", crop_res["pathology"])
        self.assertGreater(crop_res["carbon_impact_saved_kg"], 0.0)
        print(f"[TEST 3 PASS] Climate Engine: Alert={climate_res['status']}, Crop={crop_res['pathology']}")

    def test_04_mesh_networking_and_base91_compression(self):
        pkt = MeshPacket(
            sender_id="NODE-VILLAGE-01",
            recipient_id="NODE-CLINIC-HQ",
            payload_type="HEALTH_TRIAGE",
            payload_data={"patient_id": "P-9021", "urgency": "URGENT"}
        )
        sms_str = pkt.compress_for_sms()
        self.assertTrue(sms_str.startswith("PRISM:"))

        decompressed = MeshPacket.decompress_from_sms(sms_str)
        self.assertIsNotNone(decompressed)
        self.assertEqual(decompressed.sender_id, "NODE-VILLAGE-01")
        self.assertEqual(decompressed.payload_data["patient_id"], "P-9021")

        # Test Multi-hop Gossip
        router1 = ResilientMeshRouter("NODE-01")
        router2 = ResilientMeshRouter("NODE-02")
        router1.ingest_packet(pkt)
        synced = router1.gossip_sync_exchange(router2)
        self.assertEqual(synced, 1)
        self.assertIn(pkt.packet_id, router2.packet_buffer)
        print(f"[TEST 4 PASS] Mesh Network: Base91 compressed len={len(sms_str)}, Multi-hop Gossip Sync OK.")

    def test_05_privacy_vault_and_merkle_ledger(self):
        # Differential Privacy
        scores = [78.0, 82.0, 91.0, 65.0, 88.0, 95.0]
        dp_res = self.dp.anonymize_vitality_aggregate(scores)
        self.assertIn("noisy_mean", dp_res)
        self.assertIn("privacy_guarantee", dp_res)

        # Local Crypto Vault
        secret_data = "PATIENT_MEDICAL_RECORD_CONFIDENTIAL_12345"
        enc = self.vault.encrypt_record(secret_data)
        dec = self.vault.decrypt_record(enc)
        self.assertEqual(dec, secret_data)

        # Merkle Tree Root Calculation
        self.merkle.append_event("HEALTH_VISIT", "HASH_DATA_01")
        self.merkle.append_event("SKILL_MINT", "HASH_DATA_02")
        root = self.merkle.compute_root_hash()
        self.assertEqual(len(root), 64)
        print(f"[TEST 5 PASS] Privacy & Crypto: Encrypted Roundtrip OK, Merkle Root={root[:16]}...")

    def test_06_duress_sos_beacon(self):
        # Normal PIN entry
        res_norm = self.beacon.process_pin_entry("1234")
        self.assertEqual(res_norm["auth_status"], "SUCCESS_NORMAL_VIEW")
        self.assertFalse(res_norm["covert_alert_dispatched"])

        # Duress PIN entry
        res_duress = self.beacon.process_pin_entry("9999", current_gps=(23.8103, 90.4125))
        self.assertEqual(res_duress["auth_status"], "SUCCESS_NORMAL_VIEW") # Covert disguise
        self.assertTrue(res_duress["covert_alert_dispatched"])
        self.assertIsNotNone(res_duress["sos_id"])
        print("[TEST 6 PASS] Duress Beacon: Covert silent alert triggered successfully.")

    def test_07_inclusive_livelihood_and_voice_edu(self):
        # Job matching
        self.matcher.register_talent_profile("ARTISAN-01", ["embroidery", "textiles", "quality_audit"], {"craft": 95.0}, is_female_affirmative=True)
        self.matcher.post_job_opportunity("JOB-101", "Handmade Jute & Silk Textiles", ["embroidery", "textiles"], budget_bdt=4500.0, female_priority=True)
        matches = self.matcher.match_candidates_for_job("JOB-101")
        self.assertGreater(len(matches), 0)
        self.assertGreater(matches[0]["match_compatibility_pct"], 80.0)

        # Voice Education
        courses = self.edu.list_available_courses()
        self.assertGreater(len(courses), 0)
        quiz_res = self.edu.evaluate_quiz_submission("EDU-AGRI-101", [0, 0])
        self.assertTrue(quiz_res["passed"])
        self.assertIsNotNone(quiz_res["verified_certificate_token"])
        print(f"[TEST 7 PASS] Inclusion & Upskilling: Job Match Score={matches[0]['match_compatibility_pct']}%, Edu Cert={quiz_res['verified_certificate_token']}")

if __name__ == "__main__":
    unittest.main()
