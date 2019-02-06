import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectPercentile, f_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from xgboost import XGBRegressor

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=None)

# Average CV score on the training set was:-5.552160248706523
exported_pipeline = make_pipeline(
    SelectPercentile(score_func=f_regression, percentile=86),
    StackingEstimator(estimator=XGBRegressor(learning_rate=0.1, max_depth=5, min_child_weight=20, n_estimators=100, nthread=1, subsample=0.6500000000000001)),
    RandomForestRegressor(bootstrap=False, max_features=0.1, min_samples_leaf=2, min_samples_split=12, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
