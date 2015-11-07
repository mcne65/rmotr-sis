from __future__ import division, unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand, CommandError

from rmotr_sis.utils import send_template_mail
from applications.models import Application

CONFIG = {
    'not-validated-email': {
        'template_name': 'reminders/not-validated-email.html',
        'subject': '*|FNAME|*, thanks for applying to rmotr.com! Please keep in mind that...',
        'filter': {'status': 1, 'email_validated': False},
        'next_url': 'applications:application-2'
    },
    'selected-checkout-form': {
        'template_name': 'reminders/selected-checkout-form.html',
        'subject': "Congratulations *|FNAME|*, you've been selected for our Python programming course!",
        'filter': {'selected': True, 'charge_id': ''},
        'next_url': 'applications:application-checkout'
    }
}


class Command(BaseCommand):
    help = 'Sends reminder emails to students based in given configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            'action', help=('Type of reminder to send by email. '
                            'Options are: {}'.format(', '.join(CONFIG.keys()))))
        parser.add_argument(
            '--dry-run', help='Run the command without sending real emails',
            action='store_true', default=False)

    def handle(self, *args, **kwargs):
        action = kwargs['action']
        dry_run = kwargs['dry_run']

        if action not in CONFIG.keys():
            raise CommandError('Invalid action type, please use one of: {}'
                               ''.format(', '.join(CONFIG.keys())))

        applications = Application.objects.filter(**CONFIG[action]['filter'])

        print('Sending reminder emails...')
        print()
        for app in applications:
            next_url = reverse(CONFIG[action]['next_url'],
                               args=(str(app.id),))
            context = {
                'next_url': next_url,
                'application': app
            }
            subject = CONFIG[action]['subject'].replace(
                '*|FNAME|*', app.first_name)
            template = CONFIG[action]['template_name']
            if dry_run:
                # instead of sending real emails, print in stdout
                print('Recipient: "{}"'.format(app.email))
                print('Subject: "{}"'.format(subject))
                print()
            else:
                send_template_mail(subject, template,
                                   recipient_list=[app.email],
                                   context=context)
        print('Finished. {} emails were successfully sent'
              ''.format(applications.count()))
