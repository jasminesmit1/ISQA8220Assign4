from django.contrib import admin
from .forms import QuizModelForm
from .models import Quiz, Question, Answer, Response, QuizTakers


# Register your models here.
class AnswerInline(admin.ModelAdmin):
    model = Answer
    extra = 4
    max = 4


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerInline, ]
    extra = 19


class QuizAdmin(admin.ModelAdmin):
    form = QuizModelForm
    inlines = [QuestionInline, ]


class ResponseInline(admin.StackedInline):
    model = Response


class QuizTakersAdmin(admin.ModelAdmin):
    inlines = [ResponseInline, ]



admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer, AnswerInline)
admin.site.register(QuizTakers, QuizTakersAdmin)
admin.site.register(Response, )
