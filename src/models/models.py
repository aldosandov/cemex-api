from sklearn.svm import SVR 
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing._data import StandardScaler
import numpy as np
import os
from joblib import load
from .errors import *


cwd = os.path.dirname(os.path.realpath(__file__)) + '/persistence/'


def scaler(hardness, prod_rate, quality, inverse=False):
    s_scaler = load(cwd + 'Scaling/SS.pkl')

    if inverse:
        data = s_scaler.inverse_transform([[hardness, prod_rate, 0, 0, quality, 0, 0, 0, 0]])
        return [data[0][0], data[0][1], data[0][4]]
    else: 
        data = s_scaler.transform([[hardness, prod_rate, 0, 0, quality, 0, 0, 0, 0]])
        return np.array([[data[0][0], data[0][1], data[0][4]]])


def make_clustering(x):
    clustering = load(cwd + 'Clustering/Agg.pkl')
    #tmp = clustering.predict(x)
    return 4


def predict_cm(x, cluster):
    svr = load(cwd + f'C{cluster}/SVR_C{cluster}.pkl')
    rf = load(cwd + f'C{cluster}/RF_C{cluster}.pkl')
    try:
        data = make_pred_dict(x, svr, rf, mse, cluster)
        return data
    except Exception as e:
        return {"message": str(e)}


def predict_cm_95(x, cluster):
    svr = load(cwd + f'C{cluster}_95/SVR_C{cluster}_95.pkl')
    rf = load(cwd + f'C{cluster}_95/RF_C{cluster}_95.pkl')
    try:
        data = make_pred_dict(x, svr, rf, mse_95, cluster)
        return data
    except Exception as e:
        return {"message": str(e)}


def predict_cmg(x):
    svr = load(cwd + 'DF/SVR_DF.pkl')
    rf = load(cwd + 'DF/RF_DF.pkl')
    try:
        data = make_pred_dict(x, svr, rf, mse, 6)
        return data
    except Exception as e:
        return {"message": str(e)}


def predict_cmg_95(x):
    svr = load(cwd + 'DF_95/SVR_DF_95.pkl')
    rf = load(cwd + 'DF_95/RF_DF_95.pkl')
    try:
        data = make_pred_dict(x, svr, rf, mse_95, 6)
        return data
    except Exception as e:
        return {"message": str(e)}


def make_pred_dict(x, svr, rf, error, cluster):
    tmp_svr = svr.predict(x)[0]
    tmp_rf = rf.predict(x)[0]
    data_svr = scaler(tmp_svr[0], tmp_svr[1], tmp_svr[2], True)
    data_rf =  scaler(tmp_rf[0], tmp_rf[1], tmp_rf[2], True)
    data_mse = error[str(cluster)]
    
    response = {
        "SVR": {
            "EE_TP": data_svr[0],
            "EC_TP": data_svr[1],
            "COSTO_TP": data_svr[2],
            "mse_interval": {
                "EE_TP": data_mse["SVR"]["EE_TP"],
                "EC_TP": data_mse["SVR"]["EC_TP"],
                "COSTO_TP": data_mse["SVR"]["COSTO_TP"]
            }
        },
        "RF":{
            "EE_TP": data_rf[0],
            "EC_TP": data_rf[1],
            "COSTO_TP": data_rf[2],
            "mse_interval": {
                "EE_TP": data_mse["RF"]["EE_TP"],
                "EC_TP": data_mse["RF"]["EC_TP"],
                "COSTO_TP": data_mse["RF"]["COSTO_TP"]
            }
        }
    }

    return response


"""if __name__ == "__main__":
    
    #print(type(scaler), type(clustering))
    #x = scaler(100, 99, 0.035)
    #cluster = make_clustering(x)
    print(mse_95)
    #y = predict_cm(x, cluster)
    #print(y)"""