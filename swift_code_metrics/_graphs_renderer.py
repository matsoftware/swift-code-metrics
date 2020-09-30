from ._metrics import Framework, Metrics
from ._report import Report, ReportingHelpers
from dataclasses import dataclass
from typing import List
from ._graphs_presenter import GraphPresenter


@dataclass
class GraphsRender:
    """
    Component responsible to generate the needed graphs for the given report.
    """
    artifacts_path: str
    test_frameworks: List['Framework']
    non_test_frameworks: List['Framework']
    report: 'Report'

    def render_graphs(self):
        graph_presenter = GraphPresenter(self.artifacts_path)

        # Sorted data plots
        non_test_reports_sorted_data = {
            'N. of classes and structs': lambda fr: fr.data.number_of_concrete_data_structures,
            'Lines Of Code - LOC': lambda fr: fr.data.loc,
            'Number Of Comments - NOC': lambda fr: fr.data.noc,
            'N. of imports - NOI': lambda fr: fr.number_of_imports
        }

        tests_reports_sorted_data = {
            'Number of tests - NOT': lambda fr: fr.data.number_of_tests
        }

        # Non-test graphs
        for title, framework_function in non_test_reports_sorted_data.items():
            graph_presenter.sorted_data_plot(title, self.non_test_frameworks, framework_function)

        # Distance from the main sequence
        all_frameworks = self.test_frameworks + self.non_test_frameworks
        graph_presenter.distance_from_main_sequence_plot(self.non_test_frameworks,
                                                         lambda fr: Metrics.instability(fr, all_frameworks),
                                                         lambda fr: Metrics.abstractness(fr))

        # Dependency graph
        graph_presenter.dependency_graph(self.non_test_frameworks,
                                         self.report.non_test_framework_aggregate.loc,
                                         self.report.non_test_framework_aggregate.n_o_i)

        # Code distribution
        graph_presenter.pie_plot('Code distribution', self.non_test_frameworks,
                                 lambda fr:
                                 ReportingHelpers.decimal_format(fr.data.loc
                                                                 / self.report.non_test_framework_aggregate.loc))

        # Test graphs
        for title, framework_function in tests_reports_sorted_data.items():
            graph_presenter.sorted_data_plot(title, self.test_frameworks, framework_function)


