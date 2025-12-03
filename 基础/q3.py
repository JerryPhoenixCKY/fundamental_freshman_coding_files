import numpy as np
from scipy.optimize import minimize

gens = [
    (0.02, 10, 100, 50, 150),
    (0.03, 8, 120, 50, 100),
    (0.025, 9, 150, 50, 120)
]

total_load = 300

def total_cost(P):
    cost = 0.0
    for i in range(3):
        a, b, c, _, _ = gens[i]
        cost += a * P[i]**2 + b * P[i] + c
    return cost

def power_balance(P):
    return np.sum(P) - total_load

constraint = {'type': 'eq', 'fun': power_balance}
bounds = [(50, 150), (50, 100), (50, 120)]
initial_guess = [100, 75, 125]

result = minimize(
    fun=total_cost,
    x0=initial_guess,
    bounds=bounds,
    constraints=[constraint],
    method='SLSQP'
)

P1, P2, P3 = result.x
total_cost_value = result.fun

print("Optimal Power Outputs:")
print(f"P1: <{int(round(P1))} in MW>")
print(f"P2: <{int(round(P2))} in MW>")
print(f"P3: <{int(round(P3))} in MW>")
print(f"Total Generation Cost: <${int(round(total_cost_value))}>")