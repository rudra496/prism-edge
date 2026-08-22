"""
PRISM-Edge: Unified REST & Simulation API Server
Provides high-performance lightweight endpoints for all 7 competition pillars.
Operates standalone using Python standard library (http.server + socketserver)
with CORS, JSON serialization, and automated mock telemetry streaming.
"""

import sys
import os
import json
import time
import math
import numpy as np
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from urllib.parse import urlparse, parse_qs

# Import sibling modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_engine.acoustic_biomarker import AcousticBiomarkerAnalyzer
from core_engine.clinical_triage import ClinicalTriageEngine
from core_engine.climate_analytics import ClimateResilienceEngine
from mesh_network.resilient_mesh import MeshPacket, ResilientMeshRouter
from privacy_security.crypto_vault import DifferentialPrivacyEngine, LocalCryptoVault, MerkleAuditTree
from privacy_security.sos_security import EmergencyBeaconEngine
from inclusion_upskill.skill_graph import BlindJobMatcher
from inclusion_upskill.voice_education import VoiceEduEngine

# Singleton Engine Instances
biomarker_analyzer = AcousticBiomarkerAnalyzer()
clinical_engine = ClinicalTriageEngine()
climate_engine = ClimateResilienceEngine()
dp_engine = DifferentialPrivacyEngine(epsilon=0.5)
crypto_vault = LocalCryptoVault()
merkle_ledger = MerkleAuditTree()
sos_beacon = EmergencyBeaconEngine()
job_matcher = BlindJobMatcher()
edu_engine = VoiceEduEngine()

# Seed initial talent and jobs
job_matcher.register_talent_profile("T-801", ["embroidery", "textiles", "quality_audit"], {"craft": 96.0, "reliability": 98.0}, is_female_affirmative=True)
job_matcher.register_talent_profile("T-802", ["organic_farming", "hydroponics", "soil_testing"], {"agri": 92.0}, is_female_affirmative=False)
job_matcher.register_talent_profile("T-803", ["solar_maintenance", "electrical", "iot_sensor"], {"technical": 94.0}, is_female_affirmative=True)

job_matcher.post_job_opportunity("JOB-201", "Handloom Jute & Jamdani Apparel Weaving", ["embroidery", "textiles"], 5500.0, female_priority=True)
job_matcher.post_job_opportunity("JOB-202", "Solar Micro-Grid Inverter Field Inspection", ["solar_maintenance", "electrical"], 4200.0, female_priority=False)

class PrismAPIHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, status_code: int, payload: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self._send_json(200, {
                "status": "ONLINE",
                "system": "PRISM-Edge Unified Core Engine",
                "version": "2.4.0-PROD",
                "timestamp": time.time(),
                "uptime_seconds": 3600
            })
        elif path == "/api/telemetry/live":
            # Real-time multi-track snapshot
            t = time.time()
            sim_temp = 28.0 + 4.0 * math.sin(t / 60.0)
            sim_humidity = 65.0 + 10.0 * math.cos(t / 45.0)
            sim_rain = 15.0 + 20.0 * max(0.0, math.sin(t / 30.0))
            climate_eval = climate_engine.calculate_micro_climate_risk({
                "temperature_c": sim_temp,
                "humidity_pct": sim_humidity,
                "rainfall_3h_mm": sim_rain,
                "soil_moisture_pct": 62.0
            })
            self._send_json(200, {
                "timestamp": t,
                "climate": climate_eval,
                "merkle_root": merkle_ledger.compute_root_hash(),
                "active_mesh_nodes": 42,
                "dp_epsilon": dp_engine.epsilon,
                "verified_credentials_minted": 1420
            })
        elif path == "/api/courses":
            courses = edu_engine.list_available_courses()
            self._send_json(200, {"courses": courses})
        elif path == "/api/jobs":
            jobs = list(job_matcher.job_listings.values())
            # Convert sets to list
            for j in jobs:
                if isinstance(j.get("required_skills"), set):
                    j["required_skills"] = list(j["required_skills"])
            self._send_json(200, {"jobs": jobs})
        elif path == "/" or path == "/index.html":
            # Serve Web Dashboard
            dashboard_file = os.path.join(os.path.dirname(__file__), "..", "web_dashboard", "index.html")
            if os.path.exists(dashboard_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(dashboard_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._send_json(404, {"error": "Dashboard HTML not found"})
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body.decode('utf-8')) if post_body else {}

        if path == "/api/biomarker/analyze":
            # Generate or process audio signal
            freq = float(data.get("fundamental_freq_hz", 220.0))
            jitter_factor = float(data.get("jitter_factor", 0.02))
            t = np.linspace(0, 1.0, 16000, endpoint=False)
            noise = np.random.normal(0, jitter_factor, len(t))
            audio_signal = 0.5 * np.sin(2 * np.pi * freq * t) + noise
            result = biomarker_analyzer.analyze_audio_buffer(audio_signal)
            merkle_ledger.append_event("BIOMARKER_SCREEN", str(result["vitality_index"]))
            self._send_json(200, result)

        elif path == "/api/clinical/triage":
            triage_type = data.get("type", "maternal")
            if triage_type == "maternal":
                res = clinical_engine.evaluate_maternal_risk(data.get("patient_data", {}))
            else:
                res = clinical_engine.evaluate_pediatric_imci(data.get("child_data", {}))
            merkle_ledger.append_event("CLINICAL_TRIAGE", res.get("triage_urgency", res.get("triage_color", "UNKNOWN")))
            self._send_json(200, res)

        elif path == "/api/climate/analyze":
            res = climate_engine.calculate_micro_climate_risk(data)
            self._send_json(200, res)

        elif path == "/api/climate/crop":
            res = climate_engine.diagnose_crop_pathology(data.get("crop_type", "rice"), data.get("symptoms", []))
            self._send_json(200, res)

        elif path == "/api/security/pin":
            entered_pin = data.get("pin", "")
            gps = tuple(data.get("gps", [23.8103, 90.4125]))
            res = sos_beacon.process_pin_entry(entered_pin, gps)
            self._send_json(200, res)

        elif path == "/api/jobs/match":
            job_id = data.get("job_id", "JOB-201")
            matches = job_matcher.match_candidates_for_job(job_id)
            self._send_json(200, {"job_id": job_id, "candidates": matches})

        elif path == "/api/courses/quiz":
            cid = data.get("course_id", "EDU-AGRI-101")
            answers = data.get("answers", [0, 0])
            res = edu_engine.evaluate_quiz_submission(cid, answers)
            if res.get("passed"):
                merkle_ledger.append_event("CREDENTIAL_MINT", res["verified_certificate_token"])
            self._send_json(200, res)

        elif path == "/api/privacy/encrypt":
            raw_text = data.get("text", "")
            enc = crypto_vault.encrypt_record(raw_text)
            self._send_json(200, enc)

        elif path == "/api/privacy/decrypt":
            dec = crypto_vault.decrypt_record(data)
            self._send_json(200, {"decrypted_text": dec})

        else:
            self._send_json(404, {"error": f"Endpoint {path} not found"})

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def run_server(port: int = 8080):
    server_address = ('0.0.0.0', port)
    httpd = ReusableTCPServer(server_address, PrismAPIHandler)
    print(f'[PRISM-Edge] Production API Server active at http://localhost:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[PRISM-Edge] Server stopped gracefully.')
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
