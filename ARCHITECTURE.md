# System Architecture & Design

PRISM-Edge is designed around a zero-cloud-dependency paradigm. This document outlines the core components of the 7-pillar architecture.

## 1. Edge Intelligence Core (`core_engine/`)
All machine learning and signal processing algorithms are quantized for ARM64/Edge processors.
- **Acoustic Biomarker Pipeline**: Uses time-domain waveform analysis (autocorrelation) to extract $F_0$, jitter, and shimmer.
- **Clinical Triage Engine**: Encodes WHO EmONC (Maternal) and HBB APGAR (Neonatal) decision trees as directed acyclic graphs (DAGs) for $O(1)$ constant-time evaluation.
- **Agro-Meteorological Engine**: Computes Steadman Heat Indices and coastal estuarine electrical conductivity (EC).

## 2. Mesh Networking (`mesh_network/`)
- **Base91 Serialization**: Structured JSON payloads are packed into binary and encoded using Base91 ($1.23$ bytes per char) to ensure maximum payload fits within a single $140$-octet SMS or BLE advertisement packet.
- **Store-and-Forward Gossip**: Nodes hold encrypted Merkle blocks in a local cache. When a peer is discovered via WiFi-Direct or BLE, a vector-clock synchronization resolves missing blocks.

## 3. Privacy & Security (`privacy_security/`)
- **Differential Privacy ($\epsilon = 0.5$)**: Laplace noise is injected at the edge before any aggregated metrics are shared, mathematically bounding the probability of individual record reconstruction.
- **Duress Protocol**: Physical coercion triggers a covert panic mode via a duress PIN (`9999`), zeroizing local keys while broadcasting a geofenced SOS.
