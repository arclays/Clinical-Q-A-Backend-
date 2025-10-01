
# # Create your tests here.




# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def question_list_create(request):
#     """
#     List all questions or create a new question
#     """
#     if request.method == 'GET':
#         questions = DS_Questions.objects.all()

#         # Filters
#         if status_filter := request.query_params.get('status'):
#             questions = questions.filter(status=status_filter)

#         if disease := request.query_params.get('disease'):
#             questions = questions.filter(disease__icontains=disease)

#         if search := request.query_params.get('search'):
#             questions = questions.filter(question__icontains=search)

#         # Ordering
#         order_by = request.query_params.get('order_by', 'created_at')
#         if order_by in ['created_at', 'updated_at', 'disease']:
#             questions = questions.order_by(order_by)

#         # Popular filter
#         if request.query_params.get('popular'):
#             questions = questions.annotate(
#                 total_views=Sum('ds_views__number_of_clicks')
#             ).order_by('-total_views')

#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = QuestionCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             question = serializer.save()
#             DS_Views.objects.create(question=question, number_of_clicks=0)
#             return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def question_detail(request, pk):
#     """
#     Retrieve, update or delete a question
#     """
#     question = get_object_or_404(DS_Questions, pk=pk)

#     if request.method == 'GET':
#         # Increment view count
#         view, created = DS_Views.objects.get_or_create(
#             question=question, defaults={'number_of_clicks': 1}
#         )
#         if not created:
#             view.number_of_clicks += 1
#             view.save()
#         return Response(QuestionSerializer(question).data)

#     elif request.method == 'PUT':
#         serializer = QuestionUpdateSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(QuestionSerializer(serializer.instance).data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         question.delete()
#         return Response({'message': 'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['PATCH'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def update_question_status(request, pk):
#     """
#     Update only the status of a question
#     """
#     question = get_object_or_404(DS_Questions, pk=pk)
#     serializer = QuestionStatusSerializer(question, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(QuestionSerializer(serializer.instance).data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def question_search(request):
#     """
#     Search questions by text or disease
#     """
#     search_query = request.query_params.get('q', '')
#     if not search_query:
#         return Response({'error': 'Provide query parameter (q)'}, status=status.HTTP_400_BAD_REQUEST)

#     questions = DS_Questions.objects.filter(
#         Q(question__icontains=search_query) | Q(disease__icontains=search_query),
#         status='active'
#     )
#     return Response(QuestionSerializer(questions, many=True).data)


# @api_view(['GET'])
# def popular_questions(request):
#     """
#     Get top 10 popular (most viewed) questions
#     """
#     questions = DS_Questions.objects.filter(status='active').annotate(
#         total_views=Sum('ds_views__number_of_clicks')
#     ).order_by('-total_views')[:10]
#     return Response(QuestionSerializer(questions, many=True).data)


# @api_view(['GET'])
# def questions_with_most_answers(request):
#     """
#     Get top 10 questions with most answers
#     """
#     questions = DS_Questions.objects.filter(status='active').annotate(
#         answer_count=Count('ds_answers')
#     ).order_by('-answer_count')[:10]
#     return Response(QuestionSerializer(questions, many=True).data)

# (
#     DSAnswerSerializer,
#     DSAnswerCreateUpdateSerializer,
#     CustomQuestionSerializer,
#     CustomQuestionCreateSerializer,
#     CustomQuestionUpdateSerializer,
#     QuestionSerializer, 
#     QuestionCreateSerializer, 
#     QuestionUpdateSerializer,
#     QuestionStatusSerializer
# )