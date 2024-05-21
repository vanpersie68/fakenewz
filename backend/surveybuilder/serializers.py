from rest_framework import serializers
from django.contrib.auth.models import User

from surveybuilder.models import Avatar, Survey, Block, Question, SocialPostQuestion, ButtonRowQuestion, \
    ButtonQuestion, TextboxQuestionText, MultiChoiceQuestion, \
    MultiChoice, NumberScaleQuestion, DragAndDropQuestion, DragAndDropChoice, DragAndDropCard, PostAddonfield, \
    RandomSections,RankOrder,MatrixTable,MatrixTableQuestion,RankOrderQuestion,Comment,Sliders,SlidersQuestion,Groups,GroupsQuestion


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Add more fields as needed

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'researcher', 'name', 'language', 'consentText', 'time_limit_minutes', 'status',
                  'current_submission', 'required_submission', 'create_time', 'publish_time', 'expire_time',
                  'is_repeat_answer', 'if_capture_gaze', 'code', 'duration', 'deleted', 'camera', 'collaborator']

class BlockSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(max_value=2147483647, min_value=0, required=True)

    class Meta:
        model = Block
        fields = ['id', 'survey', 'title', 'description', 'order']
        extra_kwargs = {'description': {'required': False}}


class RadomSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomSections
        fields = ['survey', 'display', 'startWith', 'endWith', 'index']


class QuestionSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(max_value=2147483647, min_value=0, required=True)

    class Meta:
        model = Question
        fields = ['id', 'block', 'name', 'type', 'description', 'required', 'order', 'image']


class SocialPostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPostQuestion
        fields = ['id', 'question', 'articleURL',
                  'articleTitle', 'articleSource', 'articleImageLink','articleUser', 'articleStyle',
                  'articleSnippet', 'articleLikes', 'articleComments', 'articleShares', 'articleSends', 'articleRetweets',
                  'articleCommentsOn', 'articleSharesOn', 'articleRetweetsOn', 'articleSendsOn', 'articleLikesOn', 'numberAddon']


class PostAddonfieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddonfield
        fields = ['id', 'postRow', 'title', 'icon', 'count']


class ButtonRowQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonRowQuestion
        fields = ['id', 'question', 'numberButtons']


class ButtonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonQuestion
        fields = ['id', 'buttonRow', 'buttonText',
                  'buttonType', 'buttonIcon', 'answered', 'jumpBlockId']


class TextboxQuestionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextboxQuestionText
        fields = ['id', 'question', 'query',
                  'textboxMax', 'textboxMin', 'validate', 'ansType']


class MultiChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoice
        fields = ['id', 'question', 'order', 'title']

class RankOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankOrder
        fields = ['id', 'question', 'order', 'title']
class MatrixTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixTable
        fields = ['id', 'question', 'order', 'title']


class MatrixTableQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixTableQuestion
        fields = ['id', 'question', 'options', 'isDropDown',
                  'isCheckbox', 'textboxMax', 'textboxMin', 'multipleAnswers', 'otherInput', 'columnConfig', 'tableConfig']
class SlidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sliders
        fields = ['id', 'question', 'order', 'title']


class SlidersQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlidersQuestion
        fields = ['id', 'question', 'options', 'isDropDown',
                  'isCheckbox', 'textboxMax', 'textboxMin', 'multipleAnswers', 'otherInput', 'columnConfig', 'tableConfig','min','max','grid']
class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id', 'question', 'order', 'title']


class GroupsQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupsQuestion
        fields = ['id', 'question', 'options', 'isDropDown',
                  'isCheckbox', 'textboxMax', 'textboxMin', 'multipleAnswers', 'otherInput', 'columnConfig', 'tableConfig']

class RankOrderQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankOrderQuestion
        fields = ['id', 'question', 'options', 'isDropDown',
                  'isCheckbox', 'textboxMax', 'textboxMin', 'multipleAnswers', 'otherInput']

class MultiChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoiceQuestion
        fields = ['id', 'question', 'options', 'isDropDown',
                  'isCheckbox', 'textboxMax', 'textboxMin', 'multipleAnswers', 'otherInput']


class NumberScaleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberScaleQuestion
        fields = ['id', 'question', 'minTitle', 'middleTitle',
                  'maxTitle', 'interval', 'numberMax', 'numberMin', 'minTitleOn', 'midTitleOn', 'maxTitleOn']


class DragAndDropChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragAndDropChoice
        fields = ['id', 'question', 'order', 'title']


class DragAndDropCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragAndDropCard
        fields = ['id', 'question', 'order', 'title']


class DragAndDropQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragAndDropQuestion
        fields = ['id', 'question', 'choices', 'cards',
                  'textboxMax', 'textboxMin']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'question', 'content','username','avatarUrl']
class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'user', 'url']

