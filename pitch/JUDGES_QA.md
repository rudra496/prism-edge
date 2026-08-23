# Judges' Q&A — Anticipated Questions & Prepared Answers

## Technical / AI

**Q: "Is this real AI or rule-based wrappers?"**
A: Three layers, each with a distinct role. A random forest trained on the UCI Maternal
Health Risk dataset (DOI 10.24432/C5DP5D) — 81.3 % hold-out accuracy, exported to JSON so
it runs identically in-browser and on-device. An acoustic DSP pipeline extracting
research-standard prosody features (F₀, jitter, shimmer). And deterministic WHO IMCI/EmONC
decision trees for the clinical rules — deliberately auditable, because a triage system
judges' own families might rely on should never be an unexplainable black box.

**Q: "How accurate is it really?" / "Will it misdiagnose?"**
A: The risk model reaches 81.3 % accuracy and 0.815 macro-F1 on held-out data — good for a
3-class problem with 1,014 samples, and we publish the confusion matrix. But we are careful:
this is *decision support for trained health workers*, not a diagnosis. It prioritises who a
CHW escalates first; the CHW and protocol remain the clinical authority.

**Q: "Why not just use WhatsApp/SMS gateway when network returns?"**
A: Because the emergency happens *while* the network is down. Store-and-forward mesh means
the alert is already moving during the outage, arriving the second any node finds signal.
Also, our packets are structured 30-byte frames with CRC — machine-readable at the clinic,
not free text.

**Q: "What stops spoofed/malicious packets in the mesh?"**
A: Current design: CRC-32 integrity + duplicate suppression + TTL bounds + no PII on wire.
Roadmap (SECURITY.md): per-node HMAC chain of trust provisioned via CHW registration.
We state openly that adversarial hardening is pilot-stage work.

## Impact / feasibility

**Q: "Has this been tested with real users?"**
A: Not yet — that's precisely what our 12-week, 50-CHW pilot measures: detection-to-referral
latency vs paper baseline, referral completion rate, false-alert burden. We won't claim field
results we don't have; we will produce them.

**Q: "Why would Grameenphone care?"**
A: Operators lose revenue and reputation when cyclones kill towers — 26,000+ went down in
Remal alone. PRISM-Edge becomes a branded resilience service: the GP lifeline that still
works. It rides SMS/BLE — GP's own rails — and creates social impact data GP can report.

**Q: "Cost per user?"**
A: Software licence target under $5/CHW/year, zero server cost by design (the architecture
has no cloud), relay traffic carried by existing handsets. Cheaper than reprinting one set
of paper flip-charts.

**Q: "What about phones without Bluetooth/SMS credit?"**
A: Any phone can originate an SMS packet; BLE/WiFi-Direct only accelerates hops between
smartphones. SMS fallback works on feature phones.

## Competition-fit

**Q: "Someone has done offline health apps before."**
A: Apps die with connectivity; a *protocol* doesn't. Our novelty is the standardised
lifeline-packet format plus WHO-structured triage inside 43 characters — licensable
infrastructure rather than another app. We also publish cross-language proofs
(JS-encoded packets decode byte-perfectly in Python) instead of screenshots.

**Q: "What's the IP situation?"**
A: MIT-licensed core; we'd negotiate operator licensing separately. University-student IP
terms accepted as-is per FutureMakers rules.

**Q: "What do you need next?"**
A: The pilot: two coastal upazilas, 50 CHWs, 12 weeks, ethics approval through a partner
NGO, and GP's SMS-rate support. Deliverable: calibrated Bangla model + measured impact pack.
