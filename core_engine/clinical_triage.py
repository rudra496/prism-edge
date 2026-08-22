"""
PRISM-Edge: Clinical Triage & Maternal-Pediatric Decision Support Engine
Standardized against WHO Integrated Management of Childhood Illness (IMCI)
and Emergency Obstetric & Neonatal Care (EmONC) guidelines.
"""

from typing import Dict, List, Any, Optional

class ClinicalTriageEngine:
    """
    Evaluates vital signs, reported symptom vectors, and maternal risk flags
    to generate deterministic, explainable clinical triage recommendations.
    """

    def evaluate_maternal_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        systolic_bp = patient_data.get("systolic_bp", 120)
        diastolic_bp = patient_data.get("diastolic_bp", 80)
        gestational_weeks = patient_data.get("gestational_weeks", 0)
        symptoms = [s.lower() for s in patient_data.get("symptoms", [])]
        hemoglobin_g_dl = patient_data.get("hemoglobin_g_dl", 12.0)
        fetal_heart_rate_bpm = patient_data.get("fetal_heart_rate_bpm", 140)

        danger_flags: List[str] = []
        urgency = "ROUTINE"
        risk_score = 10.0

        # Preeclampsia / Eclampsia Screening
        if systolic_bp >= 160 or diastolic_bp >= 110:
            danger_flags.append("Severe Hypertension / Critical Preeclampsia Risk")
            urgency = "EMERGENCY"
            risk_score += 50.0
        elif systolic_bp >= 140 or diastolic_bp >= 90:
            danger_flags.append("Moderate Gestational Hypertension")
            if urgency != "EMERGENCY":
                urgency = "URGENT"
            risk_score += 25.0

        if "severe_headache" in symptoms or "blurred_vision" in symptoms or "epigastric_pain" in symptoms:
            danger_flags.append("Neurological / End-Organ Preeclampsia Symptoms")
            urgency = "EMERGENCY"
            risk_score += 30.0

        if "vaginal_bleeding" in symptoms:
            danger_flags.append("Antepartum Hemorrhage Danger")
            urgency = "EMERGENCY"
            risk_score += 45.0

        if hemoglobin_g_dl < 7.0:
            danger_flags.append("Severe Anemia (< 7.0 g/dL)")
            if urgency != "EMERGENCY":
                urgency = "URGENT"
            risk_score += 25.0

        if gestational_weeks >= 24:
            if fetal_heart_rate_bpm < 110 or fetal_heart_rate_bpm > 160:
                danger_flags.append(f"Abnormal Fetal Heart Rate ({fetal_heart_rate_bpm} BPM)")
                urgency = "EMERGENCY"
                risk_score += 35.0

        risk_score = min(100.0, risk_score)

        protocols = []
        if urgency == "EMERGENCY":
            protocols = [
                "Immediate emergency ambulance dispatch to tertiary referral center.",
                "Administer loading dose of Magnesium Sulfate if trained CHW present and preeclampsia suspected.",
                "Maintain left lateral recumbent positioning and high-flow O2 if available."
            ]
        elif urgency == "URGENT":
            protocols = [
                "Schedule priority same-day consultation with Community Health Officer.",
                "Initiate daily BP telemetry tracking via PRISM mesh beacon.",
                "Administer oral iron-folic acid therapy and dietary fortification."
            ]
        else:
            protocols = [
                "Continue standard antenatal care (ANC) schedule.",
                "Nutritional counseling: iron-rich foods, calcium, clean hydration.",
                "Maintain scheduled tele-checkin in 14 days."
            ]

        return {
            "triage_urgency": urgency,
            "composite_risk_score": round(risk_score, 1),
            "danger_flags": danger_flags,
            "recommended_protocols": protocols,
            "guideline_standard": "WHO EmONC / Safe Motherhood Protocol"
        }

    def evaluate_pediatric_imci(self, child_data: Dict[str, Any]) -> Dict[str, Any]:
        age_months = child_data.get("age_months", 12)
        temp_c = child_data.get("temperature_c", 37.0)
        respiratory_rate_bpm = child_data.get("respiratory_rate_bpm", 30)
        symptoms = [s.lower() for s in child_data.get("symptoms", [])]
        muac_mm = child_data.get("muac_mm", 135) # Mid-Upper Arm Circumference

        danger_signs = []
        triage = "GREEN"

        # General Danger Signs
        if "unable_to_drink" in symptoms or "vomiting_everything" in symptoms or "convulsions" in symptoms or "lethargic" in symptoms:
            danger_signs.append("General Danger Sign Present (IMCI Stage 3)")
            triage = "RED"

        # Fast Breathing / Pneumonia
        fast_breathing_threshold = 50 if age_months < 12 else 40
        if respiratory_rate_bpm > fast_breathing_threshold or "chest_indrawing" in symptoms or "stridor" in symptoms:
            danger_signs.append(f"Pneumonia Indicator: Fast Breathing ({respiratory_rate_bpm} bpm)")
            if triage != "RED":
                triage = "YELLOW"

        # SAM (Severe Acute Malnutrition)
        if muac_mm < 115 or "bilateral_pitting_edema" in symptoms:
            danger_signs.append(f"Severe Acute Malnutrition (MUAC {muac_mm} mm)")
            if triage != "RED":
                triage = "YELLOW"

        # High Fever
        if temp_c >= 39.0:
            danger_signs.append(f"High Pyrexia ({temp_c}°C)")
            if triage != "RED":
                triage = "YELLOW"

        actions = {
            "RED": "Immediate Urgent Referral to Hospital; give pre-referral treatment (antibiotic/antimalarial/paracetamol/ORS).",
            "YELLOW": "Specific medical treatment by Local Health Officer; home care education and 48-hr follow-up.",
            "GREEN": "Home management, continued feeding, fluids, and return for immunization."
        }

        return {
            "triage_color": triage,
            "danger_signs": danger_signs,
            "clinical_action": actions[triage],
            "muac_classification": "Severe Malnutrition" if muac_mm < 115 else ("Moderate Malnutrition" if muac_mm < 125 else "Adequate"),
            "guideline": "WHO / UNICEF IMCI Integrated Protocol"
        }
