from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationPageTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.password = 'SyntheticPass!2026'
        self.user = self.user_model.objects.create_user(
            username='synthetic-trainer',
            name='Synthetic Trainer',
            password=self.password,
        )

    def test_login_page_is_available_to_anonymous_users(self):
        response = self.client.get(reverse('accounts:login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '트레이너 로그인')
        self.assertContains(response, reverse('accounts:signup'))
        self.assertIn('csrftoken', response.cookies)

    def test_valid_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': self.user.username, 'password': self.password},
        )

        self.assertRedirects(response, reverse('lightone:dashboard'), fetch_redirect_response=False)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_invalid_login_stays_on_form_and_does_not_authenticate(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': self.user.username, 'password': 'incorrect-password'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_protected_dashboard_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse('lightone:dashboard'))

        self.assertRedirects(response, reverse('accounts:login'), fetch_redirect_response=False)

    def test_authenticated_user_is_redirected_away_from_guest_pages(self):
        self.client.force_login(self.user)

        for url_name in ('accounts:login', 'accounts:signup'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertRedirects(response, reverse('lightone:dashboard'), fetch_redirect_response=False)


class SignupRegressionTests(TestCase):
    password = 'SyntheticPass!2026'

    def setUp(self):
        self.user_model = get_user_model()

    def signup_payload(self, **overrides):
        payload = {
            'username': 'synthetic-new-trainer',
            'name': 'Synthetic New Trainer',
            'password1': self.password,
            'password2': self.password,
        }
        payload.update(overrides)
        return payload

    def test_signup_page_is_available_to_anonymous_users(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '새 계정 만들기')
        self.assertContains(response, '비의료적 운동상담 참고자료')
        self.assertIn('csrftoken', response.cookies)

    def test_valid_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse('accounts:signup'), self.signup_payload())

        self.assertRedirects(response, reverse('accounts:login'), fetch_redirect_response=False)
        user = self.user_model.objects.get(username='synthetic-new-trainer')
        self.assertEqual(user.name, 'Synthetic New Trainer')
        self.assertTrue(user.check_password(self.password))

    def test_duplicate_username_is_rejected(self):
        self.user_model.objects.create_user(
            username='synthetic-new-trainer',
            name='Existing Synthetic Trainer',
            password=self.password,
        )

        response = self.client.post(reverse('accounts:signup'), self.signup_payload())

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(
            self.user_model.objects.filter(username='synthetic-new-trainer').count(),
            1,
        )

    def test_password_mismatch_is_rejected(self):
        response = self.client.post(
            reverse('accounts:signup'),
            self.signup_payload(password2='DifferentSyntheticPass!2026'),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)
        self.assertFalse(
            self.user_model.objects.filter(username='synthetic-new-trainer').exists()
        )

    def test_login_and_signup_posts_require_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        login_response = csrf_client.post(
            reverse('accounts:login'),
            {'username': 'synthetic-trainer', 'password': self.password},
        )
        signup_response = csrf_client.post(
            reverse('accounts:signup'),
            self.signup_payload(),
        )

        self.assertEqual(login_response.status_code, 403)
        self.assertEqual(signup_response.status_code, 403)
