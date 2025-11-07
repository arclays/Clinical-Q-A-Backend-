from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DS_Answers, DS_Questions, CustomQuestion
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.db import connection

from .models import DS_Answers, CustomQuestion,DS_Questions, DS_Views
from .serializers import *

@api_view(['GET'])
@permission_classes([])
def health_check(request):
    # Check database connection
    try:
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return Response({
        "status": "healthy",
        "message": "Django backend is running",
        "timestamp": timezone.now().isoformat(),
        "database": db_status,
        "endpoints_available": True
    })
# DS_Answers
@api_view(["GET", "POST"])
@permission_classes([])
def answer_list_create(request):

    if request.method == "GET":
        answers = DS_Answers.objects.all()
        question_id = request.query_params.get("question_id")
        if question_id:
            answers = answers.filter(question_id=question_id)

        serializer = DSAnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = DSAnswerCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the related question is active
            question = serializer.validated_data["question"]
            if question.status != "active":
                return Response(
                    {"error": "Cannot add answer to a disabled question."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return Response(
                DSAnswerSerializer(serializer.instance).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([])
def answer_detail(request, pk):
    answer = get_object_or_404(DS_Answers, pk=pk)

    if request.method == "GET":
        serializer = DSAnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = DSAnswerCreateUpdateSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            # Ensure the related question is still active
            if "question" in serializer.validated_data:
                question = serializer.validated_data["question"]
                if question.status != "active":
                    return Response(
                        {"error": "Cannot reassign answer to a disabled question."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            serializer.save()
            return Response(
                DSAnswerSerializer(serializer.instance).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        answer.delete()
        return Response(
            {"message": "Answer deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

@api_view(["GET"])
def answers_by_question(request, question_id):

    # Retrieve all answers for a specific question (only if the question is active).
    question = get_object_or_404(DS_Questions, id=question_id, status="active")
    answers = DS_Answers.objects.filter(question=question)

    serializer = DSAnswerSerializer(answers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# custom_questions
@api_view(["GET", "POST"])
@permission_classes([])
def custom_questions_list_create(request):
    # List all custom questions and create a new custom_question
    if request.method == "GET":
        questions = CustomQuestion.objects.all()

        # Optional filters
        is_answered = request.query_params.get("is_answered")
        if is_answered is not None:
            if is_answered.lower() == "true":
                questions = questions.filter(is_answered=True)
            elif is_answered.lower() == "false":
                questions = questions.filter(is_answered=False)

        date = request.query_params.get("date")
        if date:
            questions = questions.filter(date_of_request__date=date)

        serializer = CustomQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CustomQuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                CustomQuestionSerializer(serializer.instance).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([])
def custom_question_detail(request, pk):
    # Retrieve, update, partially update, or delete a custom question
    custom_question = get_object_or_404(CustomQuestion, pk=pk)

    if request.method == "GET":
        serializer = CustomQuestionSerializer(custom_question)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CustomQuestionUpdateSerializer(custom_question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomQuestionSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = CustomQuestionUpdateSerializer(
            custom_question, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(CustomQuestionSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        custom_question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["PATCH"])
@permission_classes([])
def toggle_custom_question_answered(request, pk):
    # Unanswered state
    custom_question = get_object_or_404(CustomQuestion, pk=pk)
    custom_question.is_answered = not custom_question.is_answered
    custom_question.save()
    return Response(CustomQuestionSerializer(custom_question).data)

@api_view(["GET"])
def custom_question_search(request):
    # Search custom questions by text or requestor's contact
    query = request.query_params.get("q", "").strip()
    if not query:
        return Response(
            {"error": "Please provide a search query parameter (?q=...)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = CustomQuestion.objects.filter(
        Q(question_text__icontains=query)
        | Q(requestors_contact__icontains=query)
    )
    serializer = CustomQuestionSerializer(results, many=True)
    return Response(serializer.data)

# DS questions
@api_view(['GET', 'POST'])
@permission_classes([])
def question_list_create(request):  
    # List all questions or create a new question   
    if request.method == 'GET':
        questions = DS_Questions.objects.all()
        status_filter = request.query_params.get('status')
        if status_filter:
            questions = questions.filter(status=status_filter)   
        disease = request.query_params.get('disease')
        if disease:
            questions = questions.filter(disease__icontains=disease)   
        search = request.query_params.get('search')
        if search:
            questions = questions.filter(question__icontains=search)        
        order_by = request.query_params.get('order_by', 'created_at')
        if order_by in ['created_at', 'updated_at', 'disease']:
            questions = questions.order_by(order_by)
        popular = request.query_params.get('popular')
        if popular:
            questions = questions.annotate(
                total_views=Sum('ds_views__number_of_clicks')
            ).order_by('-total_views')
            
        serializer = DSQuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create a new question
        serializer = DSQuestionCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            
            # Create an initial view record for the new question
            DS_Views.objects.create(question=question, number_of_clicks=0)
            
            return Response(
                DSQuestionSerializer(question).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([])
def question_detail(request, pk):

    # Retrieve, update or delete a question
    try:
        question = DS_Questions.objects.get(pk=pk)
    except DS_Questions.DoesNotExist:
        return Response(
            {'error': 'Question not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        # Increment view count when a question is viewed
        view, created = DS_Views.objects.get_or_create(
            question=question,
            defaults={'number_of_clicks': 1}
        )
        if not created:
            view.number_of_clicks += 1
            view.save()
        
        serializer = DSQuestionSerializer(question)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = DSQuestionCreateUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(DSQuestionSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        question.delete()
        return Response(
            {'message': 'Question deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['POST'])
@permission_classes([])
def question_click(request, pk):
    # Increment view count when a user clicks on a question.
    # Uses session to ensure unique click per session.
    try:
        question = DS_Questions.objects.get(pk=pk)
    except DS_Questions.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

    session_key = f'clicked_question_{pk}'
    if not request.session.get(session_key, False):
        view, created = DS_Views.objects.get_or_create(
            question=question,
            defaults={'number_of_clicks': 0}
        )
        if not created:
            view.number_of_clicks += 1
            view.save()

        request.session[session_key] = True

    return Response({'message': 'Click registered', 'views': view.number_of_clicks})


@api_view(['PATCH'])
@permission_classes([])
def update_question_status(request, pk):
    # Update only the status of a question
    try:
        question = DS_Questions.objects.get(pk=pk)
    except DS_Questions.DoesNotExist:
        return Response(
            {'error': 'Question not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = DSQuestionCreateUpdateSerializer(question, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(DSQuestionSerializer(serializer.instance).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def questions_by_disease(request, disease_name):
    # Get all questions for a specific disease
    questions = DS_Questions.objects.filter(
        disease__icontains=disease_name, 
        status='active'
    )
    
    serializer = DSQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def question_search(request):
    # Search questions by text or disease
    search_query = request.query_params.get('q', '')
    
    if not search_query:
        return Response(
            {'error': 'Please provide a search query parameter (q)'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    questions = DS_Questions.objects.filter(
        Q(question__icontains=search_query) | 
        Q(disease__icontains=search_query)
    ).filter(status='active')
    
    serializer = DSQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def active_questions(request):
  
    # Get all active questions
    questions = DS_Questions.objects.filter(status='active')
    serializer = DSQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def disabled_questions(request):
    # Get all disabled questions
    questions = DS_Questions.objects.filter(status='disabled')
    serializer = DSQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def popular_questions(request):
   
    # Get popular questions (most viewed) # Get questions annotated with view count and order by it
    questions = DS_Questions.objects.filter(status='active').annotate(
        total_views=Sum('ds_views__number_of_clicks')
    ).order_by('-total_views')[:10]  # Top 10 most viewed questions
    
    serializer = DSQuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def questions_with_most_answers(request):
    # Get questions with the most answers
    questions = DS_Questions.objects.filter(status='active').annotate(
        answer_count=Count('ds_answers')
    ).order_by('-answer_count')[:10]  
    
    serializer = DSQuestionSerializer(questions, many=True)

@api_view(['GET'])
def disease_question_stats(request):
    """
    Returns each disease with the count of its related questions.
    """
    data = (
        DS_Questions.objects
        .filter(status="active")
        .values('disease')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    return Response(data)