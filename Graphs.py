import matplotlib.pyplot as plt

def plot_distance_main_sequence(data):
    plt.close('all')

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
    plt.plot(x, y, 'ko')
    for i, label in enumerate(labels):
        plt.annotate(label, (x[i], y[i]))

    plt.show()

