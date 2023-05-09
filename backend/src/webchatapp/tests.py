from django.test import TestCase
from django.test import Client


# Create your tests here.

# Tester info
# "username": "testitestaaja2", 
# "password": "secreaasdasdGGFAF!12!"
#
c = Client()
c.post("/webchatapp/create",
       {"username": "testitestaaja2", 
        "password1": "secreaasdasdGGFAF!12!",
        "password2": "secreaasdasdGGFAF!12!"})


class TestAuthenticationCooldown(TestCase):
    def test_login_cooldown(self):
        '''for i in range(0,5):
            response = c.post("/webchatapp/login", 
                            {"username": "testitestaaja2", 
                            "password": "wrongpassword"})'''
        response = c.post("/webchatapp/login", 
                        {"username": "testitestaaja2", 
                        "password": "secreaasdasdGGFAF!12!"})
            
        self.assertEqual(response.status_code, 403)

    def test_message_decryption_cooldown(self):
        '''for i in range(0,5):
            response = c.post("/webchatapp/login", 
                            {"username": "testitestaaja", 
                            "password": "wrongpassword"})'''
        response = c.post("/webchatapp/login", 
                {"username": "testitestaaja2", 
                "password": "secreaasdasdGGFAF!12!"})
        self.assertEqual(response.status_code, 403)
        

class TestMessageCryption(TestCase):
    #def test_message_encryption():


    #def test_message_decryption():
    print("not implemented")
