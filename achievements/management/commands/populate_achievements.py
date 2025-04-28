# achievements/management/commands/populate_achievements.py

from django.core.management.base import BaseCommand
from achievements.models import Achievement, Badge

class Command(BaseCommand):
    help = 'Populates the database with initial achievements and badges'

    def handle(self, *args, **options):
        self.stdout.write('Creating achievements...')

        # Collection achievements
        achievements = [
            # Collection achievements
            {
                'name': 'Beginner Collector',
                'description': 'Collect 5 different Pokemon',
                'category': 'collection',
                'experience_reward': 100,
                'currency_reward': 50,
            },
            {
                'name': 'Intermediate Collector',
                'description': 'Collect 10 different Pokemon',
                'category': 'collection',
                'experience_reward': 200,
                'currency_reward': 100,
            },
            {
                'name': 'Advanced Collector',
                'description': 'Collect 25 different Pokemon',
                'category': 'collection',
                'experience_reward': 500,
                'currency_reward': 250,
            },
            {
                'name': 'Type Enthusiast',
                'description': 'Collect Pokemon of 5 different types',
                'category': 'collection',
                'experience_reward': 200,
                'currency_reward': 100,
            },
            {
                'name': 'Custom Creator',
                'description': 'Create your first custom Pokemon',
                'category': 'collection',
                'experience_reward': 150,
                'currency_reward': 75,
            },

            # Trading achievements
            {
                'name': 'First Trade',
                'description': 'Complete your first Pokemon trade',
                'category': 'trading',
                'experience_reward': 100,
                'currency_reward': 50,
            },
            {
                'name': 'Trading Expert',
                'description': 'Complete 5 Pokemon trades',
                'category': 'trading',
                'experience_reward': 250,
                'currency_reward': 125,
            },
            {
                'name': 'Market Participant',
                'description': 'Sell your first Pokemon in the marketplace',
                'category': 'marketplace',
                'experience_reward': 100,
                'currency_reward': 50,
            },
            {
                'name': 'Market Mogul',
                'description': 'Sell 5 Pokemon in the marketplace',
                'category': 'marketplace',
                'experience_reward': 250,
                'currency_reward': 125,
            },

            # Battle achievements
            {
                'name': 'First Victory',
                'description': 'Win your first battle',
                'category': 'battle',
                'experience_reward': 100,
                'currency_reward': 50,
            },
            {
                'name': 'Battle Champion',
                'description': 'Win 5 battles',
                'category': 'battle',
                'experience_reward': 250,
                'currency_reward': 125,
            },
            {
                'name': 'AI Dominator',
                'description': 'Win 10 battles against AI opponents',
                'category': 'battle',
                'experience_reward': 300,
                'currency_reward': 150,
            },

            # Special achievements
            {
                'name': 'Social Butterfly',
                'description': 'Create a chat room and send at least 5 messages',
                'category': 'special',
                'experience_reward': 100,
                'currency_reward': 50,
            },
            {
                'name': 'Completionist',
                'description': 'Earn 10 different achievements',
                'category': 'special',
                'experience_reward': 500,
                'currency_reward': 250,
            },
        ]

        for achievement_data in achievements:
            Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(achievements)} achievements!'))

        # Badges
        self.stdout.write('Creating badges...')

        badges = [
            {
                'name': 'Starter Badge',
                'description': 'Earned by registering and starting your Pokemon journey',
                'difficulty': 1,
                'experience_reward': 100,
            },
            {
                'name': 'Collection Badge',
                'description': 'Earned by collecting at least 10 Pokemon',
                'difficulty': 3,
                'experience_reward': 200,
            },
            {
                'name': 'Diversity Badge',
                'description': 'Earned by collecting Pokemon of at least 8 different types',
                'difficulty': 5,
                'experience_reward': 300,
            },
            {
                'name': 'Trading Badge',
                'description': 'Earned by completing at least 5 trades',
                'difficulty': 4,
                'experience_reward': 250,
            },
            {
                'name': 'Battle Badge',
                'description': 'Earned by winning at least 5 battles',
                'difficulty': 4,
                'experience_reward': 250,
            },
            {
                'name': 'Custom Creator Badge',
                'description': 'Earned by creating at least 3 custom Pokemon',
                'difficulty': 6,
                'experience_reward': 350,
            },
            {
                'name': 'Marketplace Badge',
                'description': 'Earned by selling at least 5 Pokemon in the marketplace',
                'difficulty': 5,
                'experience_reward': 300,
            },
            {
                'name': 'Elite Trainer Badge',
                'description': 'Earned by reaching level 10',
                'difficulty': 8,
                'experience_reward': 500,
            },
        ]

        for badge_data in badges:
            Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(badges)} badges!'))