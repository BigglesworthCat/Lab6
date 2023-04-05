from tkinter import *
from tkinter import filedialog

import pandas
from pandastable import Table, TableModel
import pandas as pd

from cognitive_matrix import Stability
from impulse_modeling import ImpulseProcess

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title('Лабораторна робота 4')
        # self.resizable(False, False)

        # 'Файли'
        self.files_label_frame = LabelFrame(self, text='Файли:')
        self.files_label_frame.grid(row=0, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        self.input_matrix_label = Label(self.files_label_frame, text='Файл з матрицею:')
        self.input_matrix_label.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.input_matrix_path_var = StringVar()
        self.input_matrix_path_var.set('')
        self.input_matrix_path_entry = Entry(self.files_label_frame, textvariable=self.input_matrix_path_var)
        self.input_matrix_path_entry.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

        self.browse_button = Button(self.files_label_frame, text='...', command=self.open_input_matrix)
        self.browse_button.grid(row=0, column=2, sticky='W', padx=5, pady=2)

        self.output_matrix_label = Label(self.files_label_frame, text='Файл з результатами:')
        self.output_matrix_label.grid(row=1, column=0, sticky='E', padx=5, pady=2)

        self.output_matrix_path = StringVar()
        self.output_matrix_path.set('')
        self.output_matrix_path_entry = Entry(self.files_label_frame, textvariable=self.output_matrix_path)
        self.output_matrix_path_entry.grid(row=1, column=1, sticky='WE', padx=5, pady=2)

        self.output_button = Button(self.files_label_frame, text='...', command=self.open_input_matrix)
        self.output_button.grid(row=1, column=2, sticky='W', padx=5, pady=2)

        # 'Імпульс'
        self.impulse_label_frame = LabelFrame(self, text='Імпульс:')
        self.impulse_label_frame.grid(row=1, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        self.iterations_label = Label(self.impulse_label_frame, text='Кількість ітерацій:')
        self.iterations_label.grid(row=0, column=0, sticky='WE', padx=5, pady=2)
        self.iterations_var = StringVar()
        self.iterations_var.set('3')
        self.iterations_spinbox = Spinbox(self.impulse_label_frame, from_=1, to=20, width=5,
                                          textvariable=self.iterations_var)
        self.iterations_spinbox.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

        self.calculate_button = Button(self.impulse_label_frame, text='Змоделювати',
                                       command=self.model_impulse,
                                       bg='red',
                                       fg='white'
                                       )
        self.calculate_button.grid(row=1, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5, ipady=5)

        # 'Стійкість'
        self.sustainability_label_frame = LabelFrame(self, text='Стійкість:')
        self.sustainability_label_frame.grid(row=2, column=0, columnspan=3, sticky='NWES', padx=5, pady=5, ipadx=5,
                                             ipady=5)

        self.check_sustainability_button = Button(self.sustainability_label_frame, text='Перевірити стійкість',
                                                  command=self.check_sustainability,
                                                  bg='red',
                                                  fg='white'
                                                  )
        self.check_sustainability_button.grid(row=0, column=0, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.values_sustainability_checkbutton = Checkbutton(self.sustainability_label_frame,
                                                             text='Стійкість за значенням')
        self.values_sustainability_checkbutton.grid(row=1, column=0, sticky='W', padx=5, pady=2)

        self.disturbance_sustainability_checkbutton = Checkbutton(self.sustainability_label_frame,
                                                                  text='Стійкість за збуренням')
        self.disturbance_sustainability_checkbutton.grid(row=2, column=0, sticky='W', padx=5, pady=2)

        self.structure_sustainability_checkbutton = Checkbutton(self.sustainability_label_frame,
                                                                text='Структурна стійкість')
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
        self.adjacent_matrix_label_frame = LabelFrame(self, text='Матриця суміжності:')
        self.adjacent_matrix_label_frame.grid(row=0, column=3, columnspan=3)

        self.adjacent_matrix = Table(self.adjacent_matrix_label_frame)
        self.adjacent_matrix.show()
        self.adjacent_matrix.model.df = TableModel.getSampleData()

        # 'Імпульси'
        self.impulse_matrix_label_frame = LabelFrame(self, text='Ітерації:')
        self.impulse_matrix_label_frame.grid(row=1, column=3, columnspan=3)

        self.impulse_matrix = Table(self.impulse_matrix_label_frame)
        
        self.impulse_matrix.updateModel(TableModel(pd.DataFrame([[1]*8]*8)))
        self.impulse_matrix.show()

        # 'Вектор збурення'
        self.disturbance_vector_label_frame = LabelFrame(self, text='Вектор збурення:')
        self.disturbance_vector_label_frame.grid(row=2, column=3, columnspan=3)


        disturbance_vector = pd.DataFrame([[0]]*8)
        self.disturbance_vector = Table(self.disturbance_vector_label_frame)
        self.disturbance_vector.updateModel(TableModel(disturbance_vector))
        
        self.disturbance_vector.show()

    def open_input_matrix(self):
        input_matrix_path = filedialog.askopenfilename(title='Open a File',
                                                  filetypes=(("Excel files", ".*xlsx"), ("All Files", "*.")))
        self.input_matrix_path_var.set(input_matrix_path)
        self.input_df = pandas.read_excel(input_matrix_path)
        self.input_df = self.input_df.drop(columns=['Unnamed: 0'])
        self.adjacent_matrix.updateModel(TableModel(self.input_df))
        self.adjacent_matrix.redraw()
        
        self.disturbance_vector_df = pd.DataFrame([[0]]*self.input_df.shape[1])
        self.disturbance_vector.updateModel(TableModel(self.disturbance_vector_df))
        self.disturbance_vector.redraw()
        
    def check_sustainability(self):
        pass

    def model_impulse(self):
        self.value_impulse_modeling()

    def value_impulse_modeling(self):
        """Створити моделювання у табличному вигляді."""
        import numpy as np
        n_steps = int(self.iterations_var.get())
        q_impulses = pd.DataFrame(data=np.zeros((self.input_df.shape[0], n_steps+1)), index=self.input_df.index,
                                columns=list(range(n_steps + 1)))
        
        # q_impulses.iloc[:, 0] = self.disturbance_vector_df.iloc[:, 0]
        print(q_impulses.shape,self.input_df.shape)
        ip = ImpulseProcess(self.input_df, q_impulses.iloc[:, 0])
        ip.impulse_modeling(q_impulses, n_steps)

        x = ip.x
        # df_output = pd.DataFrame(np.zeros(len(self.adjacency_matrix.index,self.n_model_steps+1)))
        # for i in range(len(self.adjacency_matrix.index)):
        #     for j in range(self.n_model_steps+1):
        #         # item = QtWidgets.QTableWidgetItem(f'{x.iloc[i, j]:.2f}')
        #         # self.x_table.setItem(i, j, item)
        #         df_output.iloc[i,j]
        self.impulse_matrix.updateModel(TableModel(x))
        self.impulse_matrix.redraw()
    
if __name__ == "__main__":
    application = Application()
    application.mainloop()
