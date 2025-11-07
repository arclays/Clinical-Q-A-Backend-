from rest_framework import serializers
from django.db.models import Sum
from .models import DS_Questions, DS_Answers, DS_Views, CustomQuestion

class CustomQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = ['id', 'question_text', 'requestors_contact', 'date_of_request', 'is_answered']
        read_only_fields = ['date_of_request']


class CustomQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = ['question_text', 'requestors_contact', 'is_answered']


class CustomQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = ['question_text', 'requestors_contact', 'is_answered']

class DSAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DS_Answers
        fields = ['id', 'answer', 'created_at', 'updated_at']

class DSQuestionSerializer(serializers.ModelSerializer):
    answers = DSAnswerSerializer(many=True, read_only=True)
    answer_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = DS_Questions
        fields = [
            'id', 'question', 'disease', 'status',
            'created_at', 'updated_at',
            'answer_count', 'view_count', 'answers'
        ]

class DSAnswerCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating or updating answers"""
    class Meta:
        model = DS_Answers
        fields = ['question', 'answer']


class DSQuestionSerializer(serializers.ModelSerializer):
    """Main serializer to return question, its answer(s), and views"""
    answers = DSAnswerSerializer(many=True, read_only=True)
    answer_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = DS_Questions
        fields = [
            'id', 'question', 'disease', 'status',
            'created_at', 'updated_at',
            'answer_count', 'view_count', 'answers'
        ]
        read_only_fields = ['created_at', 'updated_at', 'answer_count', 'view_count']

    def get_answer_count(self, obj):
        return DS_Answers.objects.filter(question=obj).count()

    def get_view_count(self, obj):
        views = DS_Views.objects.filter(question=obj)
        return views.aggregate(total_views=Sum('number_of_clicks'))['total_views'] or 0


class DSQuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating questions"""
    class Meta:
        model = DS_Questions
        fields = ['question', 'disease', 'status']


class DSQuestionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DS_Questions
        fields = ['status']
