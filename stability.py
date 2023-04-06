import numpy as np
from scipy import linalg
from graphs import Graph


class Stability:

    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix.copy()
        self.graph = Graph(adjacency_matrix)
        self.eigenvalues = self.__get_eigenvalues()
        self.abs_eigenvalues = self.__get_abs_eigenvalues()
        self.spectral_radius = self.__get_spectral_radius()
        self.perturbation_stability = self.__get_perturbation_stability()
        self.value_stability = self.__get_value_stability()
        self.structure_stability = self.__get_structure_stability()

    def __get_eigenvalues(self):
        """Отримати власні числа матриці суміжності."""
        eigenvalues = linalg.eigvals(self.adjacency_matrix)
        return eigenvalues

    def __get_abs_eigenvalues(self):
        """Отримати модулі власних чисел матриці суміжності."""
        abs_eigenvalues = np.abs(self.eigenvalues)
        return abs_eigenvalues

    def __get_spectral_radius(self):
        """Отримати спектральний радіус матриці суміжності."""
        spectral_radius = np.max(self.abs_eigenvalues)
        return spectral_radius

    def __get_perturbation_stability(self):  # UNCHECKED!
        """Повертає True, якщо система стійка за збуренням; інакше False."""
        perturbation_stability = self.spectral_radius <= 1
        return perturbation_stability

    def __get_value_stability(self):  # UNCHECKED!
        """Повертає True, якщо система стійка за початковим значенням; інакше False."""
        value_stability = self.spectral_radius < 1
        return value_stability

    def __get_structure_stability(self):  # UNCHECKED!
        """Повертає True, якщо система структурно-стійка; інакше False."""
        structure_stability = len(self.graph.pair_cycles) == 0
        return structure_stability

    def get_stability(self):
        """Повертає True, якщо система стійка за всіми показниками; інакше False."""
        total_stability = self.perturbation_stability and self.value_stability and self.structure_stability
        return total_stability


