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
    },
    'selected-checkout-expiring': {
        'template_name': 'reminders/selected-checkout-expiring.html',
        'subject': "Hey *|FNAME|*, your reserved spot for the Python course is about to expire!",
        'filter': {'selected': True, 'charge_id': ''},
        'next_url': 'applications:application-checkout'
    },
    'scholarships-not-finished': {
        'template_name': 'reminders/scholarships-not-finished.html',
        'subject': "Hey *|FNAME|*, finish submitting your scholarship application. There's still time!",
        'filter': {'selected': False, 'status__gte': 4},
        'exclude': {'status': 7},
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

        if action not in CONFIG:
            raise CommandError('Invalid action type, please use one of: {}'
                               ''.format(', '.join(CONFIG.keys())))

        config = CONFIG[action]
        applications = Application.objects.filter(**config['filter'])

        if 'exclude' in config:
            applications = applications.exclude(**config['exclude'])

        print('Sending reminder emails...')
        print()
        for app in applications:
            next_url = reverse(config['next_url'],
                               args=(str(app.id),))
            context = {
                'next_url': next_url,
                'application': app
            }
            subject = config['subject'].replace(
                '*|FNAME|*', app.first_name)
            template = config['template_name']
            if dry_run:
                # instead of sending real emails, print in stdout
                print('Recipient: "{}"'.format(app.email))
                print('Subject: "{}"'.format(subject))
                print('Next URL: "{}"'.format(next_url))
                print()
            else:
                send_template_mail(subject, template,
                                   recipient_list=[app.email],
                                   context=context)
        print('Finished. {} emails were successfully sent'
              ''.format(applications.count()))
