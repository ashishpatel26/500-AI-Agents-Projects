from src.health_agent import analyze_symptoms

def main():
    print("🩺 AI Health Assistant")
    print("---------------------")

    symptoms = input("Enter your symptoms: ")
    result = analyze_symptoms(symptoms)

    print("\nAnalysis Result:")
    print(result)

if __name__ == "__main__":
    main()
