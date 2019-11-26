import plotly.express as pex
import pandas as pd


df = pd.read_csv('./H1N1ArrivalT-1.csv')
print(df)

fig = pex.scatter(df,x=df['Distance'],y=df['arrivalT'],hover_name=df['H1N1country'],labels = {'Distance':'effDistance', 'arrivalT':'arrival_time(day)'})

import plotly.offline as pltoff
pltoff.plot(fig, filename='3_1_scatterplot.html')
fig.show()