from django.urls import path
from . import views

urlpatterns = [
    # Ds_answers endpoints
    path("Ds_answers/", views.answer_list_create, name="answer-list-create"),
    path("Ds_answers/<int:pk>/", views.answer_detail, name="answer-detail"),
    path("questions/<int:question_id>/answers/", views.answers_by_question, name="answers-by-question"),
    # custom-questions endpoints
    path("custom-questions/", views.custom_questions_list_create, name="custom-questions-list-create"),
    path("custom-questions/<int:pk>/", views.custom_question_detail, name="custom-question-detail"),
    path("custom-questions/<int:pk>/toggle/", views.toggle_custom_question_answered, name="toggle-custom-question-answered"),
    path("custom-questions/search/", views.custom_question_search, name="custom-question-search"),
    # Ds_questions endpoints
    path('Ds_questions/', views.question_list_create, name='question-list-create'),
    path('Ds_questions/<int:pk>/', views.question_detail, name='question-detail'),
    path('Ds_questions/<int:pk>/status/', views.update_question_status, name='update-question-status'),
    path('Ds_questions/disease/<str:disease_name>/', views.questions_by_disease, name='questions-by-disease'),
    path('Ds_questions/search/', views.question_search, name='question-search'),
    path('Ds_questions/active/', views.active_questions, name='active-questions'),
    path('Ds_questions/disabled/', views.disabled_questions, name='disabled-questions'),
    path('Ds_questions/popular/', views.popular_questions, name='popular-questions'),
    path('Ds_questions/most-answered/', views.questions_with_most_answers, name='questions-with-most-answers'),
]