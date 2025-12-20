def analyze_symptoms(symptoms: str) -> str:
    """
    Analyze user symptoms and return possible conditions and precautions.
    """

    symptoms = symptoms.lower()

    if "fever" in symptoms and "cough" in symptoms:
        return (
            "Possible Conditions:\n"
            "- Viral infection\n"
            "- Common cold\n\n"
            "Precautions:\n"
            "- Rest well\n"
            "- Drink plenty of fluids\n"
            "- Consult a doctor if symptoms persist"
        )

    if "headache" in symptoms and "fatigue" in symptoms:
        return (
            "Possible Conditions:\n"
            "- Stress\n"
            "- Dehydration\n\n"
            "Precautions:\n"
            "- Stay hydrated\n"
            "- Get adequate sleep\n"
            "- Reduce screen time"
        )

    return (
        "Possible Conditions:\n"
        "- Insufficient data\n\n"
        "Precautions:\n"
        "- Monitor symptoms\n"
        "- Maintain a healthy routine\n"
        "- Seek medical advice if concerned"
    )
