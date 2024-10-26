from django.test import TestCase


from newspaper.forms import RedactorCreationForm


class FormsTest(TestCase):
    def test_redactor_creation_form_with_experience_first_last_name_is_valid(
            self
    ):
        form_data = {
            "username": "test",
            "password1": "1A2g3s4f1234",
            "password2": "1A2g3s4f1234",
            "email": "email@mail.mail",
            "first_name": "test",
            "last_name": "test",
            "years_of_experience": 5,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
