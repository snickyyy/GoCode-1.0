import time
import unittest


class TestCase(unittest.TestCase):
    def __init__(self, func, methodName='runTest'):
        self.two_sum = func
        super().__init__(methodName)  # Указываем метод теста

    def setUp(self):
        pass

    def test_example_case(self):
        result = self.two_sum(nums=[2, 7, 11, 15], target=9)
        self.assertEqual(result, [0, 1])

    def test_multiple_pairs(self):
        result = self.two_sum(nums=[1, 2, 3, 4, 5], target=6)
        self.assertIn(result, [[1, 3], [0, 4]])

    def test_no_solution(self):
        result = self.two_sum(nums=[1, 2, 3, 4], target=10)
        self.assertEqual(result, [])

    def test_negative_numbers(self):
        result = self.two_sum(nums=[-3, 4, 3, 90], target=0)
        self.assertEqual(result, [0, 2])

    def test_single_pair(self):
        result = self.two_sum(nums=[3, 3], target=6)
        self.assertEqual(result, [0, 1])

    def test_timeout(self):
        result = self.get_time_test(self.two_sum, nums=[i for i in range(1000)], target=18)
        self.assertLess(result, 10)

    def get_time_test(self, func, **kwargs):
        start_time = time.time()
        func(**kwargs)
        end_time = time.time()
        return end_time - start_time

    @staticmethod
    def run_tests(func):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        test_names = loader.getTestCaseNames(TestCase)

        for test_name in test_names:
            suite.addTest(TestCase(func, test_name))

        result = unittest.TextTestRunner(failfast=True, buffer=True).run(suite)
        return {
            "status": result.wasSuccessful(),
            "errors": [str(i) for i in result.errors][-1] if result.errors else [],
            "failures": [str(i) for i in result.failures][-1] if result.failures else [],
            "total_tests": result.testsRun,
            "successful_tests": result.testsRun - len(result.errors) - len(result.failures),
        }
