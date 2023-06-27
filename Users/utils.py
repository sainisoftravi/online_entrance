import uuid
from django.utils.text import slugify


def GenerateRandomURL(prefix):
    random_url = f"{prefix}-{uuid.uuid4().hex}"

    return slugify(random_url)
