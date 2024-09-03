from Tests import test_Database, test_Ressource, test_RessourceActions, test_RessourceManagement, test_RessourceSearch, test_User, test_UserManagement
import unittest

if __name__ == '__main__':
    test = test_User.test_User()
    test.setUp()
   # test.test_invalid_user_id()
    test.test_getters()
    test.test_invalid_hashed_password()
    test.test_setters()
    test.test_name_length()
