#!/usr/bin/python

import argparse

import analyzer
import graphics

if __name__ == '__main__':

    version = '0.1'

    CLI = argparse.ArgumentParser(description='Analyzes the architectural stability of a Swift project.')
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
        '--version',
        action='version',
        version='%(prog)s ' + version
    )

    args = CLI.parse_args()
    directory = args.source[0]
    exclude = args.exclude

    container = analyzer.Inspector(directory, exclude)

    # Detailed analysis per each framework
    for f in container.frameworks:
        print(container.framework_analysis(f), '----')

    # Distance from the main sequence plot
    data = container.instability_abstractness_data()
    graphics.plot_distance_main_sequence(data)
