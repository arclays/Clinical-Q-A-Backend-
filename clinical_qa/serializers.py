from rest_framework import serializers
from .models import DS_Questions, DS_Answers, DS_Views,CustomQuestion
from django.db.models import  Sum

class DSAnswerSerializer(serializers.ModelSerializer):
    # """Serializer for reading answers"""
    question_text = serializers.CharField(source="question.question", read_only=True)

    class Meta:
        model = DS_Answers
        fields ='__all__'

class DSAnswerCreateUpdateSerializer(serializers.ModelSerializer):
    # """Serializer for creating/updating answers"""

    class Meta:
        model = DS_Answers
        fields = ["question", "answer"]
        

class CustomQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = ['id', 'question_text', 'requestors_contact', 'date_of_request', 'is_answered']
        read_only_fields = ['date_of_request']



class CustomQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = ["question_text", "requestors_contact", "is_answered"]

class CustomQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = ["question_text", "requestors_contact", "is_answered"]


class QuestionSerializer(serializers.ModelSerializer):
    answer_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DS_Questions
        fields = ['id', 'question', 'disease', 'status', 'created_at', 'updated_at', 'answer_count', 'view_count']
        read_only_fields = ['created_at', 'updated_at', 'answer_count', 'view_count']
    
    def get_answer_count(self, obj):
        return DS_Answers.objects.filter(question=obj).count()
    
    def get_view_count(self, obj):
        views = DS_Views.objects.filter(question=obj)
        return views.aggregate(total_views=Sum('number_of_clicks'))['total_views'] or 0

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DS_Questions
        fields = ['question', 'disease', 'status']

class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DS_Questions
        fields = ['question', 'disease', 'status']

class QuestionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DS_Questions
        fields = ['status']