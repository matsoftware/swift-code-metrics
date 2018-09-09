#!/usr/bin/python

from argparse import ArgumentParser
from analyzer import Inspector
from presenter import GraphPresenter
import sys

if __name__ == '__main__':

    version = '0.5'

    CLI = ArgumentParser(description='Analyzes the code metrics of a Swift project.')
    CLI.add_argument(
        'source',
        metavar='S',
        nargs='*',
        type=str,
        default='',
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
        help='Path to save the artifacts generated'
    )
    CLI.add_argument(
        '--generate-reports',
        nargs='*',
        type=bool,
        default=False,
        help='Output the reports to the artifacts path.'
    )
    CLI.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + version
    )

    args = CLI.parse_args()
    directory = args.source[0]
    exclude = args.exclude
    artifacts = None if args.artifacts is None else args.artifacts[0]
    should_generate_reports = False if args.generate_reports is None else True

    # Inspects the provided directory
    analyzer = Inspector(directory, artifacts, exclude)

    if not should_generate_reports:
        sys.exit(0)

    # Creates graphs
    graph_presenter = GraphPresenter(artifacts)

    # Sorted data plots
    sorted_data = {
        'N. of classes and structs': lambda fr: fr.number_of_concrete_data_structures,
        'Lines Of Code (LOC)': lambda fr: fr.loc,
        'Number Of Comments (NOC)': lambda fr: fr.noc,
        'N. of methods (NBM)': lambda fr: fr.number_of_methods,
        'Instability (I)': lambda fr: analyzer.instability(fr),
        'Abstractness (A)': lambda fr: analyzer.abstractness(fr),
    }

    for title, framework_function in sorted_data.items():
        graph_presenter.sorted_data_plot(title, analyzer.frameworks, framework_function)

    # Distance from the main sequence
    graph_presenter.distance_from_main_sequence_plot(analyzer.frameworks,
                                                     lambda fr: analyzer.instability(fr),
                                                     lambda fr: analyzer.abstractness(fr))
