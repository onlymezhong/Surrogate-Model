from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data, iris.target
y_true = [0, 1, 2, 3]
y_pred = [0, 2, 1, 3]

from sklearn.metrics import fbeta_score, make_scorer

ftwo_scorer = make_scorer(fbeta_score, beta=2)

from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC

grid = GridSearchCV(LinearSVC(), param_grid={'C': [1, 10]}, scoring=ftwo_scorer)
