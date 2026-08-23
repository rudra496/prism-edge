# PRISM-Edge Field Pilot Plan (12 weeks, draft for partner discussion)

## Objective
Turn a working system into a *measured* system: quantify whether offline-first screening
+ mesh relay shortens detection-to-referral time and improves referral completion versus
the current paper workflow.

## Setting & partners
- **Where:** 2 coastal upazilas in the cyclone belt (e.g., Barguna / Patuakhali region),
  chosen because tower blackouts recur (Remal-class events) and maternal services are thin.
- **Who:** 50 government/NGO community health workers; 2 upazila health complexes as
  receiving sites; 1 NGO partner for ethics, training and supervision.
- **Ethics:** informed consent in Bangla (written + read-aloud), opt-out at any time,
  no PII leaves devices (protocol-level guarantee), aggregate reporting only under
  differential privacy (ε = 0.5). Approval sought via partner NGO's IRB before enrolment.

## Arms
| Arm | CHWs | Workflow |
|---|---|---|
| Control | 25 | Current paper register + phone calls when signal exists |
| Treatment | 25 | PRISM-Edge app (vitals + voice screening, lifeline packets via SMS/BLE) |

Both arms continue all standard DGHS protocols; PRISM is decision support only.

## Primary metrics
1. **Detection→referral latency**: median hours from danger-sign identification to facility
   acknowledgement (mesh timestamps vs paper dates).
2. **Referral completion %**: referrals reaching the facility within protocol window.
3. **Alert burden**: EMERGENCY alerts per CHW-week + clinician-rated appropriateness sample.

## Secondary / model workstream
- 200 consented voice samples (Bangla) with clinical labels → first *field-labelled*
  calibration set for the prosody strain index (replacing illustrative thresholds).
- Vitals collected on UCI-compatible form → evaluate/refresh risk model on local cohort;
  publish confusion matrix openly.
- Mesh performance during degraded network days: delivery latency vs outage duration.

## Timeline
| Weeks | Activity |
|---|---|
| 1–2 | Ethics approval, recruitment, baseline workflow audit |
| 3–4 | Device setup, CHW training (4 h), Bangla UX dry-runs |
| 5–12 | Live operation; weekly data quality checks; adverse-event review board |
| 13+ | Analysis, public results pack, model recalibration, scale-up proposal |

## Budget sketch (to finalise with partner)
Devices (50 rugged budget phones) · SIM/SMS bundle · training logistics · CHW stipend top-up ·
independent data auditor. Target total under typical innovation-grant envelopes
(final figures after partner quotes — deliberately not invented here).

## Success criteria to proceed to scale
- ≥ 30 % reduction in median detection→referral latency vs control
- ≥ 90 % CHW weekly-active retention without coercion
- Zero privacy incidents; clinician-rated appropriate-alert rate ≥ 80 %
