from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Course, User
from quizzes.models import *
from .models import Module, Content, Subject, QuizItem
from .forms import ModuleFormSet
from django.db.models import Count
from students.forms import CourseEnrollForm
from quizzes.forms import QuizModelForm
from students.views import StudentCourseDetailView


# Create your views here.
class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file', 'quizitem']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)

        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                       id=module_id,
                                       course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView,
           self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                   course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__course__owner=request.user) \
                       .update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                    total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
        courses = Course.objects.annotate(
                    total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
                                    initial={'course': self.object})
        return context


# @method_decorator([login_required], name='dispatch')
class Profile(View):
    model = User

    def dispatch(self, request, *args, **kwargs):
        group = request.user.get_group_permissions()
        if 'courses.add_course' in group:
            return redirect('manage_course_list')
        else:
            return redirect('student_course_list')
        return super(Profile, self).dispatch(request, *args, **kwargs)


def home(request):
    return redirect('profile')


def take_quiz(request, pk, model_name, *args, **kwargs):
    context = QuizItem.objects.filter(title=model_name, id=pk).get()
    print(context)
    quiz = Quiz.objects.filter(id=context.quiz_id).get()
    print(quiz)
    questions = Question.objects.all().filter(quiz=quiz)
    print(questions)
    # for question in questions:
    answers = Answer.objects.all().filter(question__in=questions)
    correct = []
    text = []
    for answer in answers:
        text.append(answer.text)
        if answer.is_correct:
            correct.append(answer.text)
    print(answers)
    print(correct)
    print(text)
    return render(request, 'courses/content/quiz_detail.html', {'quiz': quiz, 'questions': questions,
                                                                'answers': answers, 'correct': correct, 'text': text})


# def quiz_view(request, pk, module_id):
#     print(request)
#     quiz = Question.objects.all().filter(answers=module_id)
#     if not quiz:
#         quiz = Quiz.objects.annotate(
#                     total_courses=Count('name'))
#         cache.set('all_quizzes', quiz)
#         questions = Question.objects.annotate(
#             total_modules=Count('label'))
#         answers = Answer.objects.annotate(
#                     total_modules=Count('question'))
#         if quiz:
#             questions = get_object_or_404(Question, id=questions.id)
#             answers = answers.filter(question=questions)
#     return redirect ({'questions': questions, 'answers': answers, 'quiz': quiz})
#
# class QuizDetailView(DetailView):
#     template_name = 'courses/content/quiz_detail.html'
#     queryset = Quiz

    # def get_context_data(self, **kwargs):
    #     context = super(QuizDetailView, self).get_context_data(**kwargs)
    #     # get quiz object
    #     quiz = self.get_object()
    #     if 'module_id' in self.kwargs:
    #         # get current answers
    #         context['answers'] = question.label.get(id=self.kwargs['module_id'])
    #
    #     else:
    #         # get first answers
    #         context['quiz'] = quiz.answers.all()[0]
    #     # # print(context['answers'].id)
    #     # group = Content.objects.all().filter(answers=context['answers'].id)
    #     # # for i in type:
    #     # #     print(i.content_type)
    #     print(self)
    #     # print(context)
    #     return context

