import unittest
from swift_code_metrics._graph_helpers import Graph


class GraphHelpersTests(unittest.TestCase):

    def test_pie_labels_hides_small_slices(self):
        pie_labels, legend_labels = Graph.pie_labels([1, 2, 97], ['A', 'B', 'C'], ['A(a)', 'B(b)', 'C(c)'])
        self.assertEqual(['', '', 'C'], pie_labels)
        self.assertEqual(['A(a) (1.0%)', 'B(b) (2.0%)', 'C(c) (97.0%)'], legend_labels)

    def test_pie_labels_zero_total(self):
        pie_labels, legend_labels = Graph.pie_labels([0], ['A'], ['A'])
        self.assertEqual([''], pie_labels)
        self.assertEqual(['A (0.0%)'], legend_labels)


if __name__ == '__main__':
    unittest.main()
