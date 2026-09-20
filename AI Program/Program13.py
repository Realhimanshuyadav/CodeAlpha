# Bayes' Theorem Program (Percentage Input & Output)

def bayes_theorem(p_a, p_b_given_a, p_b_given_not_a):
    p_a /= 100
    p_b_given_a /= 100
    p_b_given_not_a /= 100
    p_b = p_b_given_a * p_a + p_b_given_not_a * (1 - p_a)
    return (p_b_given_a * p_a / p_b) * 100

print("Bayes' Theorem Calculator\n")

p_a = float(input("Enter P(A) in %: "))
p_b_given_a = float(input("Enter P(B|A) in %: "))
p_b_given_not_a = float(input("Enter P(B|¬A) in %: "))

p_a_given_b = bayes_theorem(p_a, p_b_given_a, p_b_given_not_a)

print(f"\nResult: P(A|B) = {p_a_given_b:.2f}%")

if p_a_given_b > 80:
    print("Interpretation: High likelihood of A given B.")
elif p_a_given_b > 50:
    print("Interpretation: Moderate likelihood of A given B.")
else:
    print("Interpretation: Low likelihood of A given B.")
