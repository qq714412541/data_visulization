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

    df2.loc[index,'effdistance'] = (1-math.log(row['weight']))

    #print(df2['effdistance'])

df2=df2.dropna(axis=0, how='any')
print(df2)

import networkx as nx
import matplotlib.pyplot as plt



###put all data into graph
G = nx.Graph()

for index,row in df2.iterrows():
    #print(index)
    #print(row['from'],row['to'],row['effdistance'])
    G.add_edge(row['from'],row['to'],weight = row['effdistance'])


print(G)
print(G.nodes)
print(G.edges)
print(nx.negative_edge_cycle(G))

pos = nx.shell_layout(G)

#nx.draw(G,pos,alpha=0.5, node_size=3,node_color = 'r',font_size = 5,width=[float(v['weight']*0.05) for (r,c,v) in G.edges(data=True)],cmap = plt.get_cmap('jet'),
        #with_labels=True)
#plt.show()
###use method of dijkstra to get shortest path and distance
path=nx.dijkstra_path(G, source='Mexico', target='China')
print('M到C的路径：', path,type(path))
distance=nx.dijkstra_path_length(G,source='Mexico', target='China')
print('M到C的距离为：', distance)

path=nx.dijkstra_path(G, source='China', target='Mexico')
print('C到M的路径：', path)
distance=nx.dijkstra_path_length(G,source='China', target='Mexico')
print('C到M的距离为：', distance)

#df1 = pd.DataFrame(df1, dtype=object)
###do circulation to get all efficient distance
path_hk = list
path_US = list
path_UK = list
a = pd.DataFrame(columns=('from','to','new_effdis'))#hk
b = pd.DataFrame(columns=('from','to','new_effdis'))#USA
c = pd.DataFrame(columns=('from','to','new_effdis'))#UK
for index,row in df1.iterrows():
    path_hk = nx.dijkstra_path(G,source='HongKong(SAR)China', target=row['H1N1country'])
    #print(path_hk)
    for i in range(len(path_hk)-1):
        temp = df2.loc[(df2['from']==path_hk[i])&(df2['to']==path_hk[i + 1]),'effdistance']
        #print(float(temp),type(temp))
        a = a.append(pd.DataFrame({'from': path_hk[i], 'to': path_hk[i + 1], 'new_effdis': float(temp)}, index=[1]))
    #path_hk[index] = nx.dijkstra_path(G,source='HongKong(SAR)China', target=row['H1N1country'])
    #df1.at[index,'path'] = nx.dijkstra_path(G,source='HongKong(SAR)China', target=row['H1N1country'])
    df1.loc[index,'new_effdis'] = nx.dijkstra_path_length(G,source='HongKong(SAR)China', target=row['H1N1country'])


df_hongkong = df1

for index,row in df1.iterrows():
    path_US = nx.dijkstra_path(G, source='USA', target=row['H1N1country'])
    # print(path_hk)
    for i in range(len(path_US) - 1):
        temp = df2.loc[(df2['from'] == path_US[i]) & (df2['to'] == path_US[i + 1]), 'effdistance']
        #print(float(temp), type(temp))
        b = b.append(pd.DataFrame({'from': path_US[i], 'to': path_US[i + 1], 'new_effdis': float(temp)}, index=[1]))
    #df1[index,'path'] = nx.dijkstra_path(G,source='HongKong(SAR)China', target=row['H1N1country'])
    df1.loc[index,'new_effdis'] = nx.dijkstra_path_length(G,source='USA', target=row['H1N1country'])

df_US = df1

for index,row in df1.iterrows():
    path_UK = nx.dijkstra_path(G, source='UnitedKingdom', target=row['H1N1country'])
    # print(path_hk)
    for i in range(len(path_UK) - 1):
        temp = df2.loc[(df2['from'] == path_UK[i]) & (df2['to'] == path_UK[i + 1]), 'effdistance']
        #print(float(temp), type(temp))
        c = c.append(pd.DataFrame({'from': path_UK[i], 'to': path_UK[i + 1], 'new_effdis': float(temp)}, index=[1]))
    #df1[index,'path'] =  nx.dijkstra_path(G,source='HongKong(SAR)China', target=row['H1N1country'])
    df1.loc[index,'new_effdis'] = nx.dijkstra_path_length(G,source='UnitedKingdom', target=row['H1N1country'])

df_UK = df1


'''fig = pex.scatter(df1,x=df1['new_effdis'],y=df1['arrivalT'],hover_name=df1['H1N1country'],labels = {'Distance':'new_effDistance', 'arrivalT':'arrival_time(day)'})
fig.show()'''
#print(df_hongkong)
#print(df_US)
#print(df_UK)
print(a)
print(b)
print(c)


G_hk = nx.MultiDiGraph()

for index,row in a.iterrows():
    #print(index)
    #print(row['from'],row['to'],row['effdistance'])
    G_hk.add_edge(row['from'],row['to'],weight = row['new_effdis'])


#print(G)
#print(G.nodes)
#print(G.edges(data=True))

#pos = nx.shell_layout(G)
edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G_hk.edges(data=True)])

#nx.draw_networkx_edge_labels(G_hk,  edge_labels=edge_labels, label_pos=0.3, font_size=3)

nx.draw(G_hk,alpha=0.5, node_size=3,node_color = 'r',font_size = 5,width=[float(v['weight']*0.05) for (r,c,v) in G_hk.edges(data=True)],
        with_labels=True)
plt.savefig('3_5_central_hk.jpg', dpi=300)
plt.show()


G_US = nx.MultiDiGraph()

for index,row in a.iterrows():
    #print(index)
    #print(row['from'],row['to'],row['effdistance'])
    G_US.add_edge(row['from'],row['to'],weight = row['new_effdis'])


#print(G)
#print(G.nodes)
#print(G.edges(data=True))

#pos = nx.shell_layout(G)
edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G_US.edges(data=True)])

#nx.draw_networkx_edge_labels(G_hk,  edge_labels=edge_labels, label_pos=0.3, font_size=3)

nx.draw(G_US,alpha=0.5, node_size=3,node_color = 'r',font_size = 5,width=[float(v['weight']*0.05) for (r,c,v) in G_US.edges(data=True)],
        with_labels=True)
plt.savefig('3_5_central_US.jpg', dpi=300)
plt.show()


G_UK = nx.MultiDiGraph()

for index,row in a.iterrows():
    #print(index)
    #print(row['from'],row['to'],row['effdistance'])
    G_UK.add_edge(row['from'],row['to'],weight = row['new_effdis'])


#print(G)
#print(G.nodes)
#print(G.edges(data=True))

#pos = nx.shell_layout(G)
edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G_UK.edges(data=True)])

#nx.draw_networkx_edge_labels(G_hk,  edge_labels=edge_labels, label_pos=0.3, font_size=3)

nx.draw(G_UK,alpha=0.5, node_size=3,node_color = 'r',font_size = 5,width=[float(v['weight']*0.05) for (r,c,v) in G_UK.edges(data=True)],
        with_labels=True)
plt.savefig('3_5_central_UK.jpg', dpi=300)
plt.show()




