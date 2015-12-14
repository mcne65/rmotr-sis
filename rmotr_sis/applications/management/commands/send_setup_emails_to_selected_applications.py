from __future__ import division, unicode_literals, absolute_import

import argparse

from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand

from rmotr_sis.utils import send_template_mail
from applications.models import Application


SUBJECT = 'Welcome to rmotr.com! Please setup your account so we can start.'


class Command(BaseCommand):
    help = 'Sends email to selected participants to setup accounts'

    def add_arguments(self, parser):
        parser.add_argument(
            'applications', type=argparse.FileType('r'),
            help='A text file containing applications ID. One per line.')
        parser.add_argument(
            '--email_template_name', required=False,
            default="signup_selected_participant.html",
            help='Template name to use as email body.')
        parser.add_argument(
            '--dry-run', help='Run the command without sending real emails',
            action='store_true', default=False)

    def process_application(self, app_id):
        if app_id in self.processed_applications_ids:
            self.duplicated_applications_ids.add(app_id)
            return

        try:
            app = Application.objects.get(id=app_id)
        except Application.DoesNotExist:
            self.nonexistent_applications_ids.append(app_id)
            return

        if not app.selected:
            self.unselected_applications_ids.append(app_id)
            return

        # Everything ok! Send the email. Mark as processed
        self.processed_applications_ids.append(app_id)
        signup_url = reverse('applications:application-signup',
                             args=(str(app.id),))
        context = {
            'signup_url': signup_url,
            'application': app
        }

        if self.dry_run:
            # instead of sending real emails, print in stdout
            print("\n====================================")
            print('App ID: "{}"'.format(app.id))
            print('Recipient: "{}"'.format(app.email))
            print('Subject: "{}"'.format(SUBJECT))
            print("URL: {}".format(signup_url))
            print("====================================\n")
            return

        send_template_mail(SUBJECT, self.template_name,
                           recipient_list=[app.email],
                           context=context)

    def print_report(self):
        def print_app_ids_with_tab(application_ids):
            for app_id in application_ids:
                print("\t {}".format(app_id))

        print("Processing finished!")
        print("Succesfully sent emails:")
        print_app_ids_with_tab(self.processed_applications_ids)
        print("Duplicated applications:")
        print_app_ids_with_tab(self.duplicated_applications_ids)
        print("Invalid/non-existent applications:")
        print_app_ids_with_tab(self.nonexistent_applications_ids)
        print("Unselected applications:")
        print_app_ids_with_tab(self.unselected_applications_ids)

    def handle(self, *args, **kwargs):
        applications_file = kwargs['applications']

        self.template_name = kwargs['email_template_name']
        self.dry_run = kwargs['dry_run']
        self.processed_applications_ids = []
        self.unselected_applications_ids = []
        self.nonexistent_applications_ids = []
        self.duplicated_applications_ids = set()

        for app_id in applications_file:
            self.process_application(app_id.strip())

        self.print_report()
