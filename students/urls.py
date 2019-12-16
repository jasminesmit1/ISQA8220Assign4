from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-quiz/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/',
         views.StudentCourseListView.as_view(),
         name='student_course_list'),
    path('quiz/<pk>/', (views.StudentCourseDetailView.as_view()),
         name='student_course_detail'),
    path('quiz/<pk>/<module_id>/', (views.StudentCourseDetailView.as_view()),
         name='student_course_detail_module'),
]
