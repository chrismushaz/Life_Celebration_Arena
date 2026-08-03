"""
Populate the database with sample church content for development and demos.
"""

from datetime import timedelta
from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw

from blog.models import BlogCategory, BlogPost
from contact.models import ChurchInfo
from events.models import Event
from gallery.models import GalleryCategory, GalleryImage, GalleryVideo
from ministries.models import LeadershipMember, Ministry
from prayer.models import PrayerRequest
from sermons.models import Speaker, Sermon

User = get_user_model()


def make_placeholder_image(width, height, label, bg_color=(30, 58, 95), text_color=(201, 162, 39)):
    """Create a simple placeholder JPEG in memory."""
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    draw.text((width // 2 - len(label) * 4, height // 2 - 8), label, fill=text_color)
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f'{label.lower().replace(" ", "-")}.jpg')


class Command(BaseCommand):
    help = 'Seed the database with sample Grace Community Church content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete existing seedable content before creating new records',
        )
        parser.add_argument(
            '--admin-password',
            default='admin123',
            help='Password for the demo admin account (default: admin123)',
        )

    def handle(self, *args, **options):
        if options['force']:
            self._clear_data()

        if ChurchInfo.objects.exists():
            self.stdout.write(self.style.WARNING('Church data already exists. Use --force to reseed.'))
            return

        admin = self._create_admin(options['admin_password'])
        church = self._create_church_info()
        speaker = self._create_speakers()
        self._create_sermons(speaker)
        self._create_ministries()
        self._create_leadership()
        self._create_events()
        self._create_blog(admin)
        self._create_gallery()
        self._create_prayer_requests()

        self.stdout.write(self.style.SUCCESS('Sample church data created successfully.'))
        self.stdout.write('Admin login: admin / {}'.format(options['admin_password']))

    def _clear_data(self):
        PrayerRequest.objects.all().delete()
        GalleryVideo.objects.all().delete()
        GalleryImage.objects.all().delete()
        GalleryCategory.objects.all().delete()
        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()
        Event.objects.all().delete()
        LeadershipMember.objects.all().delete()
        Ministry.objects.all().delete()
        Sermon.objects.all().delete()
        Speaker.objects.all().delete()
        ChurchInfo.objects.all().delete()
        User.objects.filter(username='admin').delete()

    def _create_admin(self, password):
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@gracecommunitychurch.org',
                'first_name': 'Church',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created or not user.check_password(password):
            user.set_password(password)
            user.save()
        return user

    def _create_church_info(self):
        return ChurchInfo.objects.create(
            name='Grace Community Church',
            motto='Growing Together in Faith, Hope, and Love',
            tagline='A welcoming community where everyone belongs',
            history=(
                'Grace Community Church was founded in 1985 by a small group of families '
                'who wanted to create a welcoming place of worship in the heart of the community. '
                'What began as a gathering of twenty people in a living room has grown into a '
                'vibrant congregation serving hundreds of families each week.'
            ),
            mission=(
                'To lead people into a growing relationship with Jesus Christ by creating '
                'environments where people are encouraged and equipped to pursue intimacy with God, '
                'community with believers, and influence with the world.'
            ),
            vision=(
                'To be a church that transforms lives, strengthens families, and impacts our '
                'community with the love of Christ.'
            ),
            core_values=(
                'Biblical Teaching\nAuthentic Worship\nGenuine Community\n'
                'Compassionate Outreach\nSpiritual Growth\nServant Leadership'
            ),
            pastor_name='Rev. David Thompson',
            pastor_title='Senior Pastor',
            pastor_message=(
                'Welcome to Grace Community Church! Whether you are exploring faith for the first time '
                'or have been walking with Christ for years, you belong here. We would love to meet you '
                'this Sunday and walk alongside you in your journey of faith.'
            ),
            address='123 Faith Avenue',
            city='Springfield',
            state='IL',
            zip_code='62701',
            phone='(555) 123-4567',
            email='info@gracecommunitychurch.org',
            office_hours='Monday-Friday: 9:00 AM - 5:00 PM\nSunday: 8:00 AM - 1:00 PM',
            facebook_url='https://facebook.com/gracecommunitychurch',
            youtube_url='https://youtube.com/@gracecommunitychurch',
            instagram_url='https://instagram.com/gracecommunitychurch',
            live_stream_url='https://youtube.com/@gracecommunitychurch/live',
        )

    def _create_speakers(self):
        speaker, _ = Speaker.objects.get_or_create(
            name='Rev. David Thompson',
            defaults={
                'title': 'Senior Pastor',
                'bio': 'Pastor David has served Grace Community Church since 2010.',
                'is_active': True,
            },
        )
        return speaker

    def _create_sermons(self, speaker):
        sermons = [
            {
                'title': 'Walking by Faith',
                'scripture_reference': 'Hebrews 11:1',
                'description': 'Discover what it means to live a life guided by faith rather than sight.',
                'days_ago': 7,
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'series': 'Faith Foundations',
                'is_featured': True,
            },
            {
                'title': 'The Power of Community',
                'scripture_reference': 'Acts 2:42-47',
                'description': 'How the early church modeled authentic Christian community.',
                'days_ago': 14,
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'series': 'Better Together',
                'is_featured': True,
            },
            {
                'title': 'Hope in Hard Times',
                'scripture_reference': 'Romans 8:28',
                'description': 'Finding hope and purpose when life feels overwhelming.',
                'days_ago': 21,
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'series': 'Hope for Today',
                'is_featured': True,
            },
        ]
        now = timezone.now().date()
        for data in sermons:
            sermon = Sermon(
                title=data['title'],
                speaker=speaker,
                scripture_reference=data['scripture_reference'],
                description=data['description'],
                date_preached=now - timedelta(days=data['days_ago']),
                youtube_url=data['youtube_url'],
                series=data['series'],
                is_featured=data['is_featured'],
            )
            sermon.thumbnail.save(
                f"{data['title'].lower().replace(' ', '-')}.jpg",
                make_placeholder_image(640, 360, data['title'][:20]),
                save=False,
            )
            sermon.save()

    def _create_ministries(self):
        ministries = [
            ('Children\'s Ministry', 'children', 'Nurturing the faith of our youngest members through age-appropriate teaching and fun activities.', 'Sundays 9:00 AM'),
            ('Youth Ministry', 'youth', 'Empowering teenagers to grow in faith and build lasting friendships.', 'Wednesdays 6:30 PM'),
            ('Women\'s Ministry', 'women', 'Connecting women through Bible study, fellowship, and service opportunities.', 'Tuesdays 10:00 AM'),
            ('Men\'s Ministry', 'men', 'Building godly men through accountability, study, and service projects.', 'Saturdays 7:00 AM'),
            ('Worship Team', 'worship', 'Leading our congregation in heartfelt worship through music and the arts.', 'Thursdays 7:00 PM'),
            ('Community Outreach', 'outreach', 'Serving our neighbors through food drives, shelter support, and local partnerships.', 'Monthly events'),
        ]
        for order, (name, ministry_type, description, meeting_time) in enumerate(ministries):
            ministry = Ministry(
                name=name,
                ministry_type=ministry_type,
                description=description,
                meeting_time=meeting_time,
                contact_email='ministries@gracecommunitychurch.org',
                order=order,
            )
            ministry.image.save(
                f'{ministry_type}.jpg',
                make_placeholder_image(800, 500, name[:15]),
                save=False,
            )
            ministry.save()

    def _create_leadership(self):
        leaders = [
            ('Rev. David Thompson', 'pastor', 'Senior Pastor', 'Leading the congregation with a heart for teaching and pastoral care.'),
            ('Rev. Sarah Mitchell', 'associate', 'Associate Pastor', 'Overseeing discipleship and small group ministries.'),
            ('James Wilson', 'elder', 'Elder', 'Serving on the elder board with wisdom and dedication.'),
            ('Maria Garcia', 'worship', 'Worship Leader', 'Directing our worship team and creative arts ministry.'),
            ('Michael Chen', 'youth', 'Youth Pastor', 'Passionate about helping students discover their purpose in Christ.'),
        ]
        for order, (name, role, title, bio) in enumerate(leaders):
            LeadershipMember.objects.create(
                name=name,
                role=role,
                title=title,
                bio=bio,
                order=order,
            )

    def _create_events(self):
        now = timezone.now()
        events = [
            {
                'title': 'Easter Celebration Service',
                'description': 'Join us for a special Easter worship service celebrating the resurrection of Jesus Christ.',
                'location': 'Main Sanctuary',
                'days_ahead': 30,
                'is_featured': True,
                'registration_required': True,
                'max_attendees': 500,
            },
            {
                'title': 'Community Food Drive',
                'description': 'Help us collect non-perishable food items for local families in need.',
                'location': 'Church Parking Lot',
                'days_ahead': 14,
                'is_featured': False,
                'registration_required': False,
            },
            {
                'title': 'Summer Youth Camp',
                'description': 'A week-long adventure for students grades 6-12 with worship, games, and Bible study.',
                'location': 'Camp Grace',
                'days_ahead': 60,
                'is_featured': False,
                'registration_required': True,
                'max_attendees': 80,
            },
        ]
        for data in events:
            event = Event(
                title=data['title'],
                description=data['description'],
                location=data['location'],
                start_date=now + timedelta(days=data['days_ahead']),
                end_date=now + timedelta(days=data['days_ahead'], hours=3),
                is_featured=data['is_featured'],
                registration_required=data['registration_required'],
                max_attendees=data.get('max_attendees'),
            )
            event.image.save(
                f"{data['title'].lower().replace(' ', '-')}.jpg",
                make_placeholder_image(800, 450, data['title'][:18]),
                save=False,
            )
            event.save()

    def _create_blog(self, admin):
        categories = {
            'Pastor Articles': BlogCategory.objects.create(name='Pastor Articles', slug='pastor-articles'),
            'Devotionals': BlogCategory.objects.create(name='Devotionals', slug='devotionals'),
            'Bible Study': BlogCategory.objects.create(name='Bible Study', slug='bible-study'),
        }
        posts = [
            {
                'title': 'Finding Peace in a Busy World',
                'category': categories['Pastor Articles'],
                'post_type': 'article',
                'excerpt': 'In our fast-paced culture, finding true peace can feel impossible. Here is how Scripture guides us.',
                'content': (
                    'Jesus said, "Peace I leave with you; my peace I give you." In a world filled with noise '
                    'and distraction, His peace is available to every believer who seeks Him.\n\n'
                    'Take time each day to be still before God. Turn off your phone, open your Bible, and '
                    'allow the Holy Spirit to refresh your soul.'
                ),
                'scripture_reference': 'John 14:27',
            },
            {
                'title': 'Daily Bread: Trusting God Today',
                'category': categories['Devotionals'],
                'post_type': 'devotional',
                'excerpt': 'A short devotional on trusting God with today\'s needs.',
                'content': (
                    'God provides for us one day at a time. Just as manna was given daily in the wilderness, '
                    'His grace is sufficient for today\'s challenges. Do not borrow tomorrow\'s worries.'
                ),
                'scripture_reference': 'Matthew 6:34',
            },
            {
                'title': 'Introduction to the Book of Romans',
                'category': categories['Bible Study'],
                'post_type': 'bible_study',
                'excerpt': 'Begin our study through Paul\'s letter to the Romans.',
                'content': (
                    'Romans is Paul\'s most systematic presentation of the gospel. In chapter 1, Paul introduces '
                    'himself and declares the theme of the letter: the righteousness of God revealed in the gospel.'
                ),
                'scripture_reference': 'Romans 1:16-17',
            },
        ]
        for data in posts:
            BlogPost.objects.create(
                title=data['title'],
                author=admin,
                category=data['category'],
                post_type=data['post_type'],
                excerpt=data['excerpt'],
                content=data['content'],
                scripture_reference=data['scripture_reference'],
                is_published=True,
            )

    def _create_gallery(self):
        categories = {
            'Worship Services': GalleryCategory.objects.create(name='Worship Services', slug='worship'),
            'Community Events': GalleryCategory.objects.create(name='Community Events', slug='events'),
            'Outreach': GalleryCategory.objects.create(name='Outreach', slug='outreach'),
        }
        images = [
            ('Sunday Worship', categories['Worship Services']),
            ('Baptism Celebration', categories['Worship Services']),
            ('Community Picnic', categories['Community Events']),
            ('Food Drive Volunteers', categories['Outreach']),
            ('Youth Group Retreat', categories['Community Events']),
            ('Christmas Eve Service', categories['Worship Services']),
        ]
        for title, category in images:
            image = GalleryImage(title=title, category=category, description=f'Photos from {title.lower()}.')
            image.image.save(
                f'{title.lower().replace(" ", "-")}.jpg',
                make_placeholder_image(800, 600, title[:16]),
                save=False,
            )
            image.save()

        GalleryVideo.objects.create(
            title='Easter Service Highlight',
            description='Highlights from our Easter celebration.',
            youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            category=categories['Worship Services'],
        )

    def _create_prayer_requests(self):
        PrayerRequest.objects.create(
            name='Anonymous',
            request_text='Please pray for healing and strength during a difficult season.',
            is_anonymous=True,
            is_public=True,
            status='praying',
        )
        PrayerRequest.objects.create(
            name='Jennifer',
            request_text='Pray for my family as we navigate a job transition.',
            is_public=True,
            status='new',
        )
