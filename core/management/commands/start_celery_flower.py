import os
import subprocess
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts Flower for Celery monitoring.'

    def handle(self, *args, **options):
        self.stdout.write("Starting Flower...")

        try:
            subprocess.run(
                [sys.executable, "-m", "celery", "-A", "mainProject", "flower"],
                check=True
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("`celery` command not found. Is Celery installed in your environment?"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("An error occurred while starting Flower."))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Flower stopped successfully."))
