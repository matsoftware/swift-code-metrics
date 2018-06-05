import matplotlib.pyplot as plt

def plot_instability(data):
    plt.title('Instability')
    plt.ylabel('Instability')
    bar_width = 0.35
    opacity = 0.4
    plotted_data = plt.bar(data[1], data[0], bar_width, alpha=opacity)
    plt.legend(plotted_data, data[2], loc='upper left')

    plt.show()

def plot_distance_main_sequence(data):
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
        plt.plot(x, y, 'ko', label=data[3][i])
        plt.annotate(label, (x[i], y[i]))

    plt.legend(bbox_to_anchor=(0, 1.1, 1, 1.1), loc="lower left", mode="expand", ncol=4)

    plt.show()

