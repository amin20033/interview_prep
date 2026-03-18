from django.test import TestCase
from rest_framework.test import APITestCase
from myapp.models import User,History
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.
class UserModelTest(TestCase):
    def test_user_model(self):
        user=User.objects.create_user(email="tom@gmail.com",password="amin",name="tom")
        self.assertEqual(user.email,"tom@gmail.com")
        self.assertEqual(user.name,"tom")
        self.assertTrue(user.check_password("amin"))

class HistoryModelTest(TestCase):
    def test_model_test(self):
        user=User.objects.create_user(email="tom@gmail.com",password="amin",name="tom")
        history=History.objects.create(job="Data Analyst",exp="2 Years",user=user,response="Hello")
        self.assertEqual(history.user,user)
        self.assertEqual(history.exp,"2 Years")
        self.assertEqual(history.job,"Data Analyst")
        self.assertEqual(history.response,"Hello")
class Register(APITestCase):
    def setUp(self):
        self.validdata={
        "name":"saeba",
        "email":"saeba@gmail.com",
        "password":"amin2003",
        "confirmpassword":"amin2003"
        }
        self.wrongdata={
        "name":"saeba",
        "email":"saeba@gmail.com",
        "password":"amin2003",
        "confirmpassword":"amin20034"
        }

    def test_register_correct(self):
        response=self.client.post("http://127.0.0.1:8000/api/register/",self.validdata)
        self.assertEqual(response.status_code,201)

    def test_register_wrong(self):
        response=self.client.post("http://127.0.0.1:8000/api/register/",self.wrongdata)
        self.assertEqual(response.status_code,400)

    def test_register_existing_email(self):
        User.objects.create_user(email="saeba@gmail.com",password="amin2003",name="saeba")
        response=self.client.post("http://127.0.0.1:8000/api/register/",self.validdata)
        self.assertEqual(response.status_code,400)

class ForgotpasswordRequest(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(email="saeba@gmail.com",password="amin2003",name="saeba")
        self.correctEmail={"email":"saeba@gmail.com"}
        self.wrongEmail={"email":"tom@gmail.com"}

    def test_email_do_not_exist(self):
        response=self.client.post("http://127.0.0.1:8000/api/resetrequest/",self.wrongEmail)
        self.assertEqual(response.status_code,400)
        
    def test_email_exist(self):
        response=self.client.post("http://127.0.0.1:8000/api/resetrequest/",self.correctEmail)
        self.assertEqual(response.status_code,200)

class ForgotPasswordSuccessTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            name="amin",
            email="amin@gmail.com",
            password="OldPassword@123"
        )

        # Encode user id
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))

        # Generate valid reset token
        self.token = PasswordResetTokenGenerator().make_token(self.user)

        self.url = reverse(
            "forgot-password-success",  # name of the URL
            kwargs={
                "uidb64": self.uidb64,
                "token": self.token
            }
        )

    def test_password_reset_success(self):
        data = {
            "password": "NewPassword@123",
            "confirmpassword": "NewPassword@123"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Password Changed Successfully"
        )

        # VERY IMPORTANT: verify password actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPassword@123")) 

    def test_password_mismatch(self):
        data = {
            "password": "NewPassword@123",
            "confirmpassword": "WrongPassword@123"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match", str(response.data))

    def test_invalid_token(self):
        invalid_url = reverse(
            "forgot-password-success",
            kwargs={
                "uidb64": self.uidb64,
                "token": "invalid-token-123"
            }
        )

        data = {
            "password": "NewPassword@123",
            "confirmpassword": "NewPassword@123"
        }

        response = self.client.post(invalid_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired token", str(response.data))

class Logout(APITestCase):
    def test_unauthenticated(self):
        response=self.client.post(reverse("logout"),{"refresh":"wrong-token"})
        self.assertEqual(response.status_code,401)
    def test_authenticated(self):
        user=User.objects.create_user(email="tom@gmail.com",name="tom",password="tom")
        response=self.client.post(reverse("login"),{"email":"tom@gmail.com","password":"tom"})
        refresh=response.data["refresh"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "+response.data["access"]
        )
        response=self.client.post(reverse("logout"),{"refresh":refresh})
        self.assertEqual(response.status_code,205)
class HistoryAPITest(APITestCase):
    def test_unauthenticated_get(self):
        response=self.client.get("http://127.0.0.1:8000/api/history/")
        self.assertEqual(response.status_code,401)
    def test_authenticated_get(self):
        user=User.objects.create_user(email="tom@gmail.com",name="tom",password="tom")
        response=self.client.post("http://127.0.0.1:8000/api/login/",{"email":"tom@gmail.com","password":"tom"})
        access=response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "+access
        )
        response=self.client.get("http://127.0.0.1:8000/api/history/")
        self.assertEqual(response.status_code,200)
    def test_unauthenticated_post(self):
        response=self.client.post("http://127.0.0.1:8000/api/history/",{"job":"Software Engineer","exp":"1 Year"})
        self.assertEqual(response.status_code,401)

    def test_authenticated_post(self):
        user=User.objects.create_user(email="tom@gmail.com",name="tom",password="tom")
        response=self.client.post("http://127.0.0.1:8000/api/login/",{"email":"tom@gmail.com","password":"tom"})
        access=response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "+access
        )
        response=self.client.post("http://127.0.0.1:8000/api/history/",{"job":"Software Engineer","exp":"1 Year"})
        self.assertEqual(response.status_code,201)
class Detail(APITestCase):
    def test_unauthenticated(self):
        response=self.client.get("http://127.0.0.1:8000/api/details/8/")
        self.assertEqual(response.status_code,401)
    def test_authenticated_correct_id(self):
        user=User.objects.create_user(email="tom@gmail.com",name="tom",password="tom")
        response=self.client.post("http://127.0.0.1:8000/api/login/",{"email":"tom@gmail.com","password":"tom"})
        access=response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "+access
        )
        response=self.client.post("http://127.0.0.1:8000/api/history/",{"job":"Software Engineer","exp":"1 Year"})
        response=self.client.get("http://127.0.0.1:8000/api/details/1/")
        self.assertEqual(response.status_code,200)
    def test_authenticated_wrong_id(self):
        user=User.objects.create_user(email="tom@gmail.com",name="tom",password="tom")
        response=self.client.post("http://127.0.0.1:8000/api/login/",{"email":"tom@gmail.com","password":"tom"})
        access=response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "+access
        )
        response=self.client.post("http://127.0.0.1:8000/api/history/",{"job":"Software Engineer","exp":"1 Year"})
        response=self.client.get("http://127.0.0.1:8000/api/details/2/")
        self.assertEqual(response.status_code,404)
    




        


