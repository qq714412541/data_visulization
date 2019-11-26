import plotly.express as px
import pandas as pd
'''gapminder = px.data.gapminder()
pd.set_option('display.max_columns', None)
print(gapminder)'''


df1 = pd.read_csv('./H1N1ArrivalT-1.csv')

df2 = px.data.gapminder()
df2_1 = df2[['country','iso_alpha']]

df3 = pd.merge(df1, df2_1, how='inner', left_on='H1N1country', right_on='country',
      left_index=False, right_index=False, sort=True,
      copy=True, indicator=False)
df4 = df3[['H1N1country','arrivalT','iso_alpha']]
df5 = df4.drop_duplicates()
df6 = df5.sort_values(by='arrivalT',ascending=True)

print(df6)
df6['arrivalT'][(df6['arrivalT']<=56)&(df6['arrivalT']>42)] = 56
df6['arrivalT'][(df6['arrivalT']<=42)&(df6['arrivalT']>28)] = 42
df6['arrivalT'][(df6['arrivalT']<=28)&(df6['arrivalT']>14)] = 28
df6['arrivalT'][df6['arrivalT']<=14] = 14

print(df6)




######do circulation

for index, row in df6.iterrows():
    #print (row["H1N1country"], row["arrivalT"])
    #print(type(row['arrivalT']))
    if row['arrivalT'] <= 56:
        row['arrivalT'] = 56
        s = pd.Series([row['H1N1country'],row['arrivalT'],row['iso_alpha']], index=df6.columns)
        #print('######',s)
        df6 = df6.append(s, ignore_index=True)

for index, row in df6.iterrows():
    #print (row["H1N1country"], row["arrivalT"])
    #print(type(row['arrivalT']))
    if row['arrivalT'] <= 42:
        row['arrivalT'] = 42
        s = pd.Series([row['H1N1country'],row['arrivalT'],row['iso_alpha']], index=df6.columns)
        #print('######',s)
        df6 = df6.append(s, ignore_index=True)


for index, row in df6.iterrows():
    #print (row["H1N1country"], row["arrivalT"])
    #print(type(row['arrivalT']))
    if row['arrivalT'] <= 28:
        row['arrivalT'] = 28
        s = pd.Series([row['H1N1country'],row['arrivalT'],row['iso_alpha']], index=df6.columns)
        #print('######',s)
        df6 = df6.append(s, ignore_index=True)






print(df6)

df7 = df6.sort_values(by='arrivalT',ascending=True)

print(df7)



#print(df6)



######



fig = px.scatter_geo(df7, locations="iso_alpha",
                     hover_name="H1N1country",
                     animation_frame="arrivalT",
                     projection="natural earth")
import plotly.offline as pltoff
pltoff.plot(fig, filename='3_3_morbidity_map.html')
fig.show()








