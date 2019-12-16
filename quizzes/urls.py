from django.urls import path, include
from . import views

urlpatterns = [
    path('quizzes/', views.ManageQuizListView.as_view(), name='manage_quiz_list'),
    path('create/', views.createQuiz, name='quiz_create'),
    # path('create/', views.createQuiz.as_view(), name='quiz_create'),
    path('<pk>/create/answers/', views.createAnswers, name='answers_create'),
    # path('<pk>/create/answers/', views.createAnswers.as_view(), name='answers_create'),
    path('<pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
]
