import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_backend.settings')
django.setup()

# Now import your consumer script
from consumers import start_consumer

if __name__ == '__main__':
    start_consumer()
