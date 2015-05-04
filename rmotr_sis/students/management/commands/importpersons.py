from __future__ import division, unicode_literals, absolute_import

import smartcsv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from students.models import Profile

COLUMNS = [
    {'name': 'name'},
    {'name': 'email'},
    {'name': 'timezone'}
]


class Command(BaseCommand):

    args = '<filepath>'
    help = 'Imports persons from Google spreadsheet CSV dump'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Usage: importproducts ' + self.args)

        filepath = args[0]

        print 'Importing persons from {0}...'.format(filepath)

        stats = {'imported': 0, 'skipped': 0}
        with open(filepath) as f:
            reader = smartcsv.reader(f, columns=COLUMNS, fail_fast=False)

            for person in reader:
                try:
                    Profile.objects.create(
                        email=person['email'],
                        lg_full_name=person['name'],
                        lg_timezone=person['timezone']
                    )
                except IntegrityError:
                    stats['skipped'] += 1
                else:
                    stats['imported'] += 1
        print ('Finished with stats: '
               'imported {imported}, skipped {skipped}').format(**stats)
