# 🌍 PRISM-Edge Ecosystem

![Version](https://img.shields.io/badge/version-2.4.0--PROD-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Edge%20%7C%20ARM64-lightgrey.svg)

**Decentralized Intelligence. Zero Cloud Dependency.**

PRISM-Edge is a production-grade, offline-first operating ecosystem designed for emerging markets and disaster-stricken zones. When natural disasters destroy cellular grids, PRISM-Edge executes critical medical triage and climate telemetry directly on-chip, synchronizing data globally via an encrypted P2P mesh network.

## 🚀 Live Interactive Dashboard
Experience the core engines directly in your browser (Zero Cloud Upload, 100% Local Execution):
**[Launch Web Terminal](https://rudra496.github.io/prism-edge/)**

---

## 📖 Table of Contents
1. [Core Features](#-core-features)
2. [Project Structure](#-project-structure)
3. [How It Works (Simplified)](#-how-it-works-simplified)
4. [Installation & Setup](#-installation--setup)
5. [Documentation](#-documentation)

---

## 🌟 Core Features

- **🩺 Clinical Triage Engine**: Extracts acoustic biomarkers (pitch, jitter) from voice to detect dysphoria/depression. Integrates the WHO EmONC maternal algorithms directly on-silicon.
- **⛈️ Agro-Climate Resilience**: Computes coastal estuarine salinity and Steadman heat matrices using local sensors, generating farming heuristics without internet.
- **📡 Global Mesh Routing**: Uses a custom **Base91 Gossip Protocol** to heavily compress telemetry and bounce it peer-to-peer via SMS/BLE fallback channels.
- **🔐 Differential Privacy**: Injects Laplace noise ($\epsilon = 0.5$) to mathematically guarantee anonymity before any data hits the mesh.

---

## 📂 Project Structure

A comprehensive, production-ready monorepo layout:

```text
prism-edge/
├── .github/                  # CI/CD and Issue Templates
├── assets/                   # High-res graphics and UI assets
├── docs/                     # Architecture, Security, and API documentation
│   └── api/                  # Developer API references
├── src/                      # Core Production Source Code
│   ├── core/                 # Edge ML & Offline Processing
│   │   ├── health/           # Acoustic Biomarkers & WHO Triage
│   │   └── climate/          # Agro-meteorological models
│   ├── mesh/                 # Base91 Router & P2P Gossip
│   └── security/             # Laplace Privacy & Encryption
├── tests/                    # Unit and Integration test suites
├── web_dashboard/            # Live HTML5 Interactive Dashboard
├── ARCHITECTURE.md           # Deep-dive system design
├── SECURITY.md               # Threat models & protocols
└── README.md                 # Project Overview
```

---

## 🧠 How It Works (Simplified)

### 1. The Problem
In rural areas or during floods/earthquakes, internet connectivity dies. Traditional AI fails because it relies on cloud servers (AWS, Google Cloud) to process data. 

### 2. The PRISM-Edge Solution
We moved the "brain" to the device. 
1. **Local Collection**: Voice or climate data is collected via the phone or IoT sensor.
2. **On-Chip AI**: The device uses its own processor to instantly analyze the data (e.g., diagnosing respiratory issues) in under 15 milliseconds.
3. **Encrypted Mesh**: The device compresses the diagnosis and sends it via Bluetooth or SMS to the nearest active device, forming a chain until it reaches the global network.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rudra496/prism-edge.git
   cd prism-edge
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the local Edge router:**
   ```bash
   python src/mesh/base91_router.py --start
   ```

## 🤝 Contributing
Please see `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` for details on submitting pull requests.

## 📄 License
This project is licensed under the MIT License - see the `LICENSE` file for details.
