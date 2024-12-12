import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from app import app, get_all_products

class TestProductList(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

if __name__ == '__main__':
    unittest.main()
def test_home_route(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'<html>', response.data)  # Assuming 'home.html' contains basic HTML structure
    self.assertTemplateUsed('home.html')def test_home_route_content_type(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')