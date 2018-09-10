import _graphics


class GraphPresenter:
    def __init__(self, artifacts_path):
        self.graph = _graphics.Graph(artifacts_path)

    def sorted_data_plot(self, title, list_of_frameworks, f_of_framework):
        """
        Renders framework related data to a bar plot.
        """
        sorted_data = sorted(list(map(lambda f: (f_of_framework(f),
                                                 f.compact_name(),
                                                 f.compact_name_description()), list_of_frameworks)),
                             key=lambda tup: tup[0])
        plot_data = (list(map(lambda f: f[0], sorted_data)),
                     list(map(lambda f: f[1], sorted_data)),
                     list(map(lambda f: f[2], sorted_data)))

        self.graph.bar_plot(title, plot_data)

    def distance_from_main_sequence_plot(self, list_of_frameworks, x_ax_f_framework, y_ax_f_framework):
        """
        Renders framework related data to a scattered plot
        """
        scattered_data = (list(map(lambda f: x_ax_f_framework(f), list_of_frameworks)),
                          list(map(lambda f: y_ax_f_framework(f), list_of_frameworks)),
                          list(map(lambda f: f.name, list_of_frameworks)))

        bands = [
            ([1, 0], 'g'),
            ([0.66, -0.34], 'y--'),
            ([1.34, 0.34], 'y--'),
            ([0.34, -0.66], 'r--'),
            ([1.66, 0.66], 'r--')
        ]

        self.graph.scattered_plot('Deviation from the main sequence',
                                  'I = Instability',
                                  'A = Abstractness',
                                  scattered_data,
                                  bands)
