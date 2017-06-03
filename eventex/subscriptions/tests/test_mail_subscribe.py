from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribePostValid(TestCase):

    def setUp(self):
        data = dict(name='Magno Pereira', cpf='12345678901',
                    email='elmagnopc@gmail.com', phone='11-123456-789'
                    )

        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]


    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)


    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_mail_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'elmagnopc@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Magno Pereira', '12345678901', 'elmagnopc@gmail.com', '11-123456-789']
        for content in contents:
            self.assertIn(content, self.email.body)
