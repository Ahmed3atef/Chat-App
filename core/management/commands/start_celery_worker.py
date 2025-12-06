import os
import subprocess
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts a Celery worker.'

    def handle(self, *args, **options):
        self.stdout.write("Starting Celery worker...")

        try:
            # Use sys.executable to ensure we're using the same python interpreter
            # that django is using.
            subprocess.run(
                [sys.executable, "-m", "celery", "-A", "mainProject", "worker", "-l", "info"],
                check=True
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("`celery` command not found. Is Celery installed in your environment?"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("An error occurred while starting the Celery worker."))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Celery worker stopped successfully."))
