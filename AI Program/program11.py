# Semantic Network Representation and Query System
class SemanticNetwork:
    def __init__(self):
        self.network = {}
        self.properties = {}
    def add_relation(self, subject, relation, obj):
        """Add a relationship like Fido --eats--> Whiskers"""
        if subject not in self.network:
            self.network[subject] = []
        self.network[subject].append((relation, obj))
    def add_property(self, entity, category, attributes):
        """Add attributes and category info to an entity"""
        self.properties[entity] = {"category": category, "attributes": attributes}
    def get_relations(self, subject):
        """Return all relationships of a subject"""
        if subject not in self.network:
            return []
        rels = [f"{subject} --{r}--> {o}" for (r, o) in self.network[subject]]
        return rels
    def query_relation(self, subject, relation):
        """Find who subject has a given relation with"""
        if subject not in self.network:
            return []
        return [o for (r, o) in self.network[subject] if r == relation]
    def find_who_relates(self, relation, obj):
        """Find who has a specific relation with the object"""
        result = []
        for subject, rels in self.network.items():
            for (r, o) in rels:
                if r == relation and o == obj:
                    result.append(subject)
        return result
    def relationship_between(self, subj, obj):
        """Find what relationship exists between two entities"""
        if subj not in self.network:
            return []
        return [r for (r, o) in self.network[subj] if o == obj]
    def is_a_relations(self):
        """Return all 'is_a' type relationships"""
        result = []
        for s, rels in self.network.items():
            for (r, o) in rels:
                if r == "is_a":
                    result.append(f"{s} --is_a--> {o}")
        return result
    def check_is_a(self, subj, obj):
        """Check if subj is a kind of obj"""
        visited = set()
        def dfs(current):
            if current == obj:
                return True
            visited.add(current)
            for (r, o) in self.network.get(current, []):
                if r == "is_a" and o not in visited:
                    if dfs(o):
                        return True
            return False
        return dfs(subj)
    def get_properties(self, entity):
        """Return entity properties"""
        return self.properties.get(entity, {})
# MAIN PROGRAM 
sn = SemanticNetwork()
# Build a small domain
sn.add_relation("Mammal", "is_a", "Animal")
sn.add_relation("Bird", "is_a", "Animal")
sn.add_relation("Fish", "is_a", "Animal")
sn.add_relation("Fido", "is_a", "Mammal")
sn.add_relation("Whiskers", "is_a", "Mammal")
sn.add_relation("Tweety", "is_a", "Bird")
sn.add_relation("Nemo", "is_a", "Fish")
# Add other relationships
sn.add_relation("Fido", "eats", "Whiskers")
sn.add_relation("Fido", "loves", "Tweety")
sn.add_relation("Tweety", "fears", "Whiskers")
# Add properties
sn.add_property("Fido", "Instance", {"legs": 4, "color": "brown"})
#SAMPLE OUTPUT
print("All relationships of Fido:")
print(sn.get_relations("Fido"))
print()
print("Who does Fido love?")
print(sn.query_relation("Fido", "loves"))
print()
print("Who fears Whiskers?")
print(sn.find_who_relates("fears", "Whiskers"))
print()
print("Relationship between Fido and Whiskers:")
print(sn.relationship_between("Fido", "Whiskers"))
print()
print("All 'is_a' relationships:")
print(sn.is_a_relations())
print()
print("Is Fido an Animal?")
print(sn.check_is_a("Fido", "Animal"))
print()
print("Properties of Fido:")
print(sn.get_properties("Fido"))
