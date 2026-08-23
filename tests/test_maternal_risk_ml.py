"""
PRISM-Edge: Portable Maternal Risk Model Tests
Validates the exported forest (ml/model_weights.json) loads and predicts
sensibly WITHOUT sklearn, mirroring edge-device conditions.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_engine.maternal_risk_ml import MaternalRiskModel


class TestMaternalRiskModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model = MaternalRiskModel()

    def test_model_artefact_provenance(self):
        self.assertIn("doi", self.model.meta["dataset"])
        self.assertEqual(self.model.meta["dataset"]["doi"], "10.24432/C5DP5D")
        self.assertEqual(self.model.forest["n_trees"], 40)
        acc = self.meta_acc()
        self.assertGreater(acc, 0.75, "holdout accuracy regressed below trained value")

    def meta_acc(self):
        return self.model.meta["metrics_holdout"]["forest_accuracy"]

    def test_high_risk_case(self):
        # Classic severe pre-eclampsia-adjacent vitals (UCI high-risk region)
        res = self.model.predict(
            age=30, systolic_bp=160, diastolic_bp=100,
            blood_glucose=15.0, body_temp_f=103.0, heart_rate=85
        )
        self.assertEqual(res["risk_class"], "high")
        self.assertGreater(res["probabilities"]["high"], res["probabilities"]["low"])
        self.assertIn("doi", res["model"])

    def test_low_risk_case(self):
        res = self.model.predict(
            age=25, systolic_bp=100, diastolic_bp=70,
            blood_glucose=6.5, body_temp_f=98.0, heart_rate=76
        )
        self.assertIn(res["risk_class"], ("low", "mid"))

    def test_probabilities_sum_to_one(self):
        res = self.model.predict(
            age=20, systolic_bp=120, diastolic_bp=80,
            blood_glucose=7.0, body_temp_f=98.6, heart_rate=80
        )
        total = sum(res["probabilities"].values())
        self.assertAlmostEqual(total, 1.0, delta=0.01)


if __name__ == "__main__":
    unittest.main()
