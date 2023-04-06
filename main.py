from tkinter import *
from tkinter import filedialog

import pandas
from pandastable import Table, TableModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from cognitive_matrix import Stability
from impulse_modeling import ImpulseProcess


class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title('Лабораторна робота 6')
        self.resizable(False, False)

        self.options_frame = Frame(self)
        self.options_frame.pack(side='left', fill='both', expand=True)

        self.matrices_frame = Frame(self)
        self.matrices_frame.pack(side='right', fill='both', expand=True)

        # 'Файли'
        self.files_label_frame = LabelFrame(self.options_frame, text='Файли:')
        self.files_label_frame.grid(row=0, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        self.input_matrix_label = Label(self.files_label_frame, text='Файл з матрицею:')
        self.input_matrix_label.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.input_matrix_path_var = StringVar()
        self.input_matrix_path_var.set('')
        self.input_matrix_path_entry = Entry(self.files_label_frame, textvariable=self.input_matrix_path_var,
                                             state=DISABLED, disabledbackground='white', disabledforeground='black')
        self.input_matrix_path_entry.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

        self.browse_input_button = Button(self.files_label_frame, text='...', command=self.open_input_matrix)
        self.browse_input_button.grid(row=0, column=2, sticky='WE', padx=5, pady=2)

        self.output_matrix_label = Label(self.files_label_frame, text='Файл з результатами:')
        self.output_matrix_label.grid(row=1, column=0, sticky='E', padx=5, pady=2)

        self.output_matrix_path_var = StringVar()
        self.output_matrix_path_var.set('output')
        self.output_matrix_path_entry = Entry(self.files_label_frame, textvariable=self.output_matrix_path_var)
        self.output_matrix_path_entry.grid(row=1, column=1, sticky='WE', padx=5, pady=2)

        self.browse_output_button = Button(self.files_label_frame, text='...', command=self.open_output_matrix)
        self.browse_output_button.grid(row=1, column=2, sticky='WE', padx=5, pady=2)

        # 'Імпульс'
        self.impulse_label_frame = LabelFrame(self.options_frame, text='Імпульс:')
        self.impulse_label_frame.grid(row=1, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        self.iterations_label = Label(self.impulse_label_frame, text='Кількість ітерацій:')
        self.iterations_label.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.iterations_var = StringVar()
        self.iterations_var.set('5')
        self.iterations_spinbox = Spinbox(self.impulse_label_frame, from_=1, to=20, width=30,
                                          textvariable=self.iterations_var)
        self.iterations_spinbox.grid(row=0, column=1, columnspan=2, sticky='WE', padx=5, pady=2)

        self.calculate_button = Button(self.impulse_label_frame, text='Змоделювати',
                                       command=self.model_impulse,
                                       bg='red',
                                       fg='white'
                                       )
        self.calculate_button.grid(row=1, column=0, columnspan=3, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        # 'Стійкість'
        self.sustainability_label_frame = LabelFrame(self.options_frame, text='Стійкість:')
        self.sustainability_label_frame.grid(row=2, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5,
                                             ipady=5)

        self.check_sustainability_button = Button(self.sustainability_label_frame, text='Перевірити стійкість',
                                                  command=self.check_sustainability,
                                                  bg='red',
                                                  fg='white'
                                                  )
        self.check_sustainability_button.grid(row=0, column=0, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.values_sustainability_checkbutton = Checkbutton(self.sustainability_label_frame,
                                                             text='Стійкість за значенням', state='disabled')
        self.values_sustainability_checkbutton.config(disabledforeground="black")
        self.values_sustainability_checkbutton.grid(row=1, column=0, sticky='W', padx=5, pady=2)

        self.disturbance_sustainability_checkbutton = Checkbutton(self.sustainability_label_frame,
                                                                  text='Стійкість за збуренням', state='disabled')
        self.disturbance_sustainability_checkbutton.config(disabledforeground="black")

        self.disturbance_sustainability_checkbutton.grid(row=2, column=0, sticky='W', padx=5, pady=2)

        self.structure_sustainability_checkbutton = Checkbutton(self.sustainability_label_frame,
                                                                text='Структурна стійкість', state='disabled')
        self.structure_sustainability_checkbutton.config(disabledforeground="black")

        self.structure_sustainability_checkbutton.grid(row=3, column=0, sticky='W', padx=5, pady=2)

        ## 'Цикли'
        self.cycles_label_frame = LabelFrame(self.sustainability_label_frame, text='Цикли')
        self.cycles_label_frame.grid(row=4, column=0, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        self.cycles_number_label = Label(self.cycles_label_frame, text='Кількість парних циклів:')
        self.cycles_number_label.grid(row=0, column=0, sticky='WE', padx=5, pady=2)

        self.cycles_number_entry = Entry(self.cycles_label_frame)
        self.cycles_number_entry.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

        self.cycles_listbox = Listbox(self.cycles_label_frame)
        self.cycles_listbox.grid(row=1, column=0, columnspan=2, sticky='WE', padx=5, pady=2)

        ## 'Власні числа'
        self.eigenvalues_label_frame = LabelFrame(self.sustainability_label_frame, text='Власні числа:')
        self.eigenvalues_label_frame.grid(row=5, column=0, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        self.max_eigenvalues_label = Label(self.eigenvalues_label_frame, text='Найбільше власне число:')
        self.max_eigenvalues_label.grid(row=0, column=0, sticky='WE', padx=5, pady=2)

        self.max_eigenvalues_entry = Entry(self.eigenvalues_label_frame)
        self.max_eigenvalues_entry.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

        self.eigenvalues_listbox = Listbox(self.eigenvalues_label_frame)
        self.eigenvalues_listbox.grid(row=1, column=0, columnspan=2, sticky='WE', padx=5, pady=2)

        # 'Оригінальна матриця'
        self.adjacent_matrix_label_frame = LabelFrame(self.matrices_frame, text='Матриця суміжності:')
        self.adjacent_matrix_label_frame.grid(row=0, column=3, rowspan=2)

        self.adjacent_matrix_table = Table(self.adjacent_matrix_label_frame, height=231)
        self.adjacent_matrix_table.show()

        # 'Ітерації'
        self.impulse_matrix_label_frame = LabelFrame(self.matrices_frame, text='Ітерації:')
        self.impulse_matrix_label_frame.grid(row=2, column=3, rowspan=2)

        self.impulse_matrix_table = Table(self.impulse_matrix_label_frame, height=231)
        self.impulse_matrix_table.show()

        # 'Вектор збурення'
        self.disturbance_vector_label_frame = LabelFrame(self.matrices_frame, text='Вектор збурення:')
        self.disturbance_vector_label_frame.grid(row=4, column=3, rowspan=2)

        self.disturbance_vector_table = Table(self.disturbance_vector_label_frame, height=231)
        self.disturbance_vector_table.show()

    def open_input_matrix(self):
        input_matrix_path = filedialog.askopenfilename(title='Open a File',
                                                       filetypes=(("Excel files", ".*xlsx"), ("All Files", "*.")))
        self.input_matrix_path_var.set(input_matrix_path)
        self.adjacent_matrix = pandas.read_excel(input_matrix_path, index_col=0)
        self.adjacent_matrix_table.updateModel(TableModel(self.adjacent_matrix))
        self.adjacent_matrix_table.redraw()

        self.disturbance_vector = pd.DataFrame([[0]] * self.adjacent_matrix.shape[1], index=self.adjacent_matrix.index)
        self.disturbance_vector_table.updateModel(TableModel(self.disturbance_vector))
        self.disturbance_vector_table.redraw()

    def open_output_matrix(self):
        output_matrix_path = filedialog.askopenfilename(title='Open a File',
                                                        filetypes=(("Excel files", ".*xlsx"), ("All Files", "*.")))
        self.output_matrix_path_var.set(output_matrix_path)

    def check_sustainability(self):
        adjacent_matrix = self.adjacent_matrix.copy()
        self.stability = Stability(adjacent_matrix)

        if self.stability.structure_stability:
            self.values_sustainability_checkbutton.select()
        else:
            self.values_sustainability_checkbutton.deselect()

        if self.stability.value_stability:
            self.disturbance_sustainability_checkbutton.select()
        else:
            self.disturbance_sustainability_checkbutton.deselect()

        if self.stability.value_stability:
            self.structure_sustainability_checkbutton.select()
        else:
            self.structure_sustainability_checkbutton.deselect()

        self.cycles_number_entry.delete(0, END)
        self.cycles_number_entry.insert(END, str(len(self.stability.graph.pair_cycles)))

        items_list = []
        for pc in self.stability.graph.pair_cycles:
            pc.append(pc[0])
            pc = '~>'.join(f'{e}' for e in pc)
            items_list.append(pc)
        items_list = sorted(items_list, key=len)
        for pc in items_list:
            self.cycles_listbox.insert(END, pc)

        self.max_eigenvalues_entry.delete(0, END)
        self.max_eigenvalues_entry.insert(END, f'{self.stability.spectral_radius:.2f}')

        self.eigenvalues_listbox.delete(0, END)
        for ev in self.stability.eigenvalues:
            self.eigenvalues_listbox.insert(END, '{0:.2f} {1} {2:.2f}i'.format(ev.real, '+-'[int(ev.imag < 0)],
                                                                               abs(ev.imag)))

    def model_impulse(self):
        n_steps = int(self.iterations_var.get())
        q_impulses = pd.DataFrame(data=np.zeros((self.adjacent_matrix.shape[0], n_steps + 1)),
                                  index=self.adjacent_matrix.columns,
                                  columns=list(range(n_steps + 1)))

        q_impulses.iloc[:, 0] = self.disturbance_vector.iloc[:, 0].astype(float)
        ip = ImpulseProcess(self.adjacent_matrix, q_impulses.iloc[:, 0])
        ip.impulse_modeling(q_impulses, n_steps)
        x = ip.x
        self.impulse_matrix_table.updateModel(TableModel(x))
        self.impulse_matrix_table.redraw()
        x.T.plot()
        plt.show()

        x.to_excel(
            '\\'.join(self.input_matrix_path_var.get().split('\\')[:-1]) + self.output_matrix_path_var.get() + '.xlsx')


if __name__ == "__main__":
    application = Application()
    application.mainloop()
