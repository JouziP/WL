# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import timeit
import plotly.plotly as py
from plotly.graph_objs import *

from WL.Lattices.latticeConstructor import constructLattice
from WL.Lattices.latticeLinkRemover import linkRemover


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
#################################
input_id = 1 #sys.argv[1]
#print input_id



filename = 'inputs_%d.csv'%int(input_id)
INPUTS = '../../../INPUTS/'
inputs = pd.read_csv(INPUTS+filename)

#
np.random.seed(1051)
#
#
args={}
############ Hamilt
args['J_const']= float(inputs['J_const'])   #-1.0
args['E_field']= float(inputs['E_field'])   #0.0
args['power']= float(inputs['power'])     #3.0
##########  lattice
N1=int(inputs['N1'])
N2=int(inputs['N2'])
### 
a1_x= float(inputs['a1_x'])
a1_y= float(inputs['a1_y'])
theta=np.pi/float(inputs['tetha_fraction'])
a2_x=np.cos(theta)
a2_y=np.sin(theta)
###
args['theta'] = theta
args['a1_x']=a1_x
args['a1_y']=a1_y
args['a2_x']=a2_x
args['a2_y']=a2_y
args['N1'] = N1
args['N2'] = N2
args['N_spins']=N1*N2
args['first_neighb']=inputs['first_neighb'][0]
##
##
#############
start_time = timeit.default_timer()
#print 'building lattice :'
neighbors_table=constructLattice(**args)
args['percentage_of_links_to_be_removed']=inputs['percentage_of_links_to_be_removed'][0]
neighbors_table = linkRemover(neighbors_table, **args)
elapsed = timeit.default_timer() - start_time


edges = []
for spin_idx in range(N1*N2):
    for j in range(neighbors_table[spin_idx].shape[0]):
        if neighbors_table[spin_idx][j, 1]!=0:
            edges.append((spin_idx, int(neighbors_table[spin_idx][j, 0]) ))
        
            
    
G = nx.Graph()
G.add_edges_from(edges)

for node in G.node:
    x=np.random.uniform()
    y=np.random.uniform()
#    print x,y 
    G.node[node]['pos']=(x, y)


edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')
    
for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
#    print x0, y0
#    print x1,y1
#    print '-----'
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]


node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))
#        
for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)
    
fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
#                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
#                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False))
    )

py.iplot(fig, filename='N1_%d_N2_%d_links_%d.fig'%(N1, N2, args['percentage_of_links_to_be_removed']))

