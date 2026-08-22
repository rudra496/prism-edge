# Contributing to PRISM-Edge

We welcome contributions from researchers, engineers, and healthcare professionals.

## Development Setup
1. Clone the repository: `git clone https://github.com/rudra496/prism-edge.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the test suite: `python tests/test_prism_suite.py`

## Pull Request Process
1. Ensure your code passes all 7 algorithmic tests.
2. If modifying clinical decision trees, cite the relevant WHO/UNICEF protocol.
3. Keep edge latency under $50$ms on ARM64 targets.
4. Open a PR against the `main` branch.
