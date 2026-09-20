import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Membership functions for temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['comfortable'] = fuzz.trimf(temperature.universe, [15, 22, 30])
temperature['hot'] = fuzz.trimf(temperature.universe, [25, 40, 40])

# Membership functions for fan_speed
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 40])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(temperature['cold'], fan_speed['low'])
rule2 = ctrl.Rule(temperature['comfortable'], fan_speed['medium'])
rule3 = ctrl.Rule(temperature['hot'], fan_speed['high'])

# Create control system
fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
fan_simulation = ctrl.ControlSystemSimulation(fan_ctrl)

# Simulate for a specific temperature
fan_simulation.input['temperature'] = 28  # test input
fan_simulation.compute()

# Output result
print(f"Temperature: 28°C")
print(f"Recommended Fan Speed: {fan_simulation.output['fan_speed']:.2f}%")
