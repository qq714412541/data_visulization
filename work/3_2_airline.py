import plotly.graph_objects as go
import pandas as pd


#########
df1 = pd.read_csv('./airportsAirlines.csv')
#print(df1)
#print(df1.head())
#print(df1.loc[:,:])
df2 = pd.read_csv('./airports.csv')

df3 = pd.merge(df1, df2, how='inner', left_on='from', right_on='lid',
      left_index=False, right_index=False, sort=True,
      copy=True, indicator=False)
df4 = df3[['from','to','lon','lat']]
df4.columns = ['from','to','from_lon','from_lat']

df5 = pd.merge(df4, df2, how='inner', left_on='to', right_on='lid')
df6 = df5[['from','to','from_lon','from_lat','lon','lat']]
df6.columns = ['from','to','from_lon','from_lat','to_lon','to_lat']
print(df6)
#########get all lines' lon and lat

df_airports = pd.read_csv('./airports.csv')
df_airports.head()
print(df_airports.head())
print('##########')


fig = go.Figure()

fig.add_trace(go.Scattergeo(

    lon = df_airports['lon'],
    lat = df_airports['lat'],
    hovertext = df_airports['name'],


    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

flight_paths = []
for i in range(len(df6)):
    fig.add_trace(
        go.Scattergeo(

            lon = [df6['from_lon'][i], df6['to_lon'][i]],
            lat = [df6['from_lat'][i], df6['to_lat'][i]],
            mode = 'lines',
            line = dict(width = 1,color = 'red'),
            hovertext=df6['from']+' to '+df6['to'],

        )
    )

fig.update_layout(
    title_text = ' World Airline flight paths<br>(Hover for airport names)',
    showlegend = False,
    geo = go.layout.Geo(

        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
)

import plotly.offline as pltoff
pltoff.plot(fig, filename='3_2_world_airports.html')
fig.show()
