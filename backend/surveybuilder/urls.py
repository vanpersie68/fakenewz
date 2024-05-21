from django.conf.urls import url
from surveybuilder.views import survey_view, block_view, question_view, common_view, \
    social_media_question_view, \
    button_row_question_view, multi_choice_question_view, drag_drop_question_view
from surveybuilder.views import text_entry_question_view, randomSections_view, number_scale_question_view, rank_question_view,matrix_table_question_view,sliders_question_view,groups_question_view

urlpatterns = [
    # patch/: number scale questions by ID, for handling buttons
    url(r'^questions/numberScale/(?P<id>[0-9]+)', number_scale_question_view.number_scale_info),
    # get/patch/: text entry questions by ID, for handling buttons
    url(r'^questions/textentry/(?P<id>[0-9]+)', text_entry_question_view.text_entry_info),
    # post: duplicates a block
    url(r'^blocks/duplicate/(?P<id>[0-9]+)', block_view.duplication_block),
    # post: duplicates a question
    url(r'^questions/duplicate/(?P<id>[0-9]+)', question_view.duplication_question),
    # get/delete/patch/post: multichoice questions by ID, for handling buttons
    url(r'^questions/multi/(?P<id>[0-9]+)', multi_choice_question_view.choices_data),
    url(r'^questions/rank/(?P<id>[0-9]+)', rank_question_view.choices_data),
    # patch: multichoice question by ID
    url(r'^questions/multiChoice/(?P<id>[0-9]+)', multi_choice_question_view.multiple_choice_data),
    url(r'^questions/matrixTable/(?P<id>[0-9]+)', matrix_table_question_view.multiple_choice_data),
    url(r'^questions/groups/(?P<id>[0-9]+)', groups_question_view.groups_data),
    # get/delete/patch/post: buttonrow questions by ID, for handling buttons
    url(r'^questions/buttonrow/(?P<id>[0-9]+)', button_row_question_view.buttonrow_data),
    # get/delete/patch/post: drag and drop questions by ID, for handling cards
    # url(r'^questions/draganddrop/(?P<id>[0-9]+)/cards$', drag_drop_question_view.dragdropcard_data),
    # get/delete/patch/post: drag and drop questions by ID, for handling categories
    # url(r'^questions/draganddrop/(?P<id>[0-9]+)/choices$', drag_drop_question_view.dragdropchoice_data),
    # get/delete/patch/post: 
    url(r'^questions/buttonrow/(?P<id>[0-9]+)', button_row_question_view.buttonrow_data),
    # get/delete/patch/post:
    url(r'^questions/postaddonfield/(?P<id>[0-9]+)', social_media_question_view.postAddonField_data),
    # patch: questions subtype by ID
    url(r'^questions/inner/(?P<id>[0-9]+)', question_view.question_inner),
    # patch: question image by ID
    url(r'^questions/image/(?P<id>[0-9]+)', question_view.question_image),
    # get/patch/delete: questions by ID
    url(r'^questions/(?P<id>[0-9]+)', question_view.question_info),
    url(r'^questions/patchMatrixTableQuestion', matrix_table_question_view.question_config),
    url(r'^questions/patchSlidersQuestion', sliders_question_view.question_config),
    url(r'^questions/patchGroupsQuestion', groups_question_view.question_config),
    url(r'^questions/comment/(?P<id>[0-9]+)', question_view.comment),
    # post: returns all article information
    url(r'^article', social_media_question_view.article_information),
    # get: return all video information
    url(r'^video', social_media_question_view.video_information),
    # get/post: questions in a block, post should create the type too
    url(r'^blocks/(?P<id>[0-9]+)/questions$', question_view.question_list),
    # get/delete: find blocks ID
    url(r'^blocks/(?P<id>[0-9]+)$', block_view.block_info),
    # get/post: blocks in a given survey
    url(r'^surveys/(?P<id>[0-9]+)/blocks$', block_view.block_list),
    # get: returns a survey with its blocks and questions. 
    url(r'^surveys/(?P<id>[0-9]+)/data$', survey_view.survey_data),
    # get/patch/delete: a survey by its ID
    url(r'^surveys/(?P<id>[0-9]+)$', survey_view.survey_info),
    # get: get all the surveys created by the researcher
    url(r'^surveys/researcher/(?P<researcher_id>[0-9]+)$', survey_view.survey_list),
    # get: get all the deleted surveys created by the researcher
    url(r'^surveys/deleted/(?P<researcher_id>[0-9]+)$', survey_view.survey_deleted_list),
    # get/post  get or create survey code to generate share link
    url(r'^surveys/code/(?P<id>[0-9]+)$', survey_view.survey_code),
    # post: create a new survey
    url(r'^surveys', survey_view.create_survey),
    # patch/get  add,update or get a randomSection info of a survey
    url(r'^randomSections/(?P<survey_id>[0-9]+)$', randomSections_view.randomSections_info),
    # post: create a new subset info to a survey
    url(r'^randomSections', randomSections_view.create_randomSections),
    url(r'^common/upload', common_view.upload),
    url(r'^common/avatar', common_view.avatar),
]

