import numpy as np
import common
import unittest
import naive_em
import estep_test_input_0
import estep_test_input_5
import mstep_test_input_0
import mstep_test_input_3
import bic_test_input_fixed
import bic_test_input_random

# Instructions:
#   Put all files in the same folder as naive_em.py and other files.
#   To run: python test_3_em_algorithm.py
#
# Description:
#   The tests use input and output from submissions. These are used to check your
#   results.
#
class TestEMAlgorithm(unittest.TestCase):
    #  Uncomment to skip test; add line to other tests if you want to skip them
    #  #  unittest.skip('Skip this test')
    def setUp(self):
        self.X = np.loadtxt("toy_data.txt")

    #  unittest.skip('Skip this test')
    def test_estep_toy_dataset(self):
        mixture, post = common.init(self.X, 3, 0)
        post, ll = naive_em.estep(self.X, mixture)
        expected_ll = -1388.0818
        self.assertEqual(np.isclose(ll, expected_ll),
                         True, f'Log likelihood: got {ll}, expected {expected_ll}')


    def run_estep_test_input(self, test):
        X, K, mixture, expected_post, expected_ll = test.data()
        post, ll = naive_em.estep(X, mixture)

        self.assertEqual(np.isclose(ll, expected_ll),
                         True, f'Log likelihood: got {ll}, expected {expected_ll}')

        self.assertEqual(np.allclose(post, expected_post), True, 'Post not as expected')

    def run_mstep_test_input(self, test):
        X, expected_mixture, post = test.data()
        mixture = naive_em.mstep(X, post)

        self.assertEqual(np.allclose(mixture.mu, expected_mixture.mu),
                         True, 'mu not as expected')

        self.assertEqual(np.allclose(mixture.var, expected_mixture.var),
                         True, 'var not as expected')

        self.assertEqual(np.allclose(mixture.p, expected_mixture.p),
                         True, 'p not as expected')

    #  unittest.skip('Skip this test')
    def test_estep_input_0(self):
        self.run_estep_test_input(estep_test_input_0)

    #  unittest.skip('Skip this test')
    def test_estep_input_5(self):
        self.run_estep_test_input(estep_test_input_5)

    #  unittest.skip('Skip this test')
    def test_mstep_input_0(self):
        self.run_mstep_test_input(mstep_test_input_0)

    #  unittest.skip('Skip this test')
    def test_mstep_input_3(self):
        self.run_mstep_test_input(mstep_test_input_3)

    def run_full_em(self, X, K, seed, expected_cost):
        mixture, post = common.init(X, K, seed)
        new_mixture, soft_counts, cost = naive_em.run(X, mixture, post)

        self.assertEqual(np.isclose(cost, expected_cost),
                         True, f'Cost: got {cost}, expected {expected_cost}')

    #  unittest.skip('Skip this test')
    def test_run_all(self):
        self.run_full_em(self.X, 5, 5, -1138.20583436)
        self.run_full_em(self.X, 3, 7, -1138.89094162)
        self.run_full_em(self.X, 2, 6, -1175.71487887)
        self.run_full_em(self.X, 1, 6, -1307.22343176)

    def run_bic_test_input(self, test):
        X, mixture, ll, expected_bic = test.data()

        bic = common.bic(X, mixture, ll)
        self.assertEqual(np.isclose(bic, expected_bic), True, f'BIC: got {bic}, expected {expected_bic}')

    def test_bic_fixed(self):
        self.run_bic_test_input(bic_test_input_fixed)

    def test_bic_random(self):
        self.run_bic_test_input(bic_test_input_random)


if __name__ == '__main__':
    unittest.main()
