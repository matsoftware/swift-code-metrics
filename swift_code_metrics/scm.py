#!/usr/bin/python3

from argparse import ArgumentParser

from ._helpers import Log
from ._analyzer import Inspector
from .version import VERSION
import sys


def main():
    CLI = ArgumentParser(description='Analyzes the code metrics of a Swift project.')
    CLI.add_argument(
        '--source',
        metavar='S',
        nargs='*',
        type=str,
        default='',
        required=True,
        help='The root path of the Swift project.'
    )
    CLI.add_argument(
        '--artifacts',
        nargs='*',
        type=str,
        default='',
        required=True,
        help='Path to save the artifacts generated'
    )
    CLI.add_argument(
        '--exclude',
        nargs='*',
        type=str,
        default=[],
        help='List of paths to exclude from analysis (e.g. submodules, pods, checkouts)'
    )
    CLI.add_argument(
        '--tests-paths',
        nargs='*',
        type=str,
        default=['Test', 'Tests'],
        help='List of paths that contains test classes and mocks.'
    )
    CLI.add_argument(
        '--generate-graphs',
        nargs='?',
        type=bool,
        const=True,
        default=False,
        help='Generates the graphic reports and saves them in the artifacts path.'
    )
    CLI.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + VERSION
    )

    args = CLI.parse_args()
    directory = args.source[0]
    exclude = args.exclude
    artifacts = args.artifacts[0]
    default_tests_paths = args.tests_paths
    should_generate_graphs = args.generate_graphs

    # Inspects the provided directory
    analyzer = Inspector(directory, artifacts, default_tests_paths, exclude)

    if not analyzer.analyze():
        Log.warn('No valid swift files found in the project')
        sys.exit(0)

    if not should_generate_graphs:
        sys.exit(0)

    # Creates graphs
    from ._graphs_renderer import GraphsRender
    non_test_frameworks = analyzer.filtered_frameworks(is_test=False)
    test_frameworks = analyzer.filtered_frameworks(is_test=True)
    graphs_renderer = GraphsRender(
        artifacts_path=artifacts,
        test_frameworks=test_frameworks,
        non_test_frameworks=non_test_frameworks,
        report=analyzer.report
    )
    graphs_renderer.render_graphs()
