from django.test import TestCase
from eventex.core.models import Talk, Course
from eventex.core.managers import PeriodManager


class TalkModelTest(TestCase):

    def setUp(self):
        self.talk = Talk.objects.create(title='Título da Palestra')

    def test_create(self):
        self.assertTrue(Talk.objects.exists())

    def test_has_speakers(self):
        """Talk can have many speakers and vv. """
        self.talk.speakers.create(name='Nome do Palestrante',
                                  slug='nome-do-palestrante',
                                  website='http://hbn.link/')
        self.assertEqual(1, self.talk.speakers.count())

    def test_description_blank(self):
        field = Talk._meta.get_field('description')
        self.assertTrue(field.blank)

    def test_speaker_blank(self):
        field = Talk._meta.get_field('speakers')
        self.assertTrue(field.blank)

    def test_start_blank(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.blank)

    def test_start_null(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.null)

    def test_str(self):
        self.assertEqual('Título da Palestra', str(self.talk))

    def test_ordering(self):
        self.assertListEqual(['start'], Talk._meta.ordering)


class PeriodManagerTest(TestCase):

    def setUp(self):
        Talk.objects.create(title='Palestra da Manhã', start='08:00')
        Talk.objects.create(title='Palestra da Tarde', start='13:00')

    def test_manager(self):
        self.assertIsInstance(Talk.objects, PeriodManager)

    def test_morning(self):
        qs = Talk.objects.morning()
        self.assertQuerysetEqual(qs, ['Palestra da Manhã'], lambda o: o.title)

    def test_(self):
        qs = Talk.objects.afternoon()
        self.assertQuerysetEqual(qs, ['Palestra da Tarde'], lambda o: o.title)


class TestModelCourse(TestCase):

    def setUp(self):
        self.course = Course.objects.create(title='Título do Curso',
                                            start='09:00',
                                            description='Descrição do curso',
                                            slots=20)

    def test_create(self):
        self.assertTrue(Course.objects.exists())

    def test_has_speakers(self):
        """Course can have many speakers and vv. """
        self.course.speakers.create(name='Nome do Palestrante',
                                    slug='nome-do-palestrante',
                                    website='http://hbn.link/')
        self.assertEqual(1, self.course.speakers.count())

    def test_str(self):
        self.assertEqual('Título do Curso', str(self.course))

    def test_manager(self):
        self.assertIsInstance(Course.objects, PeriodManager)

    def test_ordering(self):
        self.assertListEqual(['start'], Course._meta.ordering)
