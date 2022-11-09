#!/usr/bin/python3
import sqlite3
import plotly
import plotly.graph_objs as go
import datetime

currentdate = datetime.datetime.today().strftime("%d/%m/%Y")
file_db = './sensordata.db'
try:
    sqlite_connection = sqlite3.connect(file_db)
    cursor = sqlite_connection.cursor()
    select = cursor.execute("SELECT currentime, temperature, currentdate FROM temp_sens WHERE currentdate = '" + currentdate + "';")
    data = select.fetchall()
    cursor.close()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

dict_new = dict()
dict_new['currentime'] = [data[0][0]]
dict_new['temperature'] = [data[0][1]]
for i in data:
    if i[1] == dict_new['temperature'][-1]: continue
    else:
            dict_new['currentime'].append(i[0])
            dict_new['temperature'].append(i[1])


curr_graph = go.Scatter(
   x = dict_new['currentime'],
   y = dict_new['temperature'],
   mode = 'lines+markers',
   yaxis="y",
   name='esp32_room',
   hovertemplate="Date: %{x}<br>Celsius: %{y}"
)

curr_layout = go.Layout(
    title = "date: " + data[-1][2],
    xaxis=dict(title = "Date"),
    yaxis=dict(title = "Celsius")
)
data = [curr_graph]


plotly.offline.plot(
   { "data": [curr_graph],"layout": curr_layout })