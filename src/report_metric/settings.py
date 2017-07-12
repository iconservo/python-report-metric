try:
    from django.conf import settings

    # Use django settings if we're in a django environment
    def get(name, default=None):
        return getattr(settings, name, default)

except ImportError:
    import os

    # Just use straight env vars
    def get(name, default=None):
        return os.environ.get(name, default)
