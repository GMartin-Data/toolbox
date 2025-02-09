from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def draw_confusion_matrix(clf, X, y_true) -> None:
    """Display a confusion matrix enhanced with a heatmap"""
    y_pred = clf.predict(X)
    cm = confusion_matrix(y_true, y_pred, labels=clf.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
    disp.plot(cmap="Blues")

    plt.title("Confusion Matrix", size="x-large", weight="bold", c="b")
    plt.show()


def display_feature_importances(task: str, X, y) -> None:
    """
    Display feature importances with a sum-up and barchart
    `task` is either "reg" for regression or "clf" for classification
    """
    if task == "reg":
        forest = RandomForestRegressor(n_estimators=500, random_state=0)
    elif task == "clf":
        forest = RandomForestClassifier(n_estimators=500, random_state=0)
    else:
        raise ValueError(f"task was expected to be 'reg' or 'clf', got {task}")

    feat_labels = X.columns
    forest.fit(X, y)
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.barh(range(X.shape[1]), importances[indices], align="center")
    plt.yticks(range(X.shape[1]), feat_labels[indices])
    plt.gca().invert_yaxis()

    for i in range(X.shape[1]):
        plt.text(
            importances[indices[i]], i, f"{importances[indices[i]]:.3f}", va="center"
        )
        plt.title("Feature Importance", size="x-large", c="b", weight="bold")
        plt.tight_layout()
        plt.show()


def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    """Convenience function to plot decision boundaries"""
    # Setting marker generator and color map
    markers = ("o", "s", "^", "v", "<")
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])

    # Plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(
        np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution)
    )
    lab = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    lab = lab.reshape(xx1.shape)
    plt.contourf(xx1, xx2, lab, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # Plot class examples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(
            x=X[y == cl, 0],
            y=X[y == cl, 1],
            alpha=0.8,
            c=colors[idx],
            marker=markers[idx],
            label=f"Class {cl}",
            edgecolor="black",
        )

    # Highlight test examples
    if test_idx:
        # Plot all examples
        X_test, y_test = X[test_idx, :], y[test_idx]

        plt.scatter(
            X_test[:, 0],
            X_test[:, 1],
            c="none",
            edgecolor="black",
            alpha=1.0,
            linewidth=1,
            marker="o",
            s=100,
            label="Test set",
        )
