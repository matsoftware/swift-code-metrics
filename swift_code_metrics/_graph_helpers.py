import string

import matplotlib.pyplot as plt
import os
from functional import seq
from adjustText import adjust_text
from math import ceil
import pygraphviz as pgv
import numpy as np


class Graph:
    def __init__(self, path=None):
        self.path = path
        plt.rc('legend', fontsize='small')

    def bar_plot(self, title, data):
        plt.title(title)
        plt.ylabel(title)
        opacity = 0.8
        _ = plt.barh(data[1], data[0], color='blue', alpha=opacity)
        index = np.arange(len(data[1]))
        plt.yticks(index, data[1], fontsize=5, rotation=30)
        self.__render(plt, title)

    def pie_plot(self, title, sizes, labels, legend):
        plt.title(title)
        patches, _, _ = plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(patches, legend, loc='best')
        plt.axis('equal')
        plt.tight_layout()

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

    def directed_graph(self, title, list_of_nodes, list_of_edges):
        dir_graph = pgv.AGraph(directed=True, strict=True, rankdir='TD', name=title)
        dir_graph.node_attr['shape'] = 'rectangle'

        seq(list_of_nodes).for_each(lambda n: dir_graph.add_node(n[0],
                                                                 penwidth=ceil((n[1] + 1) / 2), width=(n[1] + 1)))
        seq(list_of_edges).for_each(
            lambda e: dir_graph.add_edge(e[0], e[1],
                                         label=e[2],
                                         penwidth=ceil((e[3] + 1) / 2),
                                         color=e[4],
                                         fontcolor=e[4]))

        dir_graph.layout('dot')
        try:
            dir_graph.draw(self.__file_path(title))
        except OSError:
            # Fallback for minimal graphviz setup
            dir_graph.draw(self.__file_path(title, extension='.svg'))

    # Private

    def __render(self, plt, name):
        if self.path is None:
            plt.show()
        else:
            save_file = self.__file_path(name)
            plt.savefig(save_file, bbox_inches='tight')
            plt.close()

    def __file_path(self, name, extension='.pdf'):
        filename = Graph.format_filename(name) + extension
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
