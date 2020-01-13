#!/bin/sh

# gather all static files in a single folder under .static/
# --clear to delete all files under /static before gather operation, --no-input to avoid asking the user
python manage.py collectstatic --clear --no-input

exec "$@"