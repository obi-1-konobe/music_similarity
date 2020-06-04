import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import NearestNeighbors
import pickle
import random
import math
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn.svm import SVR, SVC
from sklearn.metrics import classification_report
from sklearn.metrics.pairwise import cosine_similarity


with open('../data/pickles/main_dict.pickle', 'rb') as f:
    main_dict = pickle.load(f)

df_train = pd.read_csv('../data/csv/train_2.csv', index_col=0)
df_test = pd.read_csv('../data/csv/test_2.csv', index_col=0)

# df_train = df_train.drop(df_train.columns[1:553], axis=1)
# df_test = df_test.drop(df_test.columns[1:553], axis=1)

features_train = df_train.drop(['file'], 1)
features_test = df_test.drop(['file'], 1)

scaler = StandardScaler()
scaler.fit(features_train)
X_train = scaler.transform(features_train)
X_test = scaler.transform(features_test)

# pca = PCA(0.95)
# pca.fit(X_train)
# X_train = pca.transform(X_train)
# X_test = pca.transform(X_test)

with open('../data/tags_similarity.txt', 'r') as f:
    data = f.readlines()

all_similarity = [x.strip('\n').split() for x in data]
df_train_2 = df_train.reset_index(drop=True)

models = {
    # 'GBR': {
    #     'model': GradientBoostingRegressor(),
    #     'params': {
    #         'loss': ['ls', 'lad', 'huber', 'quantile'],
    #         'learning_rate': [0.001, 0.01, 0.1],
    #         'n_estimators': np.arange(80, 200),
    #         'subsample': np.arange(0.6, 1.01, 0.1),
    #         #             'min_samples_split': np.arange(20, 70),
    #         #             'min_samples_leaf': np.arange(0.1, .51, 0.1),
    #         'max_features': np.arange(0.1, 1.01, 0.1),
    #         'max_depth': np.arange(3, 7)
    #
    #     }
    # },
    # 'LinReg': {
    #     'model': LinearRegression(),
    #     'params': {}
    # },
    'LGBMR': {
        'model': LGBMRegressor(),
        'params': {
            'boosting_type': ['gbdt', 'dart', 'goss'],
            'max_depth': np.arange(3, 9),
            'learning_rate': [0.001, 0.01, 0.1],
            'n_estimators': np.arange(80, 200),
            'subsample': np.arange(0.6, 1.01, 0.1),
            'min_split_gain': np.arange(0.1, 1.01, 0.1),
            'min_child_weight': np.arange(0.1, 1.01, 0.1),
            'reg_alpha': np.arange(0.1, 1.01, 0.1),
            'reg_lambda': np.arange(0.1, 1.01, 0.1),

        }
    },
    # 'SVR': {
    #     'model': SVR(),
    #     'params': {
    #         'kernel': ['rbf', 'linear', 'sigmoid', 'poly'],
    #         'C': np.arange(0.1, 1.01, 0.1),
    #         'epsilon': np.arange(0.1, 1.01, 0.1),
    #         'shrinking': np.arange(0.1, 1.01, 0.1),
    #         'max_iter': [1000]
    #     }
    # }
}
features = list()
target = list()
for tupple in all_similarity:
    idx_1 = df_train_2[df_train_2.file == tupple[0]].index[0]
    idx_2 = df_train_2[df_train_2.file == tupple[1]].index[0]
    arr_1 = X_train[idx_1]
    arr_2 = X_train[idx_2]
    combo = np.hstack((arr_1, arr_2))
    features.append(combo)
    target.append(float(tupple[2]))

features_train, features_test, target_train, target_test = train_test_split(
    features,
    target,
    random_state=123
)


for model_name in models.keys():
    model = models[model_name]['model']
    params = models[model_name]['params']
    r_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=params,
        n_iter=50,
        scoring='neg_root_mean_squared_error',
        n_jobs=-1,
        random_state=123,
        error_score='raise'
    )
    r_search.fit(features_train, target_train)
    y_pred_train = r_search.predict(features_train)
    y_pred_test = r_search.predict(features_test)
    rmse_train = mean_squared_error(target_train, y_pred_train)
    rmse_test = mean_squared_error(target_test, y_pred_test)
    r2_train = r2_score(target_train, y_pred_train)
    r2_test = r2_score(target_test, y_pred_test)
    print(model)
    print(r_search.best_params_)
#     print(classification_report(target_train, y_pred_train))
#     print(classification_report(target_test, y_pred_test))
    print(f'rmse {rmse_train}/{rmse_test} r2 {r2_train}/{r2_test}')