rules = {
    "flu": {"fever", "cough", "body ache"},
    "cold": {"sneezing", "runny nose", "cough"},
    "malaria": {"fever", "chills", "sweating"},
    "typhoid": {"fever", "abdominal pain", "fatigue"},
    "migraine": {"headache", "nausea", "sensitivity to light"},
    "covid": {"fever", "cough", "loss of taste", "fatigue"},
}
# Function for forward chaining
def forward_chaining(symptoms, rules):
    inferred = []
    for disease, conds in rules.items():
        if conds.issubset(symptoms):
            inferred.append((disease, conds))
    return inferred

# MAIN PROGRAM 
print("\n MEDICAL DIAGNOSIS EXPERT SYSTEM \n")
print("Available Symptoms:")
all_symptoms = sorted({s for conds in rules.values() for s in conds})
print(", ".join(all_symptoms))

# Get user input
user_input = input("\nEnter observed symptoms (comma-separated): ").lower().split(",")
symptoms = {s.strip() for s in user_input if s.strip()}

# Forward chaining inference
inferred_diseases = forward_chaining(symptoms, rules)
# Display results
if inferred_diseases:
    for disease, conds in inferred_diseases:
        print(f"\nInferred: {disease} from {conds}")
    print("\nPossible Diagnoses:")
    for disease, _ in inferred_diseases:
        print(f"- {disease}")
else:
    print("\nNo diagnosis could be inferred from the given symptoms.")
    print("Please provide more symptoms or consult a doctor.")
