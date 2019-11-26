import plotly.express as pex
import pandas as pd
import math

#set rule for display
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

#########get effcient distance for all path
df1 = pd.read_csv('./H1N1ArrivalT-1.csv')
df2 = pd.read_csv('./countriesAirlines.csv')
df2['effdistance'] = None

for index,row in df2.iterrows():

    df2.loc[index,'effdistance'] = round((1-math.log(row['weight'])),3)
    if (1-math.log(row['weight']))<=0:
        print('########??????????????????????????')

    #print(df2['effdistance'])
df2=df2.dropna(axis=0, how='any')
df2.to_csv('./newcountryairlines.csv')


print(df2)




import networkx as nx
import matplotlib.pyplot as plt



###put all data into graph
G = nx.MultiDiGraph()

for index,row in df2.iterrows():
    #print(index)
    #print(row['from'],row['to'],row['effdistance'])
    G.add_edge(row['from'],row['to'],weight = row['effdistance'])


#print(G)
#print(G.nodes)
#print(G.edges(data=True))

pos = nx.shell_layout(G)
edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G.edges(data=True)])

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=3)

nx.draw(G,pos,alpha=0.5, node_size=3,node_color = 'r',font_size = 5,width=[float(v['weight']*0.05) for (r,c,v) in G.edges(data=True)],cmap = plt.get_cmap('jet'),
        with_labels=True)
plt.savefig('3_4_all_path.jpg', dpi=300)
plt.show()
###use method of dijkstra to get shortest path and distance
path=nx.dijkstra_path(G, source='Colombia', target='Mexico')
print('M到C的路径：', path)
distance=nx.dijkstra_path_length(G,source='Colombia', target='Mexico')
print('M到C的距离为：', distance)

path=nx.dijkstra_path(G, source='Mexico', target='Colombia')
print('C到M的路径：', path)
distance=nx.dijkstra_path_length(G,source='Mexico', target='Colombia')
print('C到M的距离为：', distance)


###do circulation to get all efficient distance
for index,row in df1.iterrows():

    #print(row['H1N1country'])
    df1.loc[index,'new_effdis'] = nx.dijkstra_path_length(G,source='Mexico', target=row['H1N1country'])

print(df1)


fig = pex.scatter(df1,x=df1['new_effdis'],y=df1['arrivalT'],hover_name=df1['H1N1country'],labels = {'Distance':'new_effDistance', 'arrivalT':'arrival_time(day)'})

import plotly.offline as pltoff
pltoff.plot(fig, filename='3_4_scatterplot.html')
fig.show()



