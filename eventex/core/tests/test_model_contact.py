from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):

    def setUp(self):
        self.speaker = Speaker.objects.create(name='John Doe', slug='john-doe',
                                              photo='http://fpoimg.com/512x512')

    def test_email(self):
        Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                               value='jd@server.co')
        self.assertTrue(Contact.objects.exists())

    def test_telephone(self):
        Contact.objects.create(speaker=self.speaker, kind=Contact.TELEPHONE,
                               value='2345678')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """ Contact.kid should be limited to E or T"""
        contact = Contact.objects.create(speaker=self.speaker, kind='A',
                                         value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL,
                          value='jd@server.co')
        self.assertEqual('jd@server.co', str(contact))
