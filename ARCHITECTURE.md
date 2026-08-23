# System Architecture & Design

PRISM-Edge is designed around a zero-cloud-dependency paradigm: intelligence at the
edge, connectivity treated as an *opportunistic luxury*, and privacy enforced before
any byte leaves a device.

## 1. Edge Intelligence Core (`core_engine/`)
All signal processing and inference run on-device, quantised for ARM-class CPUs.
- **Acoustic Biomarker Pipeline** (`acoustic_biomarker.py`): time-domain waveform
  analysis (autocorrelation) extracting F₀, jitter, shimmer, pause ratio and
  spectral flatness. The browser demo in `demo/` implements the identical
  decision logic in JavaScript so judges can verify behaviour live.
- **Maternal Risk Model** (`maternal_risk_ml.py` + `ml/model_weights.json`): random
  forest (40 trees, depth 8) trained on UCI Maternal Health Risk data
  (DOI 10.24432/C5DP5D; hold-out accuracy 81.3 %, macro-F1 0.815). Exported as flat
  node arrays — inference needs only `json`, no ML framework, identical arithmetic
  in Python and JS.
- **Clinical Triage Engine** (`clinical_triage.py`): WHO EmONC (maternal), UNICEF/WHO
  IMCI danger signs and APGAR / Helping Babies Breathe decision trees evaluated as
  deterministic DAGs — O(1), auditable, no black boxes.
- **Agro-Meteorological Engine** (`climate_analytics.py`): Steadman heat index,
  flood/drought heuristics, coastal salinity advisories for the climate track.

## 2. Mesh Networking (`mesh_network/`)
- **Lifeline Packet Protocol** (`sms_protocol.py`, *the* core innovation): a fixed
  30-byte frame — magic + version + urgency + risk + patient CRC-ref + vitals +
  GPS (fixed-point) + timestamp + CRC-32 — carrying zero PII. Encoded to Base91 it
  occupies **43 characters, provably inside one 160-char GSM-7 SMS**
  (enforced by `tests/test_sms_protocol.py`). Corruption is rejected via CRC.
- **Base91 Serialization**: binary payloads packed into 91 printable chars for
  BLE advertisement / USSD channels.
- **Store-and-Forward Gossip** (`resilient_mesh.py`): duplicate-suppressed,
  TTL-bounded bundle routing between peers with vector-clock-friendly sync.

## 3. Privacy & Security (`privacy_security/`)
- **Differential Privacy (ε = 0.5)**: Laplace noise on aggregates before any
  statistic leaves a village network.
- **Local Crypto Vault + Merkle Audit Tree**: records encrypted at rest;
  tamper-evident event chaining for health visits.
- **Duress Protocol**: covert panic PIN zeroises keys while broadcasting a
  geofenced SOS.

## 4. Deployment Surfaces
| Surface | Artifact | Notes |
|---|---|---|
| Browser (PWA) | `index.html`, `demo/`, `sw.js` | Offline-capable; live mic DSP + cyclone simulator |
| Python edge agent | `scripts/prism_cli.py`, `core_engine/` | CHW laptop / Raspberry-Pi class node |
| REST API | `api_server/server.py` | stdlib-only server exposing every engine |
| Container | `Dockerfile`, `docker-compose.yml` | Clinic gateway deployments |

## 5. Data flow during a blackout
```
[Mother's vitals / voice] → [on-device screening: forest + prosody + WHO rules]
        ↓ EMERGENCY?
[30-byte lifeline packet] --SMS/BLE--> [CHW phone] --> [market node] --> [shelter router]
        (store-and-forward gossip, TTL=7 hops, CRC-checked each hop)
        ↓ any node touches any backhaul
[Clinic dashboard decodes packet → doctor sees urgency + location]
```
