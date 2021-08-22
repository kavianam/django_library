from django.test import TestCase

from .forms import SignUpForm


class SignUpFormTest(TestCase):
    def test_strong_password(self):
        data = {
            'username': 'kavian',
            'password1': 'Sfjdsl23s',
            'password2': 'Sfjdsl23s'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_weak_password(self):
        data = {
            'username': 'kavian',
            'password1': '123',
            'password2': '123'
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())
