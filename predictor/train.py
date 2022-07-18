import joblib
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)
logger.info("Loading input and output data")
inputs = pd.read_csv("../data/inputs.csv")
outputs = pd.read_csv("../data/outputs.csv")
X_train, X_test, y_train, y_test = train_test_split(
    inputs, outputs, test_size=0.4, random_state=23
)
print(X_train.to_numpy())
print("="*80)
print(y_train.to_numpy().ravel())
logger.info("Create model (tuned hyperparams)")
clf = RandomForestClassifier(
    max_depth=8,
    max_leaf_nodes=64,
    max_samples=0.5,
    n_estimators=10,
    verbose=True,
    n_jobs=-1,
)

pipeline = Pipeline([('clf', clf)])

logger.info("Fitting pipeline")
pipeline.fit(X_train.to_numpy(), y_train.to_numpy().ravel())

logger.info("Saving joblib model")
joblib.dump(pipeline, 'model.joblib')
