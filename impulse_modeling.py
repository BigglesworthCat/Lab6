import pandas as pd
import numpy as np


class ImpulseProcess:

    def __init__(self, adjacency_matrix, start_q, start_x=None, start_p=None):
        self.adjacency_matrix = adjacency_matrix.copy()
        self.t = 0  # Number of current step
        self.q = self.__get_start_q(start_q)
        self.x = self.__get_start_x(start_x)
        self.p = self.__get_start_p(start_p)

    def __get_start(self, item):
        index = self.adjacency_matrix.index
        columns = [0]
        item = pd.DataFrame(data=item, index=index, columns=columns)
        return item

    def __get_start_q(self, q):
        """Отримати значення q на нульовому кроці."""
        q = self.__get_start(q)
        return q

    def __get_start_x(self, x=None):
        """Отримати значення x на нульовому кроці."""
        if x is None:
            x = np.zeros(len(self.adjacency_matrix))
        x = self.__get_start(x)
        return x

    def __get_start_p(self, p=None):
        """Отримати значення p на нульовому кроці."""
        if p is None:
            p = np.zeros(len(self.adjacency_matrix))
        p = self.__get_start(p)
        return p

    def __add_q(self, q):
        """Додати значення q на self.t-ому кроці."""
        self.q[self.t] = q
        return self.q[self.t]  # OPTIONAL

    def __add_p(self):
        """Додати значення p на self.t-ому кроці."""
        self.p[self.t] = self.x[self.t] - self.x[self.t-1]
        return self.p[self.t]  # OPTIONAL

    def __add_x(self):
        """Додати значення x на self.t-ому кроці."""
        self.x[self.t] = self.x[self.t-1] + np.dot(self.adjacency_matrix, self.p[self.t-1]) + self.q[self.t-1]
        return self.x[self.t]  # OPTIONAL

    def send_impulse(self, q):
        """Просуває імпульсне моделювання на 1 крок."""
        self.t += 1
        self.__add_q(q)
        self.__add_x()
        self.__add_p()

    def impulse_modeling(self, q_impulses, n):
        """Просуває імпульсне моделювання на n кроків."""
        for t in np.arange(1, n):
            self.send_impulse(q_impulses.iloc[:, t])
        self.t += 1
        self.__add_x()  # TEST

    def get_statistic(self, t=None):
        if t is None or t > self.t:
            x = self.x.copy()
            p = self.p.copy()
            q = self.q.copy()
        else:
            x = self.x[t].copy()
            p = self.p[t].copy()
            q = self.q[t].copy()
        statistic = {'x': x, 'p': p, 'q': q}
        return statistic


def get_default_impulses():
    pass