from scipy.optimize import minimize


def f(x):
    return (x - 3) ** 2


res = minimize(f, x0=2)
print(res)
print(res.x)
