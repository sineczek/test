from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_store_not_found(self):
        with self.app() as client:
            resp = client.get('/store/test')
            self.assertEqual(resp.status_code, 404)

    def test_store_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'id': 1, 'name': 'test', 'items': []},  # d1 dictionary 1
                                     d2=json.loads(resp.data))  # d2 dictionary 2

    def test_store_with_items_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]},
                                     d2=json.loads(resp.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.delete('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'message': 'Store deleted'},
                                     d2=json.loads(resp.data))

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(d1={'id': 1, 'name': 'test', 'items': []},
                                     d2=json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 400)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/stores')

                self.assertDictEqual(d1={'stores': [{'id': 1, 'name': 'test', 'items': []}]},
                                     d2=json.loads(resp.data))

    def test_store_with_items_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/stores')

                self.assertDictEqual(d1={'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]},
                                     d2=json.loads(resp.data))
