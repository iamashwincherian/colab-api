import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Start docker compose"
    
    def handle(self, *args, **kwargs):
        subprocess.run(["docker-compose", "up"])
        self.stdout.write("Starting docker container")