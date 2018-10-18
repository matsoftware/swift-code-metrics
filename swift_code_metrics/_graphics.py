import string

import matplotlib.pyplot as plt
import os

from adjustText import adjust_text


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

    def pie_plot(self, title, labels, sizes):
        plt.title(title)
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
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

    # Private

    def __render(self, plt, name):
        if self.path is None:
            plt.show()
        else:
            filename = Graph.format_filename(name) + '.pdf'
            save_file = os.path.join(self.path, filename)
            plt.savefig(save_file)
            plt.close()

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


