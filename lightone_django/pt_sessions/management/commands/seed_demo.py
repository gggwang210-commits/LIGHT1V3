from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Disabled archived demo seeder.'

    def handle(self, *args, **options):
        raise CommandError(
            'This archived seeder is disabled. Use the guarded seed_lightone command '
            'in lightone_v2_django with synthetic identifiers.'
        )
