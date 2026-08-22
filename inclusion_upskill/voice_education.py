"""
PRISM-Edge: Voice-First Inclusive Digital Education Subsystem
Delivers ultra-compact audio-visual micro-learning modules designed for
illiterate, neurodivergent, and rural dialect speakers with spaced repetition.
"""

from typing import Dict, List, Any, Optional

class VoiceEduEngine:
    """
    Manages offline micro-courses, interactive oral quizzes,
    and vernacular skill mastery verification.
    """
    def __init__(self):
        self.course_catalog: Dict[str, Dict[str, Any]] = {
            "EDU-AGRI-101": {
                "title": "Climate-Resilient Hydroponics & Organic Pest Defense",
                "dialect": "Bengali (Chittagong & Sylhet Dialect Pack Supported)",
                "duration_min": 15,
                "size_kb": 85,
                "modules": [
                    {"step": 1, "audio_prompt": "Recognizing early fungal blights on paddy.", "quiz_q": "Which color indicates bacterial leaf blight?", "options": ["Yellow lesions", "Purple spots", "Black holes"], "correct_idx": 0},
                    {"step": 2, "audio_prompt": "Creating biochar from crop residue.", "quiz_q": "What is the key benefit of biochar?", "options": ["Carbon storage & water retention", "Faster weeds", "Acidifies soil"], "correct_idx": 0}
                ]
            },
            "EDU-HEALTH-201": {
                "title": "Community Maternal Health & Nutrition Essentials",
                "dialect": "Standard Bengali / Vernacular Audio",
                "duration_min": 12,
                "size_kb": 70,
                "modules": [
                    {"step": 1, "audio_prompt": "Identifying severe gestational warning signs.", "quiz_q": "What symptom requires emergency doctor visit?", "options": ["Severe headache with blurred vision", "Mild foot swelling", "Craving sour food"], "correct_idx": 0}
                ]
            },
            "EDU-FIN-301": {
                "title": "Digital Micro-Finance, Safe Escrow & Cyber Fraud Defense",
                "dialect": "All Vernaculars",
                "duration_min": 10,
                "size_kb": 60,
                "modules": [
                    {"step": 1, "audio_prompt": "Protecting your mobile banking PIN from scammers.", "quiz_q": "Should you ever share your 4-digit PIN with a caller?", "options": ["Never share with anyone", "Share if caller says they are bank manager", "Write on paper"], "correct_idx": 0}
                ]
            }
        }

    def list_available_courses(self) -> List[Dict[str, Any]]:
        return [
            {
                "course_id": cid,
                "title": data["title"],
                "dialect": data["dialect"],
                "duration_min": data["duration_min"],
                "payload_size_kb": data["size_kb"],
                "module_count": len(data["modules"])
            }
            for cid, data in self.course_catalog.items()
        ]

    def evaluate_quiz_submission(self, course_id: str, answers: List[int]) -> Dict[str, Any]:
        if course_id not in self.course_catalog:
            return {"error": "Course not found"}

        course = self.course_catalog[course_id]
        modules = course["modules"]
        correct_count = 0

        for i, mod in enumerate(modules):
            if i < len(answers) and answers[i] == mod["correct_idx"]:
                correct_count += 1

        score_pct = (correct_count / len(modules)) * 100.0 if modules else 100.0
        passed = score_pct >= 80.0

        certificate_token = f"CERT-{course_id}-{int(score_pct)}-PASS" if passed else None

        return {
            "course_id": course_id,
            "score_pct": round(score_pct, 1),
            "passed": passed,
            "verified_certificate_token": certificate_token,
            "feedback": "Outstanding mastery! Micro-credential minted to your PRISM skill graph." if passed else "Review audio lesson again and retake oral quiz."
        }
