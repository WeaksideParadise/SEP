import unittest
from unittest.mock import MagicMock, patch
from Tests import test_RessourceActions
class test_Important(unittest.TestCase):
    #wichtige tests, auf dem tatsächlichen code ausgeführt
    def test_RessourceActions(self):
        rm = test_RessourceActions.test_RessourceActions()
        rm.setUp()
        rm.test_check_trustworthyness_trusted()
        rm.test_check_trustworthyness_untrusted()


