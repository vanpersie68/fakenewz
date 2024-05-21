from surveybuilder.models import SocialPostQuestion, ButtonRowQuestion, ButtonQuestion, TextboxQuestionText, MultiChoiceQuestion, MultiChoice, NumberScaleQuestion, DragAndDropQuestion, DragAndDropChoice, DragAndDropCard,RankOrderQuestion,MatrixTableQuestion,SlidersQuestion,GroupsQuestion
from surveybuilder.serializers import SocialPostQuestionSerializer, ButtonRowQuestionSerializer, ButtonQuestionSerializer, TextboxQuestionTextSerializer, MultiChoiceSerializer, MultiChoiceQuestionSerializer, NumberScaleQuestionSerializer, DragAndDropChoiceSerializer, DragAndDropQuestionSerializer, DragAndDropCardSerializer,RankOrderQuestionSerializer,MatrixTableQuestionSerializer,SlidersQuestionSerializer,GroupsQuestionSerializer

questionTypeSerializer = {
    "News post": SocialPostQuestionSerializer,
    "Button row": ButtonRowQuestionSerializer,
    "buttonquestion": ButtonQuestionSerializer,
    "Text entry": TextboxQuestionTextSerializer,
    "Multiple choice": MultiChoiceQuestionSerializer,
    "Rank order": RankOrderQuestionSerializer,
    "Matrix table": MatrixTableQuestionSerializer,
    "Sliders": SlidersQuestionSerializer,
    "Groups": GroupsQuestionSerializer,
    "multichoice": MultiChoiceSerializer,
    "Number scale": NumberScaleQuestionSerializer,
    "Drag and drop": DragAndDropQuestionSerializer,
    "Drag and drop card": DragAndDropCardSerializer,
    "Drag and drop choice": DragAndDropChoiceSerializer
}

questionTypeModel = {
    "News post": SocialPostQuestion,
    "Button row": ButtonRowQuestion,
    "buttonquestion": ButtonQuestion,
    "Text entry": TextboxQuestionText,
    "Multiple choice": MultiChoiceQuestion,
    "Rank order": RankOrderQuestion,
    "Matrix table": MatrixTableQuestion,
    "Sliders": SlidersQuestion,
    "Groups": GroupsQuestion,
    "multichoice": MultiChoice,
    "Number scale": NumberScaleQuestion,
    "Drag and drop": DragAndDropQuestion,
    "Drag and drop choice": DragAndDropChoice,
    "Drag and drop card": DragAndDropCard
}
