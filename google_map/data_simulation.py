import numpy as np
import matplotlib.pyplot as plt
# from sklearn.ensemble import IsolationForest  
from sklearn.linear_model import LinearRegression
import pandas as pd
import time

# train linear model
df = pd.read_csv('test.csv')
df_train = df.iloc[:100, :]
df_test = df.iloc[100:, :]
X_train = np.array(df_train[['Temp_F', 'Humidity']])
X_test = np.array(df_test[['Temp_F', 'Humidity']])


reg = LinearRegression().fit(X_train[:, :1], X_train[:, 1:])


data_list = []
lon_list = [8.545, 8.5453]
lat_list = [47.372, 47.374]
id_list = [1, 2]
id_curr = 2

# data generation
for t in range(1000):
    time.sleep(1)

    if t%100 == 0:
        id_curr += 1
        lat = np.random.uniform(47.37, 47.38)
        lon = np.random.uniform(8.544, 8.556)
        id_list.append(id_curr)
        lon_list.append(lon)
        lat_list.append(lat)

    for i in range(len(id_list)):
        id = id_list[i]
        lon = lon_list[i]
        lat = lat_list[i]
        p = np.random.choice([1,0], 1, p=[0.95, 0.05])[0]
        if p == 1:
            temp = np.random.uniform(60,90)
            humidity = reg.predict(np.array([[temp]]))[0][0] + np.random.uniform(-1,1)
        if p == 0:
            temp = np.random.uniform(50, 60)
            humidity = reg.predict(np.array([[temp]]))[0][0] + np.random.uniform(-10,10)
    
        data_list.append([id, lon, lat, t, temp, humidity, '0'])
        df_data = pd.DataFrame(data_list, columns = ['id', 'lon', 'lat', 't' , 'temp', 'humidity', 'c_alert'])
    
    df_data.to_csv('df_test.csv', index = 0)