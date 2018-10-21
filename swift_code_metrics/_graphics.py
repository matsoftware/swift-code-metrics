import string

import matplotlib.pyplot as plt
import os

from adjustText import adjust_text
import pygraphviz as pgv


class Graph:
    def __init__(self, path=None):
        self.path = path

    def bar_plot(self, title, data):
        plt.title(title)
        plt.ylabel(title)
        bar_width = 0.35
        opacity = 0.4
        plotted_data = plt.bar(data[1], data[0], bar_width, alpha=opacity)
        plt.legend(plotted_data, data[2], loc='upper left')

        self.__render(plt, title)

    def pie_plot(self, title, sizes, labels, legend):
        plt.title(title)
        patches, texts, _ = plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(patches, legend, loc="best")
        plt.tight_layout()
        plt.axis('equal')

        self.__render(plt, title)

    def scattered_plot(self, title, x_label, y_label, data, bands):
        plt.title(title)
        plt.axis([0, 1, 0, 1])
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # Data
        x = data[0]
        y = data[1]
        labels = data[2]

        # Bands
        for band in bands:
            plt.plot(band[0], band[1])

        # Plot
        texts = []
        for i, label in enumerate(labels):
            plt.plot(x, y, 'ko', label=label)
            texts.append(plt.text(x[i], y[i], label, size=8))

        adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))

        self.__render(plt, title)

    def directed_graph(self, title, list_of_edges):
        dir_graph = pgv.AGraph(directed=True, strict=True, rankdir='TD', name=title)
        dir_graph.node_attr['shape'] = 'rectangle'
        dir_graph.node_attr['size'] = '10'
        for e in list_of_edges:
            dir_graph.add_edge(e[0], e[1], label=e[2])

        dir_graph.layout('dot')
        dir_graph.draw(self.__file_path(title))

    # Private

    def __render(self, plt, name):
        if self.path is None:
            plt.show()
        else:
            save_file = self.__file_path(name)
            plt.savefig(save_file)
            plt.close()

    def __file_path(self, name):
        filename = Graph.format_filename(name) + '.pdf'
        return os.path.join(self.path, filename)

    @staticmethod
    def format_filename(s):
        """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    https://gist.github.com/seanh/93666

    """
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ', '_').lower()
        return filename


