from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from links.models import NegativeLink
from managers.models import Manager
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test data: users, managers, and links'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Creating test data...'))

        # Create test users
        users_data = [
            {'username': 'admin_user', 'email': 'admin@example.com', 'password': 'Admin2026!', 'is_staff': True, 'is_superuser': True},
            {'username': 'john_manager', 'email': 'john@example.com', 'password': 'John2026!', 'is_staff': True},
            {'username': 'alice_user', 'email': 'alice@example.com', 'password': 'Alice2026!'},
        ]

        created_users = []
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created user: {user.username} (password: {password})'))
            else:
                self.stdout.write(self.style.WARNING(f'- User already exists: {user.username}'))
            created_users.append(user)

        # Create test managers
        managers_data = [
            {'name': 'John Smith', 'email': 'john.smith@company.com', 'is_active': True},
            {'name': 'Sarah Johnson', 'email': 'sarah.j@company.com', 'is_active': True},
            {'name': 'Mike Chen', 'email': 'mike.chen@company.com', 'is_active': True},
            {'name': 'Emma Davis', 'email': 'emma.d@company.com', 'is_active': False},
        ]

        created_managers = []
        for manager_data in managers_data:
            manager, created = Manager.objects.get_or_create(
                email=manager_data['email'],
                defaults=manager_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created manager: {manager.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'- Manager already exists: {manager.name}'))
            if manager.is_active:
                created_managers.append(manager)

        # Create test links
        platforms = ['facebook', 'twitter', 'youtube', 'reddit', 'other']
        types = ['post', 'comment', 'video', 'article']
        statuses = ['active', 'removed', 'in_work', 'pending', 'cancelled']
        priorities = ['low', 'medium', 'high']

        sample_urls = [
            'https://facebook.com/fake-profile/posts/12345',
            'https://twitter.com/fake_user/status/98765',
            'https://www.youtube.com/watch?v=FakeVideoID123',
            'https://reddit.com/r/fakesub/comments/abc123/fake_title',
            'https://instagram.com/fake.account/p/FakePostID/',
            'https://tiktok.com/@fakeuser/video/123456789',
            'https://linkedin.com/posts/fake-post-id-123',
            'https://facebook.com/groups/12345/posts/67890',
            'https://twitter.com/another_fake/status/11111',
            'https://www.youtube.com/watch?v=AnotherFakeID',
        ]

        notes_templates = [
            'Reported by user for containing false information',
            'Contains hate speech and discriminatory content',
            'Spam content promoting fake products',
            'Violates community guidelines - harassment',
            'Copyright infringement detected',
            'Misinformation about health/medical topics',
            'Fake news spreading political propaganda',
            'Scam/phishing attempt detected',
            'Inappropriate content for minors',
            'Violates platform terms of service',
        ]

        links_created = 0
        for i in range(30):  # Create 30 test links
            platform = random.choice(platforms)
            link_type = random.choice(types)
            status = random.choice(statuses)
            priority = random.choice(priorities)
            manager = random.choice(created_managers) if random.random() > 0.3 else None
            
            # Random dates in the last 60 days
            days_ago = random.randint(0, 60)
            detected_at = datetime.now() - timedelta(days=days_ago)
            
            removed_at = None
            if status == 'removed':
                removed_at = detected_at + timedelta(days=random.randint(1, 10))

            url = random.choice(sample_urls) + f'?id={i}'
            notes = random.choice(notes_templates) if random.random() > 0.5 else ''

            link, created = NegativeLink.objects.get_or_create(
                url=url,
                defaults={
                    'platform': platform,
                    'type': link_type,
                    'status': status,
                    'detected_at': detected_at,
                    'removed_at': removed_at,
                    'priority': priority,
                    'manager': manager,
                    'notes': notes,
                }
            )

            if created:
                links_created += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {links_created} test links'))
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('TEST DATA CREATED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        
        self.stdout.write(self.style.WARNING('\nTest Users:'))
        for user_data in users_data:
            self.stdout.write(f"  • Username: {user_data['username']}")
        
        self.stdout.write(self.style.WARNING('\nTest Credentials:'))
        self.stdout.write('  • admin_user / Admin2026!')
        self.stdout.write('  • john_manager / John2026!')
        self.stdout.write('  • alice_user / Alice2026!')
        self.stdout.write('  • phil_demo / PhilDemo2026 (already exists)')
        
        self.stdout.write(self.style.WARNING(f'\nManagers: {len(created_managers)} active'))
        self.stdout.write(self.style.WARNING(f'Links: {NegativeLink.objects.count()} total'))
