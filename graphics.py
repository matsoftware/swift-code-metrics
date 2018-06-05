import matplotlib.pyplot as plt
import os

class Graph:
    def __init__(self, path=None):
        self.path = path

    def plot_instability(self, data):
        plt.title('Instability')
        plt.ylabel('Instability')
        bar_width = 0.35
        opacity = 0.4
        plotted_data = plt.bar(data[1], data[0], bar_width, alpha=opacity)
        plt.legend(plotted_data, data[2], loc='upper left')

        self.__render(plt, 'instability')

    def plot_distance_main_sequence(self, data):
        plt.title('Deviation from main sequence')
        plt.axis([0, 1, 0, 1])
        plt.ylabel('A = Abstractness')
        plt.xlabel('I = Instability')

        # Data
        x = data[0]
        y = data[1]
        labels = data[2]

        # Bands
        plt.plot([1, 0], 'g')

        plt.plot([0.66, -0.34], 'y--')
        plt.plot([1.34, 0.34], 'y--')

        plt.plot([0.34, -0.66], 'r--')
        plt.plot([1.66, 0.66], 'r--')

        # Plot
        for i, label in enumerate(labels):
            plt.plot(x, y, 'ko', label=label)
            plt.annotate(label, (x[i], y[i]))

        self.__render(plt, 'deviation_main_sequence')

    # Private

    def __render(self, plt, name):
        if self.path is None:
            plt.show()
        else:
            filename = name + '.pdf'
            save_file = os.path.join(self.path, filename)
            plt.savefig(save_file)
            plt.close()


