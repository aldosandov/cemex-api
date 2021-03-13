from sklearn.svm import SVR 
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing._data import StandardScaler
import numpy as np
from os import getcwd
from joblib import load
#from mse import *


cwd = getcwd() + '/src/models/persistence/'


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
    return 1


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



mse = {
    "1": {
        "SVR": {
            "EE_TP": [0.47309497454290295, 0.6529189746067385],
            "EC_TP": [0.8374681091040123, 0.9269201168691027],
            "COSTO_TP": [0.4730949745428932, 0.6529189746067281]
        },
        "RF": {
            "EE_TP": [0.5957400765524125, 0.7812476913851661],
            "EC_TP": [0.966867355459585, 1.1133521696916033],
            "COSTO_TP": [0.5957400765524122, 0.7812476913851659]
        }
    }, 
    "2": {
        "SVR": {
            "EE_TP": [0.31920399778231767, 0.7211151418018072],
            "EC_TP": [0.559199768207611, 1.0853160888555462],
            "COSTO_TP": [0.31920399778231756, 0.7211151418018067]
        },
        "RF": {
            "EE_TP": [0.4206507419723272, 0.7996094947102049],
            "EC_TP": [0.7489782275879502, 1.3238845966580424],
            "COSTO_TP": [0.4206507419723271, 0.7996094947102046]
        }
    },
    "3": {
        "SVR": {
            "EE_TP": [0.155142484209383, 0.23922761377784554],
            "EC_TP": [0.7966697319425813, 1.0419342847742143],
            "COSTO_TP": [0.15514248420938423, 0.239227613777845]
        },
        "RF": {
            "EE_TP": [0.1941988331361704, 0.27361237096992375],
            "EC_TP": [0.9184414882070701, 1.1335636393059803],
            "COSTO_TP": [0.19419883313617026, 0.27361237096992364]
        }
    },
    "4": {
        "SVR": {
            "EE_TP": [0.46420939123201055, 0.8906427164227321],
            "EC_TP": [1.034979560031072, 1.244593421590519],
            "COSTO_TP": [0.4642093912320096, 0.8906427164227269]
        },
        "RF": {
            "EE_TP": [0.5662261841665852, 0.8938051803465281],
            "EC_TP": [1.1643400582984433, 1.4810299555580075],
            "COSTO_TP": [0.5662261841665852, 0.8938051803465281]
        }
    },
    "5": {
        "SVR": {
            "EE_TP": [0.3959291440202342, 0.5009720377448634],
            "EC_TP": [0.7672654060778321, 0.9185749584578229],
            "COSTO_TP": [0.39592914402023127, 0.5009720377448628]
        },
        "RF": {
            "EE_TP": [0.487613902047299, 0.5635176111370243],
            "EC_TP": [0.9485883168508641, 1.140638297549971],
            "COSTO_TP": [0.4876139020472989, 0.5635176111370241]
        }
    },
    "6": {
        "SVR": {
            "EE_TP": [0.4962125135907768, 0.5333855698532585],
            "EC_TP": [0.925209932346431, 1.0226742485116396],
            "COSTO_TP": [0.4962125135930522, 0.5333855698546388]
        },
        "RF": {
            "EE_TP": [0.5676674856183385, 0.6187171120548968],
            "EC_TP": [1.0873585664660408, 1.2188150947652794],
            "COSTO_TP": [0.567667485618338, 0.6187171120548963]
        }
    }
}

mse_95 = {
    "1": {
        "SVR": {
            "EE_TP": [0.46389801772725203, 0.5988461073670834],
            "EC_TP": [0.8006838394156779, 0.9397799049147946],
            "COSTO_TP": [0.4638980177272525, 0.5988461073670832]
        },
        "RF": {
            "EE_TP": [0.5866333455174619, 0.696811936790247],
            "EC_TP": [0.9829736609909774, 1.0993716732153698],
            "COSTO_TP": [0.5866333455174619, 0.6968119367902468]
        }
    }, 
    "2": {
        "SVR": {
            "EE_TP": [0.3741539270029378, 0.8107840638408689],
            "EC_TP": [0.9395962981278642, 1.3597593007372388],
            "COSTO_TP": [0.3741539270029375, 0.8107840638408685]
        },
        "RF": {
            "EE_TP": [0.47536782288153, 0.7036881812733139],
            "EC_TP": [0.9436666949523788, 1.5870483354066294],
            "COSTO_TP": [0.4753678228815298, 0.7036881812733135]
        }
    },
    "3": {
        "SVR": {
            "EE_TP": [0.15452582854574495, 0.23767905615650917],
            "EC_TP": [0.7709408958566064, 0.9604112699173781],
            "COSTO_TP": [0.15452582854574476, 0.23767905615652118]
        },
        "RF": {
            "EE_TP": [0.18045377672163818, 0.2530995492083461],
            "EC_TP": [0.8330195385409689, 1.0752275310499604],
            "COSTO_TP": [0.1804537767216381, 0.253099549208346]
        }
    },
    "4": {
        "SVR": {
            "EE_TP": [0.5189011167202074, 0.682624306935446],
            "EC_TP": [0.9119940276028051, 1.3748402149318737],
            "COSTO_TP": [0.5189011167202129, 0.6826243069354361]
        },
        "RF": {
            "EE_TP": [0.5830195075585967, 0.7751497204435003],
            "EC_TP": [1.050303221628395, 1.5757244146432663],
            "COSTO_TP": [0.5830195075585961, 0.7751497204434997]
        }
    },
    "5": {
        "SVR": {
            "EE_TP": [0.42793458802200207, 0.5355296223737378],
            "EC_TP": [0.7365132064666229, 0.9062817114044899],
            "COSTO_TP": [0.4279345880220016, 0.5355296223737323]
        },
        "RF": {
            "EE_TP": [0.5022639680823797, 0.637300087900218],
            "EC_TP": [0.8364513925497833, 1.0895331038036824],
            "COSTO_TP": [0.5022639680823798, 0.6373000879002179]
        }
    },
    "6": {
        "SVR": {
            "EE_TP": [0.48854168207252924, 0.5562265389867125],
            "EC_TP": [0.9602781150948855, 1.0332453300324562],
            "COSTO_TP": [0.48854168207229354, 0.5562265389892241]
        },
        "RF": {
            "EE_TP": [0.5535849558215183, 0.6199439284178251],
            "EC_TP": [1.1049660242695207, 1.2319044105445651],
            "COSTO_TP": [0.5535849558215181, 0.6199439284178249]
        }
    }
}


if __name__ == "__main__":
    
    #print(type(scaler), type(clustering))
    x = scaler(100, 99, 0.035)
    cluster = make_clustering(x)
    print(cluster)
    #y = predict_cm(x, cluster)
    #print(y)