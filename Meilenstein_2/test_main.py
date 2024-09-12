import unittest
from Tests import test_Database, test_Ressource, test_RessourceActions, test_RessourceManagement, test_RessourceSearch, test_User, test_UserManagement, test_Important

# Executes all the tests in the specified test case classes
if __name__ == '__main__':
    # Load all tests from the test_classes
    test_classes = [
        test_Database.test_Database,
        test_Ressource.test_Ressource,
        test_RessourceActions.test_RessourceActions,
        test_RessourceManagement.test_RessourceManagement,
        test_RessourceSearch.test_RessourceSearch,
        test_User.test_User,
        test_UserManagement.test_UserManagement,
        test_Important.test_Important,
    ]

    # Create a test suite combining all test cases
    loader = unittest.TestLoader()
    suites_list = []
    
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    # Combine all suites into a single test suite
    big_suite = unittest.TestSuite(suites_list)

    # Run the combined test suite
    runner = unittest.TextTestRunner()
    runner.run(big_suite)
