import os
import subprocess
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts a gunicorn worker.'

    def handle(self, *args, **options):
        self.stdout.write("Starting gunicorn worker...")

        try:
            # Use sys.executable to ensure we're using the same python interpreter
            # that django is using.
            subprocess.run(
                [sys.executable, "-m", "gunicorn", "--workers",
                    "3", "mainProject.wsgi:application"],
                check=True
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(
                "`gunicorn` command not found. Is gunicorn installed in your environment?"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(
                "An error occurred while starting the gunicorn worker."))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS(
                "gunicorn worker stopped successfully."))
