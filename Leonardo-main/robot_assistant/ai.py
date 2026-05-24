import random
import unicodedata
import re
import os
from datetime import datetime
from thefuzz import process

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

responses = {
    "greeting": {
        "keywords": ["γεια", "καλημερα", "καλησπερα", "hello", "χαιρετε"],
        "answers": [
            "Γεια σου! Χαίρομαι που σε βλέπω!",
            "Καλησπέρα! Πώς μπορώ να βοηθήσω;",
            "Γεια! Τι κάνουμε σήμερα;"
        ],
        "emotion": "happy"
    },
    
    # --- YOUR PROJECT TEXT FILES ---
    "grandparent_guardian": {
        "keywords": ["grandparent guardian", "παππους", "ρομποτ για ηλικιωμενους", "ανιχνευση πτωσης"],
        "file": "GrandParent_Guardian.txt",
        "emotion": "talking"
    },
    "kalypso": {
        "keywords": ["πες μου για την καλυψω", "τι ειναι η καλυψω", "καλυψω", "kalypso"],
        "file": "kalipsos.txt",
        "emotion": "talking"
    },
    "pharos": {
        "keywords": ["pharos", "φαρος", "πες μου για τον φαρο", "ρομποτ φαρος"],
        "file": "Pharos.txt",
        "emotion": "talking"
    },
    "sheguard": {
        "keywords": ["sheguard", "she guard", "εφαρμογη προστασιας", "τι ειναι το sheguard"],
        "file": "SHEGUARD.txt",
        "emotion": "talking"
    },
    # -------------------------------

    "how_are_you": {
        "keywords": ["τι κανεις", "πως εισαι", "ολα καλα", "πως παει"],
        "answers": [
            "Είμαι πολύ καλά! Εσύ;",
            "Όλα τέλεια! Πώς είσαι εσύ;"
        ],
        "emotion": "happy"
    },
    "name": {
        "keywords": ["πως σε λενε", "ονομα σου", "ποιος εισαι"],
        "answers": [
            "Είμαι ο Ελ Γκρέκο!",
            "Το όνομά μου είναι Ελ Γκρέκο."
        ],
        "emotion": "happy"
    },
    "capabilities": {
        "keywords": ["τι μπορεις να κανεις", "βοηθεια"],
        "answers": [
            "Μπορώ να μιλήσω μαζί σου, να σου πω την ώρα, να κάνω μαθηματικά, και να διαβάσω αρχεία!"
        ],
        "emotion": "talking"
    },
    "thanks": {
        "keywords": ["ευχαριστω", "thanks", "να σαι καλα"],
        "answers": ["Παρακαλώ!", "Με χαρά!"],
        "emotion": "happy"
    },
    "bye": {
        "keywords": ["αντιο", "bye", "τα λεμε", "καληνυχτα", "κλεισε"],
        "answers": ["Αντίο!", "Τα λέμε σύντομα!"],
        "emotion": "neutral"
    }
}

all_keywords = {}
for intent, data in responses.items():
    for kw in data["keywords"]:
        all_keywords[kw] = intent

def solve_math(text):
    text = text.replace("συν", "+").replace("πλην", "-").replace("επι", "*").replace("δια", "/")
    math_pattern = r'(\d+)\s*([\+\-\*\/])\s*(\d+)'
    match = re.search(math_pattern, text)
    
    if match:
        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))
        
        try:
            if operator == '+': result = num1 + num2
            elif operator == '-': result = num1 - num2
            elif operator == '*': result = num1 * num2
            elif operator == '/': result = round(num1 / num2, 2)
            return f"Το αποτέλεσμα είναι {result}"
        except ZeroDivisionError:
            return "Δεν μπορώ να διαιρέσω με το μηδέν!"
    return None

def basic_response(text):
    text = normalize(text)

    if "ωρα" in text:
        now = datetime.now().strftime("%H:%M")
        return f"Η ώρα είναι {now}", "neutral"

    if "ημερομηνια" in text or "μερα" in text:
        today = datetime.now().strftime("%d/%m/%Y")
        return f"Σήμερα είναι {today}", "neutral"

    if "ποσο κανει" in text or "+" in text or "-" in text:
        math_result = solve_math(text)
        if math_result:
            return math_result, "talking"

    choices = list(all_keywords.keys())
    best_match, score = process.extractOne(text, choices)

    if score >= 75:
        matched_intent = all_keywords[best_match]
        data = responses[matched_intent]

        if "file" in data:
            file_path = data["file"]
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    answer = f.read().strip()
            else:
                answer = f"Συγγνώμη, δεν βρήκα το αρχείο {file_path}."
        else:
            answer = random.choice(data["answers"])

        emotion = data["emotion"]
        return answer, emotion

    return None, None
