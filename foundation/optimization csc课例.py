import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Define the objective function
f = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2

# Define inequality constraints
cons = (
    {'type': 'ineq', 'fun': lambda x: x[0] - 2 * x[1] + 2},     # x - 2y + 2 >= 0
    {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},    # -x - 2y + 6 >= 0
    {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2}     # -x + 2y + 2 >= 0
)

# Bounds: x >= 0, y >= 0
bnds = ((0, None), (0, None))

# Solve the optimization problem
res = minimize(f, (2, 0), bounds=bnds, constraints=cons)

# Create a grid of points for plotting
x = np.linspace(-1, 7, 200)
y = np.linspace(-1, 7, 200)
X, Y = np.meshgrid(x, y)

# Feasible region defined by constraints
c1 = X - 2*Y + 2 >= 0
c2 = -X - 2*Y + 6 >= 0
c3 = -X + 2*Y + 2 >= 0
c4 = X >= 0
c5 = Y >= 0
feasible = c1 & c2 & c3 & c4 & c5

# Plotting
plt.figure(figsize=(10, 8))
plt.imshow(feasible, extent=[-1, 7, -1, 7], origin='lower', alpha=0.3, cmap='Greens')

# Plot constraint lines
plt.plot(x, (x + 2)/2, 'r--', label='x - 2y + 2 = 0')
plt.plot(x, (-x + 6)/2, 'g--', label='-x - 2y + 6 = 0')
plt.plot(x, (x - 2)/2, 'b--', label='-x + 2y + 2 = 0')

# Plot optimal point
if res.success:
    optimal_x = res.x
    plt.plot(optimal_x[0], optimal_x[1], 'r*', markersize=15, label='Optimal Point')
else:
    print("Optimization failed.")

# Final formatting
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Feasible Region and Optimal Solution (Nonlinear)')
plt.legend()
plt.show()


# Differential Equation using solve_ivp
from scipy.integrate import solve_ivp
# Define the ODE: dv/dt = 3*v^2 - 5
def dvdt(t, v):
    return 3*v**2 - 5

# Initial condition
v0 = [0]

# Time span for integration
t_span = (0, 10)

# Time points where solution is evaluated
t_eval = np.linspace(0, 10, 10000)

# Solve the ODE
sol = solve_ivp(dvdt, t_span, v0, t_eval=t_eval)

# Extract results
t_result = sol.t
v_result = sol.y[0]  # First (and only) component of y

# Plot the solution
plt.plot(t_result, v_result)
plt.xlabel('t')
plt.ylabel('v')
plt.title('Solution using solve_ivp')
plt.grid(True)
plt.show()
#####################################################################################3
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# 读取数据
file_path = 'data.csv'
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date'])  # 将日期列转换为 datetime 类型
data.set_index('date', inplace=True)         # 设置日期为索引
load_data = data['load']                     # 提取 'load' 列作为目标变量

# 分割训练集和测试集（80% 训练，20% 测试）
train_size = int(len(load_data) * 0.8)
train_data, test_data = load_data[:train_size], load_data[train_size:]

# 构建 ARIMA 模型
model = ARIMA(train_data, order=(20, 1, 5))  # p=20, d=1, q=5
arima_model = model.fit()                   # 拟合模型

# 在测试集上做预测
predictions = arima_model.forecast(steps=len(test_data))

# 绘制预测结果图
plt.figure(figsize=(10, 6))
plt.plot(test_data.index, test_data, label='Actual Load')           # 实际值
plt.plot(test_data.index, predictions, label='Predicted Load', color='red')  # 预测值
plt.legend(fontsize=15)
plt.xlabel('Date', fontsize=15)
plt.ylabel('Load', fontsize=15)
plt.title('Load Prediction using ARIMA', fontsize=15)
plt.grid(True)
plt.tight_layout()
plt.savefig('arima_forecast.pdf')  # 保存图像
plt.show()




