import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Starts the SMTP4Dev Docker service.'

    def handle(self, *args, **options):
        docker_compose_path = os.path.join(settings.BASE_DIR, 'Docker')
        
        if not os.path.isdir(docker_compose_path):
            self.stdout.write(self.style.ERROR(f"Docker directory not found at: {docker_compose_path}"))
            return

        self.stdout.write("Starting SMTP4Dev service...")
        
        try:
            result = subprocess.run(
                ['docker-compose', 'up', '-d', 'smtp4dev'],
                cwd=docker_compose_path,
                check=True,
                capture_output=True,
                text=True
            )
            self.stdout.write(self.style.SUCCESS("SMTP4Dev service started successfully."))
            self.stdout.write(result.stdout)
            if result.stderr:
                self.stderr.write(self.style.WARNING(result.stderr))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("`docker-compose` command not found. Is Docker installed and in your PATH?"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("An error occurred while running docker-compose."))
            self.stderr.write(e.stdout)
            self.stderr.write(e.stderr)
