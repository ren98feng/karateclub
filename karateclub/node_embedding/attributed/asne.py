import random
import numpy as np
import networkx as nx
from typing import Union
from scipy.sparse import coo_matrix
from karateclub.estimator import Estimator
from gensim.models.word2vec import Word2Vec
from karateclub.utils.walker import RandomWalker

class ASNE(Estimator):
    r"""An implementation of `"ASNE" <https://arxiv.org/abs/1705.04969>`_
    from the TKDE '18 paper "Attributed Social Network Embedding". The 
    procedure implicitly factorizes a joint adjacency matrix power and feature matrix.
    The decomposition happens on truncated random walks and the adjacency matrix powers
    are pooled together.
       
    Args:
        dimensions (int): Dimensionality of embedding. Default is 128.
        workers (int): Number of cores. Default is 4.
        epochs (int): Number of epochs. Default is 1.
        learning_rate (float): HogWild! learning rate. Default is 0.05.
        min_count (int): Minimal count of node occurrences. Default is 1.
        seed (int): Random seed value. Default is 42.
    """
    def __init__(self, dimensions: int=128, workers: int=4, epochs: int=1,
                 learning_rate: float=0.05, min_count: int=1, seed: int=42):

        self.dimensions = dimensions
        self.workers = workers
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.min_count = min_count
        self.seed = seed


    def _feature_transform(self, graph, X):
        features = {str(node): [] for node in graph.nodes()}
        nodes = X.row
        for i, node in enumerate(nodes):
            features[str(node)].append("feature_"+ str(X.col[i]))
        return features

    def _select_walklets(self):
        self._walklets = []
        for walk in self._walker.walks:
            for power in range(1, self.window_size+1): 
                for step in range(power+1):
                    neighbors = [n for i, n in enumerate(walk[step:]) if i % power == 0]
                    neighbors = [n for n in neighbors for _ in range(0, 3)]
                    neighbors = [random.choice(self._features[val]) if i % 3 == 1 and self._features[val] else val for i, val in enumerate(neighbors)]
                    self._walklets.append(neighbors)
        del self._walker
        
        
    def fit(self, graph: nx.classes.graph.Graph, X: Union[np.array, coo_matrix]):
        """
        Fitting a SINE model.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be embedded.
            * **X** *(Scipy COO array)* - The matrix of node features.
        """
        self._set_seed()
        self._check_graph(graph)
        self._walker = RandomWalker(self.walk_length, self.walk_number)
        self._walker.do_walks(graph)
        self._features = self._feature_transform(graph, X)
        self._select_walklets()

        model = Word2Vec(self._walklets,
                         hs=0,
                         alpha=self.learning_rate,
                         iter=self.epochs,
                         size=self.dimensions,
                         window=1,
                         min_count=self.min_count,
                         workers=self.workers,
                         seed=self.seed)

        self.embedding = np.array([model[str(n)] for n in range(graph.number_of_nodes())])

    def get_embedding(self) -> np.array:
        r"""Getting the node embedding.

        Return types:
            * **embedding** *(Numpy array)* - The embedding of nodes.
        """
        embedding = self.embedding
        return embedding
