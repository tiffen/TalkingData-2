import time
import gc
import numpy as np
import pandas as pd
# sklearn imports
from sklearn.metrics.scorer import roc_auc_scorer, roc_auc_score
from sklearn.model_selection import train_test_split
import lightgbm
# gravity imports
import gravity_learn.utils as gu

# read data
df_train = pd.read_hdf('./input/train_v6.3_new.hdf').astype('float32')
gc.collect()
# col
target = 'is_attributed'
features = [
    'app',
    'device',
    'os',
    'channel',
    'hour',
    'in_test_hh',
    'ip_day_hour_clicks',
    'ip_app_day_hour_clicks',
    'ip_os_day_hour_clicks',
    'ip_device_day_hour_clicks',
    'ip_day_test_hh_clicks',
    'ip_app_device_clicks',
    'ip_app_device_day_clicks',
    'ip_day_nunique_app',
    'ip_day_nunique_device',
    'ip_day_nunique_channel',
    'ip_day_nunique_hour',
    'ip_nunique_app',
    'ip_nunique_device',
    'ip_nunique_channel',
    'ip_nunique_hour',
    'app_day_nunique_channel',
    'app_nunique_channel',
    'ip_app_day_nunique_os',
    'ip_app_nunique_os',
    'ip_device_os_day_nunique_app',
    'ip_device_os_nunique_app',
    'ip_app_day_var_hour',
    'ip_device_day_var_hour',
    'ip_os_day_var_hour',
    'ip_channel_day_var_hour',
    'ip_app_os_var_hour',
    'ip_app_channel_var_day',
    'ip_app_channel_mean_hour',
    'ip_day_cumcount',
    'ip_cumcount',
    'ip_app_day_cumcount',
    'ip_app_cumcount',
    'ip_device_os_day_cumcount',
    'ip_device_os_cumcount',
    'next_click',
    'previous_click',
]
# categorical
categorical_features = [
    'app',
    'device',
    'os',
    'channel',
    'hour',
    'in_test_hh',
]
# prep data
dtrain = lightgbm.Dataset(
    df_train[features].values,
    label=df_train[target].values,
    feature_name=features,
    categorical_feature=categorical_features,
    free_raw_data=True,
)
del df_train
gc.collect()
print('done data prep!!!')

t0 = time.time()
###################################################################
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.03,
    'num_leaves': 32,
    'max_depth': 6,
    'min_split_gain': 0,
    'subsample': 0.9,
    'subsample_freq': 1,
    'colsample_bytree': 0.9,
    'min_child_samples': 100,
    'min_child_weight': 0,
    'max_bin': 100,
    'subsample_for_bin': 200000,
    'reg_alpha': 0,
    'reg_lambda': 0,
    'scale_pos_weight': 100,
    'metric': 'auc',
    'nthread': 22,
    'verbose': 0,
}
# train
model = lightgbm.train(
    params=params,
    train_set=dtrain,
    num_boost_round=1880,
    feature_name=features,
    categorical_feature=categorical_features,
    verbose_eval=1,
#     init_model='model_lgb_0.01_4000_64_8_0.7_v6.2.txt'
)
####################################################################
t1 = time.time()
t_min = np.round((t1-t0) / 60, 2)
print('It took {} mins to train model'.format(t_min))
# save model
# model.save_model('model_lgb_0.03_5000_64_8_0.7_v6.3.txt')
# clean up
# del model
gc.collect()
####################################################################
# submit
df_test = pd.read_hdf('./input/test_v6.3_new.hdf')
# pred
df_test['is_attributed'] = model.predict(df_test[features])
# create submission
sub_cols = ['click_id', 'is_attributed']
df_sub = df_test[sub_cols]
# save
df_sub.to_csv('./input/lightGBM_v6.3_0.03_32_6_0.9_1880.csv', index=False)
del model, df_test, df_sub
gc.collect()



dtrain.set_init_score(None)
dtrain.set_weight(None)
t0 = time.time()
###################################################################
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.03,
    'num_leaves': 32,
    'max_depth': 6,
    'min_split_gain': 0,
    'subsample': 0.9,
    'subsample_freq': 1,
    'colsample_bytree': 0.9,
    'min_child_samples': 100,
    'min_child_weight': 0,
    'max_bin': 100,
    'subsample_for_bin': 200000,
    'reg_alpha': 0,
    'reg_lambda': 0,
    'scale_pos_weight': 100,
    'metric': 'auc',
    'nthread': 22,
    'verbose': 0,
}
# train
model = lightgbm.train(
    params=params,
    train_set=dtrain,
    num_boost_round=2000,
    feature_name=features,
    categorical_feature=categorical_features,
    verbose_eval=1,
#     init_model='model_lgb_0.01_4000_64_8_0.7_v6.2.txt'
)
####################################################################
t1 = time.time()
t_min = np.round((t1-t0) / 60, 2)
print('It took {} mins to train model'.format(t_min))
# save model
# model.save_model('model_lgb_0.03_5000_64_8_0.7_v6.3.txt')
# clean up
# del model
gc.collect()
####################################################################
# submit
df_test = pd.read_hdf('./input/test_v6.3_new.hdf')
# pred
df_test['is_attributed'] = model.predict(df_test[features])
# create submission
sub_cols = ['click_id', 'is_attributed']
df_sub = df_test[sub_cols]
# save
df_sub.to_csv('./input/lightGBM_v6.3_0.03_32_6_0.9_2000.csv', index=False)
del model, df_test, df_sub
gc.collect()



dtrain.set_init_score(None)
dtrain.set_weight(None)
t0 = time.time()
###################################################################
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.03,
    'num_leaves': 32,
    'max_depth': 6,
    'min_split_gain': 0,
    'subsample': 0.9,
    'subsample_freq': 1,
    'colsample_bytree': 0.9,
    'min_child_samples': 100,
    'min_child_weight': 0,
    'max_bin': 100,
    'subsample_for_bin': 200000,
    'reg_alpha': 0,
    'reg_lambda': 0,
    'scale_pos_weight': 100,
    'metric': 'auc',
    'nthread': 22,
    'verbose': 0,
}
# train
model = lightgbm.train(
    params=params,
    train_set=dtrain,
    num_boost_round=2200,
    feature_name=features,
    categorical_feature=categorical_features,
    verbose_eval=1,
#     init_model='model_lgb_0.01_4000_64_8_0.7_v6.2.txt'
)
####################################################################
t1 = time.time()
t_min = np.round((t1-t0) / 60, 2)
print('It took {} mins to train model'.format(t_min))
# save model
# model.save_model('model_lgb_0.03_5000_64_8_0.7_v6.3.txt')
# clean up
# del model
gc.collect()
####################################################################
# submit
df_test = pd.read_hdf('./input/test_v6.3_new.hdf')
# pred
df_test['is_attributed'] = model.predict(df_test[features])
# create submission
sub_cols = ['click_id', 'is_attributed']
df_sub = df_test[sub_cols]
# save
df_sub.to_csv('./input/lightGBM_v6.3_0.03_32_6_0.9_2200.csv', index=False)
del model, df_test, df_sub
gc.collect()



dtrain.set_init_score(None)
dtrain.set_weight(None)
t0 = time.time()
###################################################################
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.03,
    'num_leaves': 32,
    'max_depth': 6,
    'min_split_gain': 0,
    'subsample': 0.9,
    'subsample_freq': 1,
    'colsample_bytree': 0.9,
    'min_child_samples': 100,
    'min_child_weight': 0,
    'max_bin': 100,
    'subsample_for_bin': 200000,
    'reg_alpha': 0,
    'reg_lambda': 0,
    'scale_pos_weight': 100,
    'metric': 'auc',
    'nthread': 22,
    'verbose': 0,
}
# train
model = lightgbm.train(
    params=params,
    train_set=dtrain,
    num_boost_round=2400,
    feature_name=features,
    categorical_feature=categorical_features,
    verbose_eval=1,
#     init_model='model_lgb_0.01_4000_64_8_0.7_v6.2.txt'
)
####################################################################
t1 = time.time()
t_min = np.round((t1-t0) / 60, 2)
print('It took {} mins to train model'.format(t_min))
# save model
# model.save_model('model_lgb_0.03_5000_64_8_0.7_v6.3.txt')
# clean up
# del model
gc.collect()
####################################################################
# submit
df_test = pd.read_hdf('./input/test_v6.3_new.hdf')
# pred
df_test['is_attributed'] = model.predict(df_test[features])
# create submission
sub_cols = ['click_id', 'is_attributed']
df_sub = df_test[sub_cols]
# save
df_sub.to_csv('./input/lightGBM_v6.3_0.03_32_6_0.9_2400.csv', index=False)
del model, df_test, df_sub
gc.collect()