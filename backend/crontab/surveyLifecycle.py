from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_job
from django.utils import timezone

from surveybuilder.models import Survey

surveyScheduler = BackgroundScheduler()


@register_job(surveyScheduler, "interval", minutes=1, id="end_survey_by_time", replace_existing=True, misfire_grace_time=50)
def end_survey_by_time():
    now = timezone.now()
    Survey.objects.filter(expire_time__lt=now).update(status=2)


surveyScheduler.start()

urlpatterns = []
