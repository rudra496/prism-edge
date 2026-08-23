"""
PRISM-Edge: On-Device Maternal Risk Model (portable inference)

Evaluates the random forest exported by ml/train_model.py against
model_weights.json using plain Python only — no sklearn at inference time,
so the same artefact runs identically on a clinic laptop, a Raspberry Pi
class edge node, or inside the browser demo.

Model provenance is embedded in the JSON itself (dataset DOI, training date,
holdout metrics). This module never invents numbers it cannot read back.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

WEIGHTS_PATH = Path(__file__).resolve().parent.parent / "ml" / "model_weights.json"
LABELS = ["low", "mid", "high"]


def _load():
    if not WEIGHTS_PATH.exists():
        raise FileNotFoundError(
            f"{WEIGHTS_PATH.name} missing — run `python ml/train_model.py` first"
        )
    return json.loads(WEIGHTS_PATH.read_text(encoding="utf-8"))


class MaternalRiskModel:
    """Portable random-forest inference for maternal risk screening."""

    def __init__(self):
        self.meta = _load()
        self.forest = self.meta["forest"]
        self.features = self.meta["dataset"]["features"]

    def _tree_prob(self, tree: Dict[str, List], x: List[float]) -> List[float]:
        node = 0
        while True:
            left = tree["left"][node]
            right = tree["right"][node]
            if left == -1:  # leaf
                return tree["leaf"][node]
            feature = tree["feature"][node]
            go_left = x[feature] <= tree["threshold"][node]
            node = left if go_left else right

    def predict(self, age: float, systolic_bp: float, diastolic_bp: float,
                blood_glucose: float, body_temp_f: float, heart_rate: float) -> Dict[str, Any]:
        x = [age, systolic_bp, diastolic_bp, blood_glucose, body_temp_f, heart_rate]
        probs = [0.0, 0.0, 0.0]
        for tree in self.forest["trees"]:
            p = self._tree_prob(tree, x)
            probs = [pi + pj for pi, pj in zip(probs, p)]
        total = sum(probs) or 1.0
        probs = [p / total for p in probs]
        idx = max(range(len(probs)), key=probs.__getitem__)
        return {
            "risk_class": LABELS[idx],
            "probabilities": {LABELS[i]: round(probs[i], 4) for i in range(len(LABELS))},
            "model": {
                "source": self.meta["dataset"]["name"],
                "doi": self.meta["dataset"]["doi"],
                "holdout_accuracy": self.meta["metrics_holdout"]["forest_accuracy"],
            },
            "disclaimer": "Decision support for trained health workers — not a diagnosis.",
        }


if __name__ == "__main__":
    model = MaternalRiskModel()
    demo = model.predict(age=25, systolic_bp=130, diastolic_bp=80,
                         blood_glucose=15.0, body_temp_f=98.0, heart_rate=86)
    print(demo)
