import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, adjacency_matrix):
        self.__adjacency_matrix = adjacency_matrix.copy()
        self.__graph = nx.from_pandas_adjacency(self.__adjacency_matrix, create_using=nx.DiGraph)
        self.__cycles = self.__get_cycles()
        self.pair_cycles = self.__get_pair_cycles()
        self.__edges_colors = self.__get_edges_colors()

    def __get_edges_colors(self):
        """Встановлюємо зелений колір для позитивних ребер та червоний для негативних."""
        edges_colors = ['#D6AE01' if edge[2]['weight'] > 0 else '#E63244' for edge in self.__graph.edges(data=True)]
        return edges_colors

    def __get_cycles(self):
        """Отримуємо всі існуючі у графі цикли."""

        def cycle_to_edges(_cycle_):
            _cycle_.append(_cycle_[0])
            edges = set()
            for idx in range(len(_cycle_)-1):
                edges.add((_cycle_[idx], _cycle_[idx+1]))
            return edges

        try:
            dirty_cycles = [*nx.simple_cycles(self.__graph)]
        except nx.exception.NetworkXNoCycle:
            return tuple()
        cycles = list()
        cycles_edges_sets = list()
        for cycle in dirty_cycles:
            cycle_edges = cycle_to_edges(cycle.copy())
            if cycle_edges not in cycles_edges_sets:
                cycles_edges_sets.append(cycle_edges)
                cycles.append(cycle)
        return tuple(cycles)

    def __get_pair_cycles(self):
        """Отримуємо всі парні цикли (цикли з парною кількістю негативних ребер)."""

        def get_number_of_negative_edges(graph, _cycle_):
            number_of_negative_edges = 0
            _cycle_.append(_cycle_[0])
            for idx in range(len(_cycle_)-1):
                edge_data = graph.get_edge_data(_cycle_[idx], _cycle_[idx+1])
                number_of_negative_edges += edge_data['weight'] < 0
            return number_of_negative_edges

        pair_cycles = list()
        for cycle in self.__cycles:
            if get_number_of_negative_edges(self.__graph, cycle.copy()) % 2 == 0:
                pair_cycles.append(cycle)
        return tuple(pair_cycles)

    def plot_graph(self, show_weight=False):  # сделать апгрейд, не очень ок рисует
        """Малюємо граф."""
        pos = nx.spiral_layout(self.__graph)
        nx.draw_networkx(self.__graph, pos=pos, edge_color=self.__edges_colors, node_size=725, node_color='#969992')
        if show_weight:
            edge_labels = nx.get_edge_attributes(self.__graph, 'weight')
            nx.draw_networkx_edge_labels(self.__graph, pos=pos, edge_labels=edge_labels, label_pos=0.25)
        plt.show()


# def test_graph():
#     adjacency_matrix = pd.read_excel("AdjacencyMatrix.xlsx", index_col=0)
#     graph = Graph(adjacency_matrix)
#     graph.plot_graph()
#
#
# if __name__ == '__main__':
#     test_graph()

