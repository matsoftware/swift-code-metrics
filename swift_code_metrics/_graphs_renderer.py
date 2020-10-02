from ._metrics import Metrics, SubModule
from ._report import ReportingHelpers
from dataclasses import dataclass
from typing import List
from ._graphs_presenter import GraphPresenter


@dataclass
class GraphsRender:
    "Component responsible to generate the needed graphs for the given report."
    artifacts_path: str
    test_frameworks: List['Framework']
    non_test_frameworks: List['Framework']
    report: 'Report'

    def render_graphs(self):
        graph_presenter = GraphPresenter(self.artifacts_path)

        # Project graphs
        self.__project_graphs(graph_presenter=graph_presenter)

        # Submodules graphs
        self.__submodules_graphs(graph_presenter=graph_presenter)

    def __project_graphs(self, graph_presenter: 'GraphPresenter'):
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
        graph_presenter.frameworks_pie_plot('Code distribution', self.non_test_frameworks,
                                            lambda fr:
                                            ReportingHelpers.decimal_format(fr.data.loc
                                                                            / self.report.non_test_framework_aggregate.loc))

        # Test graphs
        for title, framework_function in tests_reports_sorted_data.items():
            graph_presenter.sorted_data_plot(title, self.test_frameworks, framework_function)

    def __submodules_graphs(self, graph_presenter: 'GraphPresenter'):
        for framework in self.non_test_frameworks:
            GraphsRender.__render_submodules(parent='Code distribution',
                                             root_submodule=framework.submodule,
                                             graph_presenter=graph_presenter)

    @staticmethod
    def __render_submodules(parent: str, root_submodule: 'SubModule', graph_presenter: 'GraphPresenter'):
        current_submodule = root_submodule.next
        while current_submodule != root_submodule:
            GraphsRender.__render_submodule_loc(parent=parent,
                                                submodule=current_submodule,
                                                graph_presenter=graph_presenter)
            current_submodule = current_submodule.next

    @staticmethod
    def __render_submodule_loc(parent: str, submodule: 'SubModule', graph_presenter: 'GraphPresenter'):
        submodules = submodule.submodules
        if len(submodules) == 0:
            return
        total_loc = submodule.data.loc
        if total_loc == submodules[0].data.loc:
            # Single submodule folder - not useful
            return
        if len(submodule.files) > 0:
            # Add a submodule to represent the root slice
            submodules = submodules + [SubModule(name='(root)',
                                                 files=submodule.files,
                                                 submodules=[],
                                                 parent=submodule)]

        chart_name = f'{parent} {submodule.path}'
        graph_presenter.submodules_pie_plot(chart_name, submodules,
                                            lambda s: ReportingHelpers.decimal_format(s.data.loc / total_loc))
