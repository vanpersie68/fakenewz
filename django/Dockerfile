FROM python:3.7-buster

ENV EMAIL_BACKEND=django_smtp_ssl.SSLEmailBackend \
    EMAIL_HOST=smtp.qiye.aliyun.com \
    EMAIL_PORT=465 \
    EMAIL_HOST_USER=cs63-1@mineserver.top \
    EMAIL_HOST_PASSWORD=CS63-1-mail \
    EMAIL_USE_TLS=True \
    DEFAULT_FROM_EMAIL=cs63-1@mineserver.top \
    SITE_ID=1 \
    ACCOUNT_EMAIL_VERIFICATION=mandatory \
    ACCOUNT_EMAIL_REQUIRED=True \
    PYTHONUNBUFFERED=1 
    
WORKDIR /backend

COPY ./backend/requirements.txt requirements.txt
EXPOSE 8000
RUN python3 -m pip install --default-timeout=100 -r requirements.txt
RUN apt-get update && apt-get install libpq-dev nginx vim net-tools -y
COPY ./backend .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
