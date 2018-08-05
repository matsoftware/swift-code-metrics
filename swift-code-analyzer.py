#!/usr/bin/python

import argparse
import analyzer
import presenter

if __name__ == '__main__':

    version = '0.3'

    CLI = argparse.ArgumentParser(description='Analyzes the code metrics of a Swift project.')
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
    artifacts = None if args.artifacts is None else args.artifacts[0]

    # Inspects the provided directory
    analyzer = analyzer.Inspector(directory, exclude)

    # Prints out the detailed analysis
    text_presenter = presenter.TextPresenter(artifacts)
    for f in analyzer.frameworks:
        text_presenter.render(analyzer.framework_analysis(f))
        text_presenter.render('----')
    text_presenter.render(analyzer.global_frameworks_data())
    text_presenter.close()

    # Creates graphs
    graph_presenter = presenter.GraphPresenter(artifacts)

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
