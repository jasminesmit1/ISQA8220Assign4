from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render, HttpResponseRedirect
from .models import *
from django.forms.models import inlineformset_factory, modelformset_factory
from quizzes.forms import AnswerModelForm, QuizModelForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin


# Create your views here.
class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerQuizMixin(OwnerMixin, LoginRequiredMixin):
    model = Quiz
    fields = ['name', 'questions_count', 'description', 'roll_out']
    success_url = reverse_lazy('manage_quiz_list')


class OwnerQuizEditMixin(OwnerQuizMixin, OwnerEditMixin):
    fields = ['name', 'questions_count', 'description', 'roll_out']
    success_url = reverse_lazy('manage_quiz_list')
    template_name = 'quizzes/manage/quiz/form.html'


class ManageQuizListView(OwnerQuizMixin, ListView):
    template_name = 'quizzes/manage/quiz/list.html'


class QuizCreateView(PermissionRequiredMixin,
                       OwnerQuizEditMixin,
                       CreateView):
    permission_required = 'quizzes.add_quiz'
    # template_name = 'quizzes/manage/quiz/form.html'
    success_url = reverse_lazy('manage_course_list')

def createQuiz(request):
    quiz = QuizModelForm()
    QuizFormset = inlineformset_factory(Quiz, Question,  fields=('label', 'order',), extra=5)
    if request.method == 'POST':
        # print(request.method)
        formset = QuizFormset(request.POST)
        quiz = QuizModelForm(request.POST)
        if formset.is_valid() and quiz.is_valid():
            # print('HI')
            instance = quiz.save(commit=False)
            instance.owner = request.user
            instance.save()
            fset = formset.save(commit=False)
            for item in fset:
                item.quiz = instance
                item.save()
            quiz_list = Quiz.objects.filter(owner=instance.owner)
        else:
            quiz = QuizModelForm()
        return render(request, 'quizzes/manage/quiz/list.html', {'quiz_list': quiz_list})
    formset = QuizFormset()
    quiz = QuizModelForm()
    return render(request, 'quizzes/manage/quiz/formset.html', {'formset': formset, 'quiz': quiz})


def createAnswers(request, pk):
        AnswerFormset = AnswerModelForm
        quiz_list = Quiz.objects.all()
        if request.method == 'POST':
            form = AnswerFormset(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'quizzes/manage/quiz/list.html', {'quiz_list': quiz_list})
        form = AnswerFormset()
        return render(request, 'quizzes/manage/answers/formset.html', {'form': form})

# class createAnswers(CreateView):
#         form_class = AnswerModelForm
#         # queryset = Question.objects.filter(quiz=pk)
#         template_name = 'quizzes/manage/answers/formset.html'
#         success_url = 'quizzes/manage/quiz/list.html'

        # def get_form(self, form_class=form_class):
        #     form = super(createAnswers, self).get_form(form_class)
        #     # for form in formset:
        #     form.fields['question'].queryset = Question.objects.filter(
        #         quiz=self.kwargs['pk'])
        #     print(form)
        #     return form
        #
        # def form_valid(self, form_class):
        #     """If the form is valid, save the associated model."""
        #     self.object = form_class.save()
        #
        #
        # def post(self, request, *args, **kwargs):
        #     """
        #     Handle POST requests: instantiate a form instance with the passed
        #     POST variables and then check if it's valid.
        #     """
        #     form = self.get_form()
        #     if form.is_valid():
        #         return self.form_valid(form)
        #     else:
        #         return self.form_invalid(form)

        # def __init__(self, *args, **kwargs):
        #     self.my_var = kwargs.pop('my_var')
        #     super(TaskcreateForm, self).__init__(*args, **kwargs)
        #     self.fields['projects'].queryset = Project.objects.filter(type=self.my_var))

        # def get_initial(self, form_class=form_class):
        #     formset = super(createAnswers, self).queryset
        #     formset.fields['question'].query = Question.objects.filter(quiz=self.kwargs['pk'])
        #     return self.initial.copy()



        # quiz = Quiz.objects.filter(id=pk)
        # if request.method == 'POST':
        #     formset = AnswerFormset(request.POST)
        #     if formset.is_valid():
        #         fset = formset.save(commit=False)
        #         for item in fset:
        #             item.save()
        #         return render(request, 'quizzes/manage/quiz/list.html')
        # formset = AnswerFormset()
        # return render(request, 'quizzes/manage/answers/formset.html', {'formset': formset}, {'quiz': quiz})

class QuizUpdateView(PermissionRequiredMixin,
                       OwnerQuizEditMixin,
                       UpdateView):
    permission_required = 'quizzes.change_quiz'


class QuizDeleteView(PermissionRequiredMixin,
                       OwnerQuizMixin,
                       DeleteView):
    template_name = 'quizzes/manage/quiz/delete.html'
    success_url = reverse_lazy('manage_quiz_list')
    permission_required = 'quizzes.delete_quiz'
