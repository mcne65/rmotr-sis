from django.core.management.base import BaseCommand

import random
from string import ascii_letters, digits

import smartcsv

from accounts.models import User

CSV_STRUCTURE = [
    {'name': 'first_name', 'required': True},
    {'name': 'last_name', 'required': True},
    {
        'name': 'email',
        'required': True,
        'validator': lambda c: '@' in c
    },
    {'name': 'github_handle'},
    {'name': 'cloud9_handle'}
]


class Command(BaseCommand):
    help = 'Imports list of users from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def get_random_passwd(self, length=8):
        chars = ascii_letters + digits
        return ''.join(random.choice(chars) for _ in range(length))

    def handle(self, *args, **options):
        print('Starting...')
        print('======= SUMMARY =======')
        with open(options['filepath'], 'r') as f:
            reader = smartcsv.reader(f, columns=CSV_STRUCTURE, header_included=False)
            counter = 0
            for row in reader:
                row['username'] = '{}.{}'.format(
                    row['first_name'], row['last_name']).lower()
                user = User(**row)

                # generate random password
                password = self.get_random_passwd()
                user.set_password(password)
                user.save()

                print('{}\t{}'.format(user.username, password))
                counter += 1
        print('=======================')
        print('Finished creating {} users.'.format(counter))
