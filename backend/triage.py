# backend/triage.py

EMERGENCY_KEYWORDS = [
    # Français
    "douleur thoracique", "douleur poitrine", "mal à la poitrine",
    "difficultés à respirer", "du mal à respirer", "essoufflement soudain",
    "perte de conscience", "je m'évanouis", "je vais m'évanouir",
    "saignement abondant", "je saigne beaucoup",
    "paralysie", "je ne sens plus", "je ne bouge plus",
    "convulsion", "crise épilepsie",
    "overdose", "surdose", "j'ai avalé", "empoisonnement",
    "accident vasculaire", "avc",
    "crise cardiaque", "infarctus",
    "allergie grave", "choc anaphylactique",
    "urgence", "appel le 15", "samu",

    # Anglais
    "chest pain", "chest tightness", "heart attack",
    "can't breathe", "cannot breathe", "difficulty breathing",
    "shortness of breath", "loss of consciousness", "unconscious",
    "severe bleeding", "heavy bleeding",
    "stroke", "paralysis", "seizure", "convulsion",
    "overdose", "poisoning", "anaphylaxis",
    "emergency", "call 911", "call 999",
    "intense pain", "severe pain", "unbearable pain",
    "i am dying", "i can't move"
]

SPECIALIST_KEYWORDS = {
    "Cardiologue": [
        "heart", "chest", "cardiac", "palpitation", "arrhythmia",
        "blood pressure", "hypertension", "coronary",
        "coeur", "cardiaque", "palpitation", "pression artérielle"
    ],
    "Neurologue": [
        "brain", "headache", "migraine", "seizure", "memory",
        "stroke", "tremor", "numbness", "dizziness",
        "cerveau", "mémoire", "migraine", "vertiges", "engourdissement"
    ],
    "Pneumologue": [
        "lung", "asthma", "breathing", "cough", "bronchitis",
        "pneumonia", "respiratory", "inhaler",
        "poumon", "asthme", "toux", "respiration", "bronchite"
    ],
    "Gastro-entérologue": [
        "stomach", "bowel", "colon", "liver", "digestive",
        "nausea", "vomiting", "diarrhea", "constipation",
        "estomac", "intestin", "foie", "nausée", "vomissement", "diarrhée"
    ],
    "Dermatologue": [
        "skin", "rash", "eczema", "psoriasis", "acne", "itching",
        "peau", "éruption", "démangeaison", "acné"
    ],
    "Néphrologue": [
        "kidney", "urine", "renal", "dialysis", "urinary",
        "rein", "urinaire", "dialyse"
    ],
    "Endocrinologue": [
        "diabetes", "thyroid", "insulin", "hormone", "glucose",
        "diabète", "thyroïde", "insuline", "glycémie"
    ],
    "Psychiatre": [
        "depression", "anxiety", "mental", "psychiatric", "bipolar",
        "schizophrenia", "ptsd", "stress",
        "dépression", "anxiété", "mental", "bipolaire"
    ],
    "Rhumatologue": [
        "arthritis", "joint", "bone", "rheumatoid", "lupus",
        "arthrite", "articulation", "os", "rhumatisme"
    ],
    "Oncologue": [
        "cancer", "tumor", "chemotherapy", "oncology", "malignant",
        "tumeur", "chimiothérapie", "oncologie"
    ]
}


def detect_emergency(user_input: str) -> bool:
    """
    Retourne True si une urgence médicale est détectée
    """
    text = user_input.lower()
    return any(keyword in text for keyword in EMERGENCY_KEYWORDS)


def suggest_specialist(user_input: str) -> str:
    """
    Retourne le type de spécialiste selon les symptômes
    """
    text = user_input.lower()

    for specialist, keywords in SPECIALIST_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return specialist

    return "Médecin généraliste"