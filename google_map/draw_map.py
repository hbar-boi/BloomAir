import gmaps
from bokeh import io
from bokeh.plotting import gmap
from bokeh.models import GMapOptions, Scatter, Plot, LinearAxis
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.layouts import gridplot
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.palettes import Plasma256 as palette1
from bokeh.palettes import Viridis256 as palette2
from bokeh.palettes import Spectral10
from bokeh.models import ColorBar
import pandas as pd
import time
import numpy as np
from sklearn.ensemble import IsolationForest  

api_key = 'AIzaSyBrK9dNHHfxpAfjMjg_iC9skTkgjaMMyHo'
lat = 47.375
lng = 8.55
zoom = 15
map_type='roadmap'
bokeh_width, bokeh_height = 500, 400

df = pd.read_csv('test.csv')
df_train = df.iloc[:100, :]
df_test = df.iloc[100:, :]
X_train = np.array(df_train[['Temp_F', 'Humidity']])
X_test = np.array(df_test[['Temp_F', 'Humidity']])

# anomaly detection training
clf = IsolationForest(max_samples=100,random_state=100, contamination = 0.1)
clf.fit(X_train)


# drawing graphs
df = pd.read_csv('df_test.csv')
df_data = df[df['t'] == max(df['t'])]

gmap_options = GMapOptions(lat=lat, lng=lng, 
                            map_type=map_type, zoom=zoom)
hover = HoverTool(
    tooltips = [
        ('Longitude', '@lon'),
        ('Latitude', '@lat'),
        ('Temperature', '@temp F'),
        ('Humidity', '@humidity'),
        ('Alert', '@c_alert')
    ]
)


source = ColumnDataSource(dict(df_data))
source1 = ColumnDataSource(dict(df_data))
source2 = ColumnDataSource(dict(df_data))

mapper1 = linear_cmap('temp', palette1, 60., 90.) 
p1 = gmap(api_key, gmap_options, title='ETH surroundings(temperature)', 
        tools=[hover, 'reset', 'wheel_zoom', 'pan'])
center = p1.diamond('lon', 'lat', size=20, alpha=0.9, color=mapper1, source = source)
color_bar = ColorBar(color_mapper=mapper1['transform'], 
                         location=(0,0))
p1.add_layout(color_bar, 'right')


mapper2 = linear_cmap('humidity', palette2, 30., 90.) 
p2 = gmap(api_key, gmap_options, title='ETH surroundings(Humidity)', 
        tools=[hover, 'reset', 'wheel_zoom', 'pan'])
center1 = p2.diamond('lon', 'lat', size=20, alpha=0.9, color=mapper2, source = source)
color_bar = ColorBar(color_mapper=mapper2['transform'], 
                         location=(0,0))
p2.add_layout(color_bar, 'right')


p4 = gmap(api_key, gmap_options, title='ETH surroundings(Alert)', 
        tools=[hover, 'reset', 'wheel_zoom', 'pan'])
p4.diamond('lon', 'lat', size=20, alpha=0.9, fill_color='#db6f6d', source = source1)
p4.diamond('lon', 'lat', size=20, alpha=0.9, fill_color='#8daccd', source = source2)



p3 = Plot(title=None, #idth=300, height=300,
    min_border=0, toolbar_location=None)
g1 = Scatter(x="temp", y="humidity", size=10, marker='circle', fill_color = '#db6f6d')
g2 = Scatter(x="temp", y="humidity", size=10, marker='circle', fill_color = '#8daccd')
p3.add_glyph(source1, g1)
p3.add_glyph(source2, g2)

xaxis = LinearAxis()
p3.add_layout(xaxis, 'below')
yaxis = LinearAxis()
p3.add_layout(yaxis, 'left')

grid = gridplot([[p1, p2], [p3, p4]], width=500, height=400)
io.curdoc().add_root(grid)


def stream():
    df = pd.read_csv('df_test.csv')
    df_data = df[df['t'] == max(df['t'])].reset_index(drop= True)

    X_test = np.array(df_data[['temp', 'humidity']])
    y_pred_test = clf.predict(X_test)
    df_data.loc[(y_pred_test == -1), 'c_alert'] = '1'
    source.data = dict(df_data)
    source1.data = dict(df_data.loc[(y_pred_test == -1), :])
    source2.data = dict(df_data.loc[(y_pred_test == 1), :])

    time.sleep(1)

io.curdoc().add_periodic_callback(stream, 10)

