import os
import subprocess
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts the Celery beat scheduler.'

    def handle(self, *args, **options):
        self.stdout.write("Starting Celery beat scheduler...")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "celery", "-A", "mainProject", "beat", "-l", "info"],
                check=True
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("`celery` command not found. Is Celery installed in your environment?"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("An error occurred while starting the Celery beat scheduler."))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Celery beat scheduler stopped successfully."))
