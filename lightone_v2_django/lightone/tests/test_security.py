from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from accounts.models import User


class DemoSeedSecurityTests(TestCase):
    @override_settings(DEBUG=False)
    def test_seed_is_blocked_outside_debug_mode(self):
        with self.assertRaises(CommandError):
            call_command('seed_lightone', generate_passwords=True)

    @override_settings(DEBUG=True)
    def test_seed_creates_only_synthetic_accounts_with_random_passwords(self):
        stdout = StringIO()
        call_command('seed_lightone', generate_passwords=True, stdout=stdout)

        users = User.objects.filter(username__in=['syn-admin', 'syn-001', 'syn-002'])
        self.assertEqual(users.count(), 3)
        self.assertEqual(
            set(users.values_list('name', flat=True)),
            {'데모관리자', '데모회원-A', '데모회원-B'},
        )
        for user in users:
            self.assertFalse(user.check_password('12' + '34'))
            self.assertFalse(user.check_password('ad' + 'min'))

        output = stdout.getvalue()
        self.assertIn('One-time local credentials', output)
        self.assertNotIn('member1', output)
        self.assertNotIn('member2', output)
