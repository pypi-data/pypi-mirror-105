

default_search_space_dict = dict()



xgboost_regressor_search_space = {'learning_rate_multiplier': [(0.5, 10), 'real', 'uniform'],
										 'gamma': [(0, 5), 'real', 'uniform'],
										 'max_depth': [(2, 20), 'discrete'],
										 'n_estimators': [(10, 1250), 'discrete'],
										 'min_child_weight': [(1, 50), 'discrete'],
										 'colsample_bytree': [(0.1, 1), 'real', 'uniform'],
										 'subsample': [(0.1, 1), 'real', 'uniform'],
										 'reg_alpha': [(0, 1), 'real', 'loguniform'],
										 'reg_lambda': [(1, 5), 'real', 'loguniform']}

xgboost_regressor_search_space_str = \
"""
{'learning_rate_multiplier': [(0.5, 10), 'real', 'uniform'],
 'gamma': [(0, 5), 'real', 'uniform'],
 'max_depth': [(2, 20), 'discrete'],
 'n_estimators': [(10, 1250), 'discrete'],
 'min_child_weight': [(1, 50), 'discrete'],
 'colsample_bytree': [(0.1, 1), 'real', 'uniform'],
 'subsample': [(0.1, 1), 'real', 'uniform'],
 'reg_alpha': [(0, 1), 'real', 'loguniform'],
 'reg_lambda': [(1, 5), 'real', 'loguniform']}"""

default_search_space_dict['xgboost_regressor'] = [xgboost_regressor_search_space, xgboost_regressor_search_space_str]


tiny_xgboost_regressor_search_space = {'learning_rate_multiplier': [(0.5, 10), 'real', 'uniform'],
										 'gamma': [(0, 5), 'real', 'uniform'],
										 'max_depth': [(2, 3), 'discrete'],
										 'n_estimators': [(10, 25), 'discrete'],
										 'min_child_weight': [(1, 50), 'discrete'],
										 'colsample_bytree': [(0.1, 1), 'real', 'uniform'],
										 'subsample': [(0.1, 1), 'real', 'uniform'],
										 'reg_alpha': [(0, 1), 'real', 'loguniform'],
										 'reg_lambda': [(1, 5), 'real', 'loguniform']}

tiny_xgboost_regressor_search_space_str = \
"""
{'learning_rate_multiplier': [(0.5, 10), 'real', 'uniform'],
 'gamma': [(0, 5), 'real', 'uniform'],
 'max_depth': [(2, 3), 'discrete'],
 'n_estimators': [(10, 25), 'discrete'],
 'min_child_weight': [(1, 50), 'discrete'],
 'colsample_bytree': [(0.1, 1), 'real', 'uniform'],
 'subsample': [(0.1, 1), 'real', 'uniform'],
 'reg_alpha': [(0, 1), 'real', 'loguniform'],
 'reg_lambda': [(1, 5), 'real', 'loguniform']}"""

default_search_space_dict['tiny_xgboost_regressor'] = [tiny_xgboost_regressor_search_space, tiny_xgboost_regressor_search_space_str]


sklearn_random_forest_regressor_search_space = {'n_estimators': [(50, 950), 'discrete'],
						                        'max_depth': [(2, 20), 'discrete'],
						                        'min_samples_split': [(2, 50), 'discrete'],
						                        'min_samples_leaf': [(1, 50), 'discrete'],
						                        'max_features': [('auto', 'sqrt', 'log2'), 'choice'],
						                        'bootstrap': [(True, False), 'choice']}

sklearn_random_forest_regressor_search_space_str = \
"""
{'n_estimators': [(50, 950), 'discrete'],
 'max_depth': [(2, 20), 'discrete'],
 'min_samples_split': [(2, 50), 'discrete'],
 'min_samples_leaf': [(1, 50), 'discrete'],
 'max_features': [('auto', 'sqrt', 'log2'), 'choice'],
 'bootstrap': [(True, False), 'choice']}"""

default_search_space_dict['sklearn_random_forest_regressor'] = [sklearn_random_forest_regressor_search_space, sklearn_random_forest_regressor_search_space_str]


lightgbm_regressor_eval_method_search_space = {'num_boost_round': [(10, 950), 'discrete'],
								               'num_leaves': [(10, 150), 'discrete'],
								               'lambda_l1': [(1e-8, 10), 'real', 'loguniform'],
								               'lambda_l2': [(1e-8, 10), 'real', 'loguniform'],
								               'bagging_freq': [(2, 9), 'discrete'],
								               'bagging_fraction': [(0.4, 1.0), 'real', 'uniform'],
								               'min_data_in_leaf': [(15, 100), 'discrete'],
								               'learning_rate': [(0.05, 0.25), 'real', 'loguniform']}

lightgbm_regressor_eval_method_search_space_str = \
"""
{'num_boost_round': [(10, 950), 'discrete'],
'num_leaves': [(10, 150), 'discrete'],
'lambda_l1': [(1e-8, 10), 'real', 'loguniform'],
'lambda_l2': [(1e-8, 10), 'real', 'loguniform'],
'bagging_freq': [(2, 9), 'discrete'],
'bagging_fraction': [(0.4, 1.0), 'real', 'uniform'],
'min_data_in_leaf': [(15, 100), 'discrete'],
'learning_rate': [(0.05, 0.25), 'real', 'loguniform']}"""

default_search_space_dict['lightgbm_regressor_eval_method'] = [lightgbm_regressor_eval_method_search_space, lightgbm_regressor_eval_method_search_space_str]




















