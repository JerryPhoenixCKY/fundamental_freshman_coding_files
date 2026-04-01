import numpy as np
from sklearn.linear_model import LinearRegression

X_array = np.array([1.19154063, 1.37434891, 1.17195486, 0.16152634, 0.79415049, 1.72423116,
                    1.9907262, 0.2851336, 1.78185502, 1.2749914, 1.35433286, 0.37991704,
                    1.86381926, 0.14110919, 0.4916442, 0.08485453, 1.40743255, 1.8189095,
                    0.79861128, 0.91450109])
Y_array = np.array([7.25283192, 7.4995625, 8.84322609, 3.94706203, 6.65112617, 8.23952238,
                    10.00317942, 3.19168625, 10.03715158, 7.27914416, 8.66561184, 3.73632541,
                    9.58035831, 3.99475623, 5.84385689, 3.19935995, 8.69952762, 8.48467547,
                    6.81720262, 6.05033212])
X = X_array.reshape(-1, 1)
Y = Y_array.reshape(-1, 1)

model = LinearRegression()
model.fit(X, Y)

velocity = model.coef_[0][0]
displacement = model.intercept_[0]

print("Q11 Results:")
print(f"Velocity (w): {velocity:.4f} km/h")
print(f"Starting Displacement (b): {displacement:.4f} km")



