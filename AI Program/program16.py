def combine_evidence(m1, m2):
    combined = {}
    conflict = 0.0

    for A in m1:
        for B in m2:
            intersection = tuple(sorted(set(A).intersection(B)))
            if intersection:
                combined[intersection] = combined.get(intersection, 0) + m1[A] * m2[B]
            else:
                conflict += m1[A] * m2[B]

    # Normalize
    for key in combined:
        combined[key] /= (1 - conflict)
    
    return combined, conflict

def belief(mass, hypothesis):
    return sum(m for h, m in mass.items() if set(h).issubset(hypothesis))

def plausibility(mass, hypothesis):
    return sum(m for h, m in mass.items() if set(h).intersection(hypothesis))

# Define mass functions from Sensor A and Sensor B
m1 = {
    ('Rainy',): 0.6,
    ('Cloudy', 'Rainy'): 0.3,
    ('Sunny', 'Cloudy', 'Rainy'): 0.1  # Total set
}

m2 = {
    ('Cloudy',): 0.7,
    ('Sunny', 'Cloudy'): 0.2,
    ('Sunny', 'Cloudy', 'Rainy'): 0.1
}

# Combine evidence
combined_mass, conflict = combine_evidence(m1, m2)

print(" Combined Mass Function:")
for k, v in combined_mass.items():
    print(f"{k}: {v:.4f}")
print(f"\n  Conflict (K): {conflict:.4f}")

# Calculate Belief and Plausibility for 'Cloudy'
hypothesis = {'Cloudy'}
bel = belief(combined_mass, hypothesis)
pl = plausibility(combined_mass, hypothesis)

print(f"\n  Belief (Cloudy): {bel:.4f}")
print(f"  Plausibility (Cloudy): {pl:.4f}")
