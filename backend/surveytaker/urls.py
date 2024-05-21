from django.conf.urls import url
from django.urls import re_path, path
from django.views.decorators.csrf import csrf_exempt

from surveytaker.views import save_response_view, get_survey_questions_view, get_survey_result_view, get_random_response

urlpatterns = [
    # Get: get 5 text response randomly
    path('survey/result/statistic/<str:flag>/<int:question_id>', get_random_response.get_text_result),
    # Get: get survey statistic result
    path('survey/result/<int:preview>/<int:survey_id>', get_survey_result_view.get_result),
    # Post: save survey taker's response
    url(r'^survey/saveResponse', save_response_view.save_response),
    # Get: survey questions according to the code
    url(r'^surveyQuestions/(?P<code>[A-Za-z0-9]+$)', get_survey_questions_view.get_survey_questions),
    # url(r'^survey/$', csrf_exempt(views.ResponseView.as_view())),
    # re_path(r'^survey/(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{10}$', csrf_exempt(views.SurveyAPIView.as_view()))
]
