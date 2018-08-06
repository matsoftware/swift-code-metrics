import unittest
import analyzer

class AnalyzerTest(unittest.TestCase):

    def setUp(self):
        self.analyzer = analyzer.Inspector(
            directory="resources/ExampleProject/SwiftCodeMetricsExample",
            exclude_paths=["Test"]
        )


    def test_inspector_global_frameworks_data(self):
        expected_data = f'''
Aggregate data:
LOC = 97
NOC = 35
POC = 27% 
Na = 1
Nc = 7
NBM = 10
'''
        self.assertEqual(expected_data, self.analyzer.global_frameworks_data())


    def test_inspector_framework_analysis(self):
        expected_data_bb = f'''
Architectural analysis for BusinessLogic (BL): 

LOC = 49
NOC = 7
POC = 12% (under commented)
Fan In = 1
Fan Out = 2
Instability = 0.6666666666666666

Na = 0
Nc = 3
A = 0.0

D3 = 0.33333333333333337

NBM = 3

Low abstract component, few interfaces.

'''
        bb_framework = list(filter(lambda fr: fr.name == 'BusinessLogic', self.analyzer.frameworks))[0]
        self.assertEqual(expected_data_bb, self.analyzer.framework_analysis(bb_framework))


if __name__ == '__main__':
    unittest.main()
