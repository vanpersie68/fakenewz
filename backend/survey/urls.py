from django.conf.urls import url
from survey.views import survey_import_view, survey_configuration_export_view, survey_clone_view, add_collaborator_view
from django.urls import path
from django.conf.urls import url

from survey.views import csv_result_view, survey_import_view, response_number_view

urlpatterns = [
    url(r'^exportCsv/(?P<survey_id>[0-9]+)$', csv_result_view.csv_export),
    url(r'^import/(?P<researcher_id>[0-9]+)$', survey_import_view.import_survey),
    url(r'^exportSurvey/(?P<survey_id>[0-9]+)$', survey_configuration_export_view.export_survey),
    url(r'^responseNumber/(?P<survey_id>[0-9]+)$', response_number_view.response_number),
    url(r'^cloneSurvey/(?P<survey_id>[0-9]+)/(?P<researcher_id>[0-9]+)/(?P<to_language>[a-z]+)$', survey_clone_view.clone_survey),
    url(r'^add-collaborator/', add_collaborator_view.update_collaborator),
    # get: get all the collaborators of specific survey
    url(r'^collaborators/survey/(?P<id>[0-9]+)$', add_collaborator_view.get_collaborator),
    url(r'^collaborators/delete/$', add_collaborator_view.delete_collaborator),
]

