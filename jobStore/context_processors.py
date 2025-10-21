import os
from pathlib import Path
from django.conf import settings

def static_revisions(request):
    """Expose simple cache-busting revisions for key static assets."""
    base = Path(settings.BASE_DIR)
    logo_path = base / 'jobStore' / 'static' / 'img' / 'logo.png'
    try:
        rev_logo = str(int(os.path.getmtime(logo_path)))
    except Exception:
        rev_logo = '1'
    return {
        'STATIC_REV_LOGO': rev_logo,
    }

