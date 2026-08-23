# PRISM-Edge — Pitch Deck Outline (8 slides / 5 minutes)

> Judged on: **originality · feasibility · social impact · meaningful use of AI**
> (published FutureMakers criteria). Every slide maps to one criterion.

---

## Slide 1 — The night the network died (Impact)
**Visual:** news photo strip of Cyclone Remal flooding + headline "26,000+ towers down".
**Say:** *"In May 2024, Cyclone Remal silenced more than 26,000 mobile towers in Bangladesh.
For a pregnant woman in labour, losing the network can mean losing the referral that saves
her life or her baby's. 131 mothers per 100,000 births still die here; most newborn deaths
happen in the first week — exactly when decisions must be fastest."*
*(All numbers cited on our site's References section.)*

## Slide 2 — Why current solutions fail (Originality of framing)
Cloud apps need what blackouts destroy. Paper flip-charts can't escalate.
Messaging apps need data for every single message.
**One line:** *"Every existing tool assumes connectivity. We assume it disappears."*

## Slide 3 — What we built (Solution)
PRISM-Edge = CHW companion that **assesses offline, decides by WHO rules, and relays
through blackout**. Show the three-part diagram: on-device AI → WHO triage →
phone-to-phone lifeline packets.

## Slide 4 — Live demo (Feasibility — the trust builder)
Open `rudra496.github.io/prism-edge`:
1. Voice screener — speak; watch real jitter/shimmer/F₀ compute live. "No canned numbers — view source."
2. Cyclone simulator — fill vitals; AI says HIGH risk (78%); encode → 43/160 chars;
   packet hops village→CHW→market→shelter→clinic while every tower is down.
3. Turn off Wi-Fi. The site still works — because it's a PWA, like the real system.

## Slide 5 — The meaningful AI (AI criterion)
- Random forest trained on UCI Maternal Health Risk dataset (1,014 patients, DOI cited):
  **81.3 % hold-out accuracy**, exported to one JSON file running *identically* in browser
  and Python (78.4 % vs 78.45 % on the same patient).
- Acoustic prosody pipeline mirroring research speech-biomarker features.
- Deterministic WHO IMCI/EmONC/APGAR decision trees — auditable, not black-box.
- Honest limits stated on-slide: thresholds illustrative until field-labelled data.

## Slide 6 — Novelty: an app dies with the network; a protocol doesn't
We turned an obstetric emergency referral into a **standardised 30-byte / 43-character,
CRC-protected, PII-free wire format** that hops any phone with SMS or Bluetooth.
This is licensable network infrastructure for operators — GP's own blackout problem.

## Slide 7 — Business & path to impact (B2B2G)
1. Telecom resilience licensing (branded lifeline for subscribers in blackout zones).
2. NGO/DGHS per-CHW licence (< $5/CHW/year — cheaper than reprinting flip-charts).
3. OEM pre-install on health tablets.
Beachhead: 13 coastal cyclone-prone districts. No invented TAM — bottom-up sizing after
pilot pricing interviews (methodology available).

## Slide 8 — Pilot ask (Feasibility close)
12 weeks, 2 upazilas, 50 CHWs (see `PILOT_PLAN.md`): measure detection-to-referral latency,
referral completion %, false-alert burden vs paper baseline. Deliverable: evidence pack +
calibrated Bangla model. **"Fund the pilot that turns this from a working system into a
measured one."**

---

### Delivery tips
- Team speaks alternately; demo is done live, never video-only.
- If Wi-Fi fails at the venue: that IS the demo — open the PWA offline.
- Keep Bangla phrases ready ("মায়ের সংকেত পৌঁছাবে") — judges are Bangladeshi executives.
