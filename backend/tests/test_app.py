import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_message_endpoint(self):
        response = self.app.get('/api/message')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello DevOps"})

    def test_contact_endpoint(self):
        response = self.app.post('/api/contact', data={
            'name': 'Usuario de Prueba',
            'activity': 'Desarrollo de Software',
            'email': 'prueba@ejemplo.com',
            'phone': '1234567890',
            'description': 'Descripción de prueba'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/tools.html', response.location)

    def test_register_endpoint(self):
        response = self.app.post('/api/register', data={
            'name': 'Test User',
            'email': 'test@ejemplo.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Registro exitoso"})

    def test_register_duplicate_email(self):
        self.app.post('/api/register', data={
            'name': 'Test User',
            'email': 'test@ejemplo.com',
            'password': 'password123'
        })
        response = self.app.post('/api/register', data={
            'name': 'Another User',
            'email': 'test@ejemplo.com',
            'password': 'password456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("El correo ya está registrado", response.json['error'])

    def test_login_endpoint(self):
        self.app.post('/api/register', data={
            'name': 'Test User',
            'email': 'test@ejemplo.com',
            'password': 'password123'
        })
        response = self.app.post('/api/login', data={
            'email': 'test@ejemplo.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Inicio de sesión exitoso"})

    def test_login_wrong_password(self):
        self.app.post('/api/register', data={
            'name': 'Test User',
            'email': 'test@ejemplo.com',
            'password': 'password123'
        })
        response = self.app.post('/api/login', data={
            'email': 'test@ejemplo.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Contraseña incorrecta", response.json['error'])

if __name__ == '__main__':
    unittest.main()
