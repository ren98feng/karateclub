"""Example runs with Karate Club."""

import networkx as nx

import community
import numpy as np

from karateclub.community_detection.overlapping import EgoNetSplitter, NNSED, DANMF, MNMF, BigClam
from karateclub.community_detection.non_overlapping import EdMot, LabelPropagation
from karateclub.node_embedding.neighbourhood import GraRep, DeepWalk, Walklets
from karateclub.node_embedding.structural import GraphWave
from karateclub.node_embedding.attributed import BANE


#-----------------------------------
# BANE example
#-----------------------------------

g = nx.newman_watts_strogatz_graph(100, 20, 0.05)

x = np.random.uniform(0,1,(100,2000))

p = nx.newman_watts_strogatz_graph(100, 20, 0.05)

x = nx.adjacency_matrix(p)
model = BANE()

model.fit(g, x)

#------------------------------------
# BigClam example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 20, 0.05)

model = BigClam()

model.fit(g)

membership = model.get_memberships()

#------------------------------------
# Walklets example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 20, 0.05)

model = Walklets()

model.fit(g)

emb = model.get_embedding()

#------------------------------------
# DeepWalk example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 20, 0.05)

model = DeepWalk()

model.fit(g)

#------------------------------------
# Splitter example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 20, 0.05)

model = EgoNetSplitter(1.0)

model.fit(g)

#------------------------------------
# Edmot example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.9)

model = EdMot(3, 0.5)

model.fit(g)

#------------------------------------
# DANMF example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.02)

model = DANMF()

model.fit(g)

#------------------------------------
# M-NMF example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.02)

model = MNMF()

model.fit(g)

#------------------------------------
# Label Propagation example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.02)

model = LabelPropagation()

model.fit(g)

#------------------------------------
# GraRep example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.02)

model = GraRep()

model.fit(g)

embedding = model.get_embedding()

#------------------------------------
# GraphWave example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.02)

model = GraphWave()

model.fit(g)

embedding = model.get_embedding()

#------------------------------------
# NNSED example
#------------------------------------

g = nx.newman_watts_strogatz_graph(100, 10, 0.02)

model = NNSED()

model.fit(g)

embedding = model.get_embedding()

memberships = model.get_memberships()

