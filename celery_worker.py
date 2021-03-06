"""
Sets up the celery worker
"""

#!/usr/bin/env python
import os

from app import create_app

app = create_app()
app.app_context().push()

from app import celery