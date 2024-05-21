from tkinter import Grid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



class Survey(models.Model):
    name = models.CharField(max_length=5000, blank=True, default='')
    researcher = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=5000, blank=True, default='')
    consentText = models.CharField(max_length=10000, blank=True, default='')
    current_submission = models.IntegerField(default=0)
    required_submission = models.IntegerField(default=0)
    time_limit_minutes = models.IntegerField(default=60)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    publish_time = models.DateTimeField(blank=True, default=None, null=True)
    expire_time = models.DateTimeField(blank=True, default=None, null=True)
    is_repeat_answer = models.BooleanField(default=True)
    if_capture_gaze = models.BooleanField(default=False)
    duration = models.IntegerField(default=-1)
    code = models.CharField(max_length=5000, blank=True, default='')
    deleted = models.BooleanField(default=False)
    camera = models.BooleanField(default=False)
    collaborator = ArrayField(models.IntegerField(), blank=True, default=list)



class RandomSections(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    display = models.IntegerField(default=1)
    startWith = models.IntegerField(default=None)
    endWith = models.IntegerField(default=None)
    index = models.IntegerField(default=None)


class Block(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    description = models.CharField(max_length=15000, blank=True, default='')
    title = models.CharField(max_length=5000, blank=True, default='')
    order = models.IntegerField(default=None)


class Question(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000, blank=True, default='')
    type = models.CharField(max_length=5000, blank=True, default='')
    description = models.CharField(max_length=5000, blank=True, default='')
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=None)
    image = models.TextField(blank=True, default='')


class SocialPostQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    articleURL = models.URLField(max_length=5000, blank=True, default='')
    articleTitle = models.CharField(max_length=5000, blank=True, default='')
    articleSource = models.CharField(max_length=5000, blank=True, default='')
    articleImageLink = models.CharField(max_length=5000, blank=True, default='')
    articleUser = models.CharField(max_length=5000, blank=True, default='')
    articleStyle = models.CharField(max_length=5000, blank=True, default='Twitter')
    articleSnippet = models.CharField(max_length=5000, blank=True, default='')
    articleLikes = models.IntegerField(default=0)
    articleComments = models.IntegerField(default=0)
    articleShares = models.IntegerField(default=0)
    articleSends = models.IntegerField(default=0)
    articleRetweets = models.IntegerField(default=0)
    articleCommentsOn = models.BooleanField(default=False)
    articleSharesOn = models.BooleanField(default=False)
    articleRetweetsOn = models.BooleanField(default=False)
    articleSendsOn = models.BooleanField(default=False)
    articleLikesOn = models.BooleanField(default=False)
    numberAddon = models.IntegerField(default=0)


class PostAddonfield(models.Model):
    postRow = models.ForeignKey(SocialPostQuestion, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000, blank=True, default='')
    icon = models.CharField(max_length=5000, blank=True, default='')
    count = models.IntegerField(default=0)


class ButtonRowQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    numberButtons = models.IntegerField(default=0)


class ButtonQuestion(models.Model):
    buttonRow = models.ForeignKey(ButtonRowQuestion, on_delete=models.CASCADE)
    buttonText = models.CharField(max_length=5000, blank=True, default='')
    buttonType = models.CharField(max_length=5000, blank=True, default='')
    buttonIcon = models.CharField(max_length=5000, blank=True, default='')
    answered = models.BooleanField(default=False)
    jumpBlockId = models.IntegerField(default=0)


class TextboxQuestionText(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    query = models.CharField(max_length=5000, blank=True, default='')
    validate = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=0)
    textboxMin = models.IntegerField(default=0)
    ansType = models.CharField(max_length=5000, blank=True, default='Text')


class MultiChoiceQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.IntegerField(default=0)
    isDropDown = models.BooleanField(default=False)
    isCheckbox = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)
    multipleAnswers = models.BooleanField(default=False)
    otherInput = models.BooleanField(default=False)
class RankOrderQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.IntegerField(default=0)
    isDropDown = models.BooleanField(default=False)
    isCheckbox = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)
    multipleAnswers = models.BooleanField(default=False)
    otherInput = models.BooleanField(default=False)
class MatrixTableQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.IntegerField(default=0)
    isDropDown = models.BooleanField(default=False)
    isCheckbox = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)
    multipleAnswers = models.BooleanField(default=False)
    otherInput = models.BooleanField(default=False)
    columnConfig = models.TextField(max_length=5000, blank=True, default='[{"label":"Strong disgree","value":"e"},{"label":"Disagree","value":"d"},{"label":"Neutral","value":"c"},{"label":"Agree","value":"b"},{"label":"Strong agree","value":"a"}]')
    tableConfig = models.TextField(max_length=5000, blank=True, default='[{"name":"Default1"},{"name":"Default2"},{"name":"Default3"}]')
class SlidersQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.IntegerField(default=0)
    isDropDown = models.BooleanField(default=False)
    isCheckbox = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)
    multipleAnswers = models.BooleanField(default=False)
    otherInput = models.BooleanField(default=False)
    columnConfig = models.TextField(max_length=5000, blank=True, default='[{"label":"Label1","value":"e"},{"label":"Label2","value":"d"},{"label":"Label3","value":"c"},{"label":"Label4","value":"b"}]')
    tableConfig = models.TextField(max_length=5000, blank=True, default='[{"name":"Choice1"},{"name":"Choice2"},{"name":"Choice3"}]')
    max = models.IntegerField(default=100)
    min = models.IntegerField(default=0)
    grid = models.IntegerField(default=10)
class GroupsQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.IntegerField(default=0)
    isDropDown = models.BooleanField(default=False)
    isCheckbox = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)
    multipleAnswers = models.BooleanField(default=False)
    otherInput = models.BooleanField(default=False)
    columnConfig = models.TextField(max_length=5000, blank=True, default='[{"label":"Label1","value":"e","children":[]},{"label":"Label2","value":"d","children":[]}]')
    tableConfig = models.TextField(max_length=5000, blank=True, default='[{"name":"Choice1"},{"name":"Choice2"},{"name":"Choice3"}]')



class MultiChoice(models.Model):
    question = models.ForeignKey(MultiChoiceQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')

class RankOrder(models.Model):
    question = models.ForeignKey(RankOrderQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')

class MatrixTable(models.Model):
    question = models.ForeignKey(MatrixTableQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')
class Sliders(models.Model):
    question = models.ForeignKey(SlidersQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')
class Groups(models.Model):
    question = models.ForeignKey(GroupsQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')


class NumberScaleQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    minTitle = models.CharField(max_length=5000, blank=True, default='')
    middleTitle = models.CharField(max_length=5000, blank=True, default='')
    maxTitle = models.CharField(max_length=5000, blank=True, default='')
    interval = models.IntegerField(default=1)
    numberMax = models.IntegerField(default=0)
    numberMin = models.IntegerField(default=0)
    minTitleOn = models.BooleanField(default=True)
    midTitleOn = models.BooleanField(default=True)
    maxTitleOn = models.BooleanField(default=True)


# not prioritsing the likert scale for now - will come back if we have time
"""
class LikertScaleQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    numberRows = models.IntegerField(default=None)
    numberChoices = models.IntegerField(default=None)
    #entry = models.CharField(max_length=500, blank=False, default='')
    #minTitle = models.CharField(max_length=5000, blank=False, default='') 
    #middleTitle = models.CharField(max_length=5000, blank=False, default='') 
    #maxTitle = models.CharField(max_length=5000, blank=False, default='') 

class LikertScaleRow(models.Model):
    question = models.ForeignKey(LikertScaleQuestion, on_delete=models.CASCADE) # associated with a likert q
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=False, default='')

class LikertScaleChoices(models.Model):
    question = models.ForeignKey(LikertScaleRow, on_delete=models.CASCADE) # associated with a likert q row
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=False, default='')
"""


class DragAndDropQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # choices are the categories for cards to be sorted into
    choices = models.IntegerField(default=0)
    # cards are the items that will be dragged and sorted
    cards = models.IntegerField(default=0)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)


class DragAndDropCard(models.Model):
    question = models.ForeignKey(DragAndDropQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')


class DragAndDropChoice(models.Model):
    question = models.ForeignKey(DragAndDropQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000, blank=True, default='')
    username = models.CharField(max_length=5000, blank=True, default='')
    avatarUrl = models.CharField(max_length=5000, blank=True, default='/upload/0.5635229252972436WeChat0f76336fb69d8e174d7d6ad50cc53a5d.png')
class Avatar(models.Model):
    url = models.CharField(max_length=5000, blank=True, default='')
    user = models.CharField(max_length=5000, blank=True, default='')

