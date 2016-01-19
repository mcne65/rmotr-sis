
import sh
from os.path import join
from pathlib import Path
import pytoml as toml

from django.core.management.base import BaseCommand

from tracks.models import Course, Unit, Lesson, ReadingLesson, AssignmentLesson


ORG_GITHUB_BASE_URL = 'https://github.com/rmotr-curriculum/{}'
BASE_DIR = '/tmp'
META_FILE_NAME = '.rmotr'
READINGS_FILE_NAME = 'README.md'
git = sh.git.bake('--no-pager')

# clone GH repository in a tmp directory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'course', help=('Course Github identifier. '
                            'Ex: "advanced-python-programming"'))

    def handle(self, *args, **options):
        course = Course.objects.get(github_repo=options['course'])
        course_folder = Path(join(BASE_DIR, course.github_repo))

        if course_folder.exists():
            print('Pulling changes from repo: "{}"'.format(course.github_repo))
            sh.cd(str(course_folder))
            git.pull()
        else:
            print('Cloning repo: "{}"'.format(course.github_repo))
            git.clone(ORG_GITHUB_BASE_URL.format(course.github_repo))
            sh.cd(str(course_folder))

        unit_imported_ids = []
        for unit_folder in [f for f in course_folder.glob('unit-*') if f.is_dir()]:

            print('Processing unit: "{}"'.format(unit_folder))

            # read unit meta file
            unit_dot_rmotr = unit_folder / META_FILE_NAME
            with unit_dot_rmotr.open('r') as unit_meta:
                unit_meta = toml.loads(unit_meta.read())

            # get current unit commit hash
            unit_commit = str(git.log('-n1', '--pretty=format:%H',
                                      str(unit_folder)))

            unit_imported_ids.append(unit_meta['uuid'])

            try:
                unit = Unit.objects.get(id=unit_meta['uuid'])
            except Unit.DoesNotExist:
                # unit was not imported yet. create it.
                print('\tUnit did not exist. Creating it...')
                unit = Unit.objects.create(
                    id=unit_meta['uuid'],
                    name=unit_meta['name'],
                    order=unit_meta['order'],
                    last_commit_hash=unit_commit,
                    course=course
                )
            else:
                # unit already exists. check if it was modified
                if unit.last_commit_hash != unit_commit:
                    print('\tUnit found but was modified. Updating it...')
                    unit.name = unit_meta['name']
                    unit.order = unit_meta['order']
                    unit.last_commit_hash = unit_commit
                    unit.save()
                else:
                    print('\tUnit was up to date')

            # mark all units not included in the repo as deleted
            Unit.objects.exclude(id__in=unit_imported_ids).update(deleted=True)

            lesson_imported_ids = []
            for lesson_folder in [f for f in unit_folder.glob('lesson-*') if f.is_dir()]:

                # read lesson meta file
                lesson_dot_rmotr = lesson_folder / META_FILE_NAME
                with lesson_dot_rmotr.open('r') as lesson_meta:
                    lesson_meta = toml.loads(lesson_meta.read())

                # get current lesson commit hash
                lesson_commit = str(git.log('-n1', '--pretty=format:%H',
                                            str(lesson_folder)))

                lesson_imported_ids.append(lesson_meta['uuid'])

                pass

                # mark all lessons not included in the repo as deleted
                Lesson.objects.exclude(id__in=lesson_imported_ids).update(deleted=True)
