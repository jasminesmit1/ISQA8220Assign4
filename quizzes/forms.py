from django import forms
from django.forms.models import inlineformset_factory
from .models import Quiz, Question, Answer


#Create custom form with specific queryset:
class QuizModelForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ('created','owner', 'questions_count')

class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerModelForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'


QuizFormset1 = inlineformset_factory(Quiz,
                                       Question,
                                       fields=('label','order',),
                                       can_delete=True)

