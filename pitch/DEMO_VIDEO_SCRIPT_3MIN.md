# PRISM-Edge — 3-Minute Demo Video Script

> Format: screen recording + voiceover. Record at 1080p; keep every cut ≤ 8 s.
> Total: ~3:00. Bangla lines subtitled in English.

---

**[0:00–0:20] Cold open — the problem**
*(Rain audio under. News headline overlay: "Cyclone Remal: 27,000 cell phone towers down" — Dhaka Tribune, May 2024.)*
VO: "May 2024. Cyclone Remal silences 26,000+ mobile towers across Bangladesh.
For thousands of pregnant women in coastal villages, the phone that should call the
 ambulance… becomes a brick."

**[0:20–0:40] The idea**
*(Title card: PRISM-Edge — ঘূর্ণিঝড়েও নিরাপদ / Safe even in cyclones.)*
VO: "What if health screening didn't need the network at all — and alerts could hop
phone-to-phone until they find one? That's PRISM-Edge."

**[0:40–1:30] Live demo 1 — on-device AI screening**
*(Screen capture: rudra496.github.io/prism-edge/demo/)*
VO: "This is a real microphone, real DSP, zero servers."
*(Speak into mic; waveform dances; strain index and jitter/shimmer update live.)*
VO: "Pitch, jitter, shimmer, pause ratio — computed on-device, in your browser.
The same pipeline ships to CHW phones. Nothing here is canned — view source."

**[1:30–2:25] Live demo 2 — the blackout relay**
*(Screen capture: Cyclone Blackout Simulator tab.)*
VO: "A health worker enters vitals during a total blackout."
*(Type BP 165, HR 48, temp 38.6 → AI panel: 'HIGH risk (78% confidence)'.)*
VO: "An AI model trained on the UCI maternal-risk dataset runs right here in the browser —
81 percent hold-out accuracy, no internet required."
*(Click Encode → show hex bytes + Base91 string + badge '43/160 chars ✓ fits ONE SMS'.)*
VO: "One referral becomes 43 characters. No names leave the village — just a CRC-protected code."
*(Click Relay → nodes light up one by one: home → CHW → market tea-stall → school shelter → clinic.)*
VO: "Every hop is a real protocol step: store-and-forward gossip, TTL countdown,
CRC verification. The moment ANY node touches any network, the doctor sees this—"
*(Clinic card flips open with decoded JSON: EMERGENCY, BP 165, GPS Barishal.)*

**[2:25–2:45] The offline proof**
*(Recording shows Wi-Fi being switched off; site reloads perfectly from cache.)*
VO: "By the way — we just turned off the internet. Our own site still works.
Offline-first isn't a slide for us. It's how it's built."

**[2:45–3:00] Close**
*(Title card over calm sunrise footage:)*
VO: "PRISM-Edge. When the towers die, mothers shouldn't.
We're ready to pilot with 50 community health workers this season."
*(End card: github.com/rudra496/prism-edge · rudra496.github.io/prism-edge)*

---

### Shot list / assets needed
- Screen recordings of both demos (OBS, 1080p)
- Rain/storm SFX + calm ambient for close
- Subtitle track EN + BN
