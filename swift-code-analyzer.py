#!/usr/bin/python

import argparse

import analyzer
import graphics

if __name__ == '__main__':

    version = '0.2'

    CLI = argparse.ArgumentParser(description='Analyzes the code metrics of a Swift project.')
    CLI.add_argument(
        'source',
        metavar='S',
        nargs='*',
        type=str,
        help='The root path of the Swift project.'
    )
    CLI.add_argument(
        '--exclude',
        nargs='*',
        type=str,
        default=[],
        help='List of paths to exclude from analysis (e.g. submodules, pods, checkouts)'
    )
    CLI.add_argument(
        '--artifacts',
        nargs='*',
        type=str,
        default=None,
        help='Path to save the graphic artifacts generated'
    )
    CLI.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + version
    )

    args = CLI.parse_args()
    directory = args.source[0]
    exclude = args.exclude
    artifacts = args.artifacts[0]

    analyzer = analyzer.Inspector(directory, exclude)

    # Detailed analysis per each framework
    for f in analyzer.frameworks:
        print(analyzer.framework_analysis(f))
        print('----')


    graph = graphics.Graph(artifacts)

    # Size
    size_data = analyzer.components_classes_size_data()
    graph.bar_plot('N. of classes and structs', size_data)

    # LOC
    loc_data = analyzer.loc_data()
    graph.bar_plot('Lines Of Code (LOC)', loc_data)

    # NOC
    noc_data = analyzer.noc_data()
    graph.bar_plot('Number Of Comments (NOC)', noc_data)

    # Number of methods
    methods_data = analyzer.methods_size_data()
    graph.bar_plot('N. of methods (NBM)', methods_data)

    # Instability
    instability_data = analyzer.instability_data()
    graph.bar_plot('Instability', instability_data)

    # Abstractness
    abstractness_data = analyzer.abstractness_data()
    graph.bar_plot('Abstractness', abstractness_data)

    # Distance from the main sequence plot
    d3_data = analyzer.instability_abstractness_data()
    graph.plot_distance_main_sequence(d3_data)
