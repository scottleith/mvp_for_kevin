release: python manage.py migrate
web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
clock: python mvp_texting_app/schedules/schedule_checker.py
