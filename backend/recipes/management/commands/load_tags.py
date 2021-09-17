import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = "loads tags from tags.csv"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR.parent / "data/tags.csv"
        with open(file_path, "r") as f:
            tags = csv.reader(f)
            bulk_create_tags = (
                Tag(name=tag[0], color=tag[2], slug=tag[1]) for tag in tags
            )
            Tag.objects.bulk_create(bulk_create_tags)
