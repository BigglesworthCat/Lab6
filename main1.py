import sys

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PyQt5 import QtWidgets
from interface import Ui_MainWindow


from cognitive_matrix import Stability
from impulse_modeling import ImpulseProcess


class UI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.adjacency_matrix = None
        self.stability = None
        self.impulse_process = None
        self.n_model_steps = None
        self.q_impulses = None
        self.first_am_load = True

        self.load_am.clicked.connect(self.load_adjacency_matrix)
        self.save_am.clicked.connect(self.save_adjacency_matrix)
        self.browse_input.clicked.connect(self.choose_adjacency_matrix)
        self.browse_output.clicked.connect(self.choose_output)
        self.check_stability_button.clicked.connect(self.check_stability)
        self.plot_graph_button.clicked.connect(self.plot_graph)

        self.im.clicked.connect(self.impulse_modeling)
        self.clear_im.clicked.connect(self.clear_qx_table)

    def load_adjacency_matrix(self):
        """Завантаження програмою матриці суміжності та відображення її в інтерфейсі."""
        filename = self.input_filename.text()
        try:
            self.adjacency_matrix = pd.read_excel(filename, index_col=0)
            self.output_adjacency_matrix()
            self.set_q_table()
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Помилка!', f'Файл вхідних даних {filename} не знайдено.')
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, 'Помилка!', f'Доступ до файлу вхідних даних {filename} заборонено.')

    def save_adjacency_matrix(self):
        filename = self.output_filename.text()
        try:
            self.read_adjacency_matrix()
            self.adjacency_matrix.to_excel(filename)
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, 'Помилка!', f'Доступ до файлу вихідних даних {filename} заборонено.')

    def clear_q_table(self):
        """Очищення матриці імпульсів."""
        m, n = self.q_table.size()
        for column in range(n):
            item = QtWidgets.QTableWidgetItem(0)
            self.q_table.setItem(item, 0, column)

    def clear_x_table(self):
        """Очищення матриці результатів імпульсного моделювання."""
        self.x_table.clear()
        self.x_table.setRowCount(0)
        self.x_table.setColumnCount(0)

    def clear_qx_table(self):
        self.clear_q_table()
        self.clear_x_table()

    def choose_adjacency_matrix(self):
        """Обрання файлу з матрицею суміжності за допомогою Провідника."""
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open data file', '.', 'Data file (*.xlsx)')[0]
        self.input_filename.setText(filename)

    def choose_output(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open data file', '.', 'Data file (*.xlsx)')[0]
        self.output_filename.setText(filename)

    def read_adjacency_matrix(self):
        """Зчитування матриці суміжності з інтерфейсу."""
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix.columns)):
                self.adjacency_matrix.iloc[i, j] = float(self.adjacency_matrix_out.item(i, j).text())

    def check_stability(self):
        """Перевіряємо матрицю на стійкість та виводимо результати у інтерфейс."""
        self.read_adjacency_matrix()
        self.stability = Stability(self.adjacency_matrix)

        def bull_converter(bull_term):
            return 'так!' if bull_term else 'ні!'

        self.set_structure_stability.setText(bull_converter(self.stability.structure_stability))
        self.set_value_stability.setText(bull_converter(self.stability.value_stability))
        self.set_perturbation_stability.setText(bull_converter(self.stability.value_stability))

        self.spectral_radius_out.setText(f'{self.stability.spectral_radius:.2f}')
        self.pair_cycles_number_out.setText(str(len(self.stability.graph.pair_cycles)))
        self.print_eigenvalues()
        self.print_pair_cycles()


    def print_eigenvalues(self):
        """Друкуємо власні числа матриці."""
        self.eigenvalues_out.clear()
        for ev in self.stability.eigenvalues:
            self.eigenvalues_out.addItem('{0:.2f} {1} {2:.2f}i'.format(ev.real, '+-'[int(ev.imag < 0)], abs(ev.imag)))

    def sort_by_length(item1, item2):
        return len(item1.text()) < len(item2.text())

    def print_pair_cycles(self):
        """Друкуємо парні цикли матриці."""
        self.pair_cycles_out.clear()
        rofl_list = []
        for pc in self.stability.graph.pair_cycles:
            pc.append(pc[0])
            pc = '~>'.join(e for e in pc)
            rofl_list.append(pc)
            # self.pair_cycles_out.addItem(pc)
        rofl_list = sorted(rofl_list, key=len)
        for pc in rofl_list:
            self.pair_cycles_out.addItem(pc)

    def plot_graph(self):
        """Створення малюнку графу."""
        self.read_adjacency_matrix()
        self.stability = Stability(self.adjacency_matrix)
        self.stability.graph.plot_graph(True)

    def output_adjacency_matrix(self):
        """Виведення матриці суміжності у вікно інтерфейсу."""
        m, n = self.adjacency_matrix.shape
        if self.first_am_load:
            self.first_am_load = False
            self.adjacency_matrix_out.setRowCount(m)
            self.adjacency_matrix_out.setColumnCount(n)
            self.adjacency_matrix_out.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.adjacency_matrix_out.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

            for idx in range(m):
                item = QtWidgets.QTableWidgetItem(self.adjacency_matrix.columns[idx])
                self.adjacency_matrix_out.setHorizontalHeaderItem(idx, item)
                self.adjacency_matrix_out.setVerticalHeaderItem(idx, item)

        for row in range(m):
            for column in range(n):
                item = QtWidgets.QTableWidgetItem(str(self.adjacency_matrix.iloc[row, column]))
                self.adjacency_matrix_out.setItem(row, column, item)

    def execute_set_model_steps(self):
        """Встановити кількість кроків моделювання"""
        model_steps = self.impulse_modeling_steps.value()
        self.n_model_steps = model_steps

    def set_q_table(self, q_impulses=None):
        self.q_table.setRowCount(1)
        self.q_table.setColumnCount(len(self.adjacency_matrix.index))
        self.q_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.q_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for idx in range(len(self.adjacency_matrix.index)):
            item = QtWidgets.QTableWidgetItem(self.adjacency_matrix.columns[idx])
            self.q_table.setHorizontalHeaderItem(idx, item)
        self.q_table.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem('0'))
        if q_impulses is None:
            for i in range(len(self.adjacency_matrix.index)):
                item = QtWidgets.QTableWidgetItem(f'{0.}')
                self.q_table.setItem(0, i, item)
        else:
            for i in range(len(self.adjacency_matrix.index)):
                item = QtWidgets.QTableWidgetItem(f'{q_impulses.iloc[i, 0]}')
                self.q_table.setItem(0, i, item)

    def set_x_table(self):
        self.x_table.setRowCount(len(self.adjacency_matrix.index))
        self.x_table.setColumnCount(self.n_model_steps+1)
        self.x_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.x_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for idx in range(len(self.adjacency_matrix.index)):
            item = QtWidgets.QTableWidgetItem(self.adjacency_matrix.columns[idx])
            self.x_table.setVerticalHeaderItem(idx, item)
        for idx in range(self.n_model_steps+2):
            item = QtWidgets.QTableWidgetItem(f'{idx}')
            self.x_table.setHorizontalHeaderItem(idx, item)

    def read_q_impulses(self):
        """Зчитує з інтерфейсу значення імпульсів."""
        r = len(self.adjacency_matrix.index)
        c = self.n_model_steps+1
        q_impulses = pd.DataFrame(data=np.zeros((r, c)), index=self.adjacency_matrix.index,
                                  columns=list(range(self.n_model_steps + 1)))
        for i in range(len(self.adjacency_matrix.index)):
            q_impulses.iloc[i, 0] = float(self.q_table.item(0, i).text())

        self.q_impulses = q_impulses

    def impulse_modeling(self):
        if self.im_table.isChecked():
            self.value_impulse_modeling()
        elif self.im_graph.isChecked():
            self.plot_impulse_modeling()
        else:
            raise KeyError('Unknown type of impulse modeling!')

    def value_impulse_modeling(self):
        """Створити моделювання у табличному вигляді."""
        self.execute_set_model_steps()
        self.set_x_table()
        self.read_adjacency_matrix()
        self.read_q_impulses()
        ip = ImpulseProcess(self.adjacency_matrix, self.q_impulses.iloc[:, 0])
        ip.impulse_modeling(self.q_impulses, self.n_model_steps)
        x = ip.x
        for i in range(len(self.adjacency_matrix.index)):
            for j in range(self.n_model_steps+1):
                item = QtWidgets.QTableWidgetItem(f'{x.iloc[i, j]:.2f}')
                self.x_table.setItem(i, j, item)

    def plot_impulse_modeling(self):
        """Створити моделювання у графічному вигляді."""
        self.execute_set_model_steps()
        self.read_adjacency_matrix()
        self.read_q_impulses()
        ip = ImpulseProcess(self.adjacency_matrix, self.q_impulses.iloc[:, 0])
        ip.impulse_modeling(self.q_impulses, self.n_model_steps)
        ip.x.T.plot()
        plt.show()


def cognitive_analysis_execute():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = UI()
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    cognitive_analysis_execute()
