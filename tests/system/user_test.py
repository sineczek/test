from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    """
    test_register_user - czy może się zarejestrować
    test_register_and_login - czy może się zalogować
    test_register_duplicate_user - czy już w bazie go nie ma
    """
    def test_register_user(self):
        with self.app() as client:
            with self.app_context(): #aby zapisać w bazie i mieć do niej dostęp
                response = client.post('/register', data={'username' : 'test', 'password' : '1234'}) # przygotowanie danych na endpoint

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({"message": "User created successfully."},
                                     json.loads(response.data)) # ładuje json'a, s - jako string


    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}), # wysyła datę jako jsona a nie słownik
                                           headers={'Content-Type' : 'application/json'}) # wysyła słownik jako headera

# /auth zwróci {'access_token': 'ciąg znaków zakodowany JWT'}
                self.assertIn('access_token', json.loads(auth_response.data).keys()) # zwraca listę kluczy i sprawdza czy jest tam ['access_token']




    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))
