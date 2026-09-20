# Bayesian Network: Predict Disease Name using Bayes' Theorem

def bayes_theorem(p_a, p_b_given_a, p_b_given_not_a):
    """Compute P(A|B) using Bayes' theorem."""
    p_not_a = 1 - p_a
    p_b = p_b_given_a * p_a + p_b_given_not_a * p_not_a
    return (p_b_given_a * p_a) / p_b

print("=== Bayesian Network: Disease Prediction ===\n")
print("We will consider 3 possible diseases: Flu, Covid, Allergy.\n")

# Prior probabilities
p = {
    "Flu": 0.2,
    "Covid": 0.1,
    "Allergy": 0.15
}

# Conditional probabilities
symptom_given = {
    "Flu": 0.8,
    "Covid": 0.9,
    "Allergy": 0.7
}
test_given = {
    "Flu": 0.6,
    "Covid": 0.95,
    "Allergy": 0.4
}

# Ask user for evidence
has_symptom = input("Does the patient have fever/cough symptoms? (y/n): ").lower() == 'y'
test_positive = input("Is the test positive? (y/n): ").lower() == 'y'

# False positive rates
p_symptom_given_no_disease = 0.1
p_test_given_no_disease = 0.05

# Compute posterior probabilities
posteriors = {}
for disease in p.keys():
    if has_symptom and test_positive:
        p_b_given_a = symptom_given[disease] * test_given[disease]
        p_b_given_not_a = p_symptom_given_no_disease * p_test_given_no_disease
    elif has_symptom:
        p_b_given_a = symptom_given[disease]
        p_b_given_not_a = p_symptom_given_no_disease
    elif test_positive:
        p_b_given_a = test_given[disease]
        p_b_given_not_a = p_test_given_no_disease
    else:
        p_b_given_a = 1
        p_b_given_not_a = 1

    posteriors[disease] = bayes_theorem(p[disease], p_b_given_a, p_b_given_not_a)

# Normalize
total = sum(posteriors.values())
for disease in posteriors:
    posteriors[disease] /= total

# Display results
predicted = max(posteriors, key=posteriors.get)

print("\n--- Results ---")
for d, val in posteriors.items():
    print(f"P({d} | evidence) = {val * 100:.2f}%")
print(f"\nMost likely disease: {predicted}")
