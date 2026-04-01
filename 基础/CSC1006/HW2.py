import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# =========================================================
# Q2(2): Plot out the Perceptron Decision Boundary
# =========================================================
def plot_q2_decision_boundary():
    x0 = np.linspace(-2, 4, 100)
    # the decision boundary equation: x1 = 0.5 * x0 - 0.5
    x1 = 0.5 * x0 - 0.5  
    
    plt.figure(figsize=(6, 4))
    plt.plot(x0, x1, '-r', label='Decision Boundary: $x_1 = 0.5x_0 - 0.5$')
    plt.scatter([3], [0], color='blue', label='(3, 0), $\hat{y}=+1$')
    plt.scatter([1], [1], color='green', label='(1, 1), $\hat{y}=-1$')
    
    plt.fill_between(x0, x1, y2=1.5, color='green', alpha=0.1, label='Class -1 Area')
    plt.fill_between(x0, x1, y2=-2.5, color='blue', alpha=0.1, label='Class +1 Area')
    
    plt.xlabel('$x_0$')
    plt.ylabel('$x_1$')
    plt.title('Q2: Perceptron Decision Boundary')
    plt.legend()
    plt.grid(True)
    plt.show()

# =========================================================
# Q3(2): Plot the Binary Cross Entropy Loss Function
# =========================================================
def plot_q3_bce_loss():
    # prevent evaluating log(0) explicitly
    y_hat = np.linspace(0.001, 0.999, 100) 
    loss_y1 = -np.log(y_hat)
    loss_y0 = -np.log(1 - y_hat)
    
    plt.figure(figsize=(6, 4))
    plt.plot(y_hat, loss_y1, label='$L(\hat{y})$ when True Label $y=1$', linewidth=2)
    plt.plot(y_hat, loss_y0, label='$L(\hat{y})$ when True Label $y=0$', linewidth=2, linestyle='--')
    
    plt.xlabel('Predicted Probability ($\hat{y}$)')
    plt.ylabel('BCE Loss Value')
    plt.title('Q3: Binary Cross Entropy Loss Function')
    plt.legend()
    plt.grid(True)
    plt.show()

# =========================================================
# Q4: Coding - Classify Different Types of Iris 
# =========================================================
def q4_iris_classification():
    # 0. Load Data
    X, y = load_iris(return_X_y=True)
    # transform label directly to binary classification 0 or 1 (whether it is Versicolour)
    y = (y == 1).astype(int)  

    # 1. 80-20 Train and Test split, apply stratify to keep class distribution intact
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 2. Build KNN model with k=3
    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(X_train, y_train)
    y_pred_knn = knn_model.predict(X_test)

    # 3. Build Logistic Regression Model
    lr_model = LogisticRegression(random_state=42, max_iter=200)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)

    # 4. Define local evaluation tool and log outputs
    def evaluate_model(name, y_true, y_pred):
        print(f"--- Model: {name} ---")
        print(f"Accuracy  : {accuracy_score(y_true, y_pred):.4f}")
        print(f"Precision : {precision_score(y_true, y_pred):.4f}")
        print(f"Recall    : {recall_score(y_true, y_pred):.4f}")
        print(f"F1-Score  : {f1_score(y_true, y_pred):.4f}")
        print()

    evaluate_model("KNN (k=3)", y_test, y_pred_knn)
    evaluate_model("Logistic Regression", y_test, y_pred_lr)

    # 5. Optional feature demonstration: Cross Validation searching for Opt-K
    print("--- Q4(5) Optional Task: finding best k using Cross Validation ---")
    # Utilizing 5-Fold validation methodology over the train batch
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    k_range = list(range(1, 21))
    param_grid = dict(n_neighbors=k_range)
    
    grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=cv, scoring='f1')
    grid.fit(X_train, y_train)
    
    print(f"Best K parameter from Grid Search  : {grid.best_params_['n_neighbors']}")
    print(f"Best cross-validated F1 Valid-Score: {grid.best_score_:.4f}")

# Execute everything by uncommenting the procedures below
if __name__ == "__main__":
    # plot_q2_decision_boundary()
    # plot_q3_bce_loss()
    q4_iris_classification()
