"""Tests for sermon list and detail views."""

from datetime import date

from django.test import TestCase
from django.urls import reverse

from sermons.models import Speaker, Sermon


class SermonViewTests(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(name='Rev. David Thompson')
        self.sermon = Sermon.objects.create(
            title='Walking by Faith',
            speaker=self.speaker,
            date_preached=date.today(),
            description='A message about faith.',
            scripture_reference='Hebrews 11:1',
        )

    def test_sermon_list_loads(self):
        response = self.client.get(reverse('sermons:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Walking by Faith')

    def test_sermon_detail_loads(self):
        response = self.client.get(reverse('sermons:detail', kwargs={'slug': self.sermon.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Walking by Faith')
        self.assertContains(response, 'Hebrews 11:1')
