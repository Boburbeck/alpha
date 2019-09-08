import os
import json
import pycodestyle

from django.core.management.base import BaseCommand
from django.conf import settings

from development.utils import get_files_for_checking


class Command(BaseCommand):
    help = 'Run pycodestyle linter'

    def handle(self, *args, **options):
        app_dir = os.path.join(settings.BASE_DIR, 'apps')
        source = get_files_for_checking(app_dir)

        for item in source:
            style = pycodestyle.StyleGuide(quite=True, ignore=['E501'])
            result = style.check_files([item])
            message = '%s: %s' % (item, json.dumps(result.messages, sort_keys=True, indent=4))
            if result.total_errors > 0:
                self.stderr.write(message)
