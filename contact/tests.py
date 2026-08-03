"""Tests for contact views and forms."""

from django.test import TestCase
from django.urls import reverse

from .models import ChurchInfo, ContactMessage


class HomeViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('contact:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Grace Community Church')

    def test_home_page_shows_church_info(self):
        ChurchInfo.objects.create(
            name='Grace Community Church',
            motto='Growing Together in Faith, Hope, and Love',
            history='History text',
            mission='Mission text',
            vision='Vision text',
            core_values='Faith\nHope\nLove',
            pastor_name='Rev. David Thompson',
            pastor_message='Welcome!',
            address='123 Faith Avenue',
            city='Springfield',
            state='IL',
            zip_code='62701',
            phone='(555) 123-4567',
            email='info@gracecommunitychurch.org',
            office_hours='Mon-Fri 9-5',
        )
        response = self.client.get(reverse('contact:home'))
        self.assertContains(response, 'Rev. David Thompson')
        self.assertContains(response, 'Growing Together in Faith, Hope, and Love')


class AboutViewTests(TestCase):
    def test_about_page_loads(self):
        response = self.client.get(reverse('contact:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')


class ContactFormTests(TestCase):
    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact:contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '555-0100',
            'subject': 'General Inquiry',
            'message': 'Hello, I would like to learn more about your church.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, 'Thank you')

    def test_contact_page_loads(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact')
