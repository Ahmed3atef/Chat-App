import os
import subprocess
import sys
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Starts Locust for performance testing.'

    def handle(self, *args, **options):
        locustfile_path = os.path.join(settings.BASE_DIR, 'locustfiles', 'users.py')
        
        if not os.path.isfile(locustfile_path):
            self.stdout.write(self.style.ERROR(f"Locust file not found at: {locustfile_path}"))
            return

        self.stdout.write("Starting Locust...")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "locust", "-f", locustfile_path, "--host", "http://127.0.0.1:8000"],
                check=True
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("`locust` command not found. Is Locust installed in your environment?"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("An error occurred while starting Locust."))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Locust stopped successfully."))
