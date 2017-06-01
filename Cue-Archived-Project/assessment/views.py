import random

from django.http import HttpResponse
from django.shortcuts import render

from knowledgebase.models import Category, Topic, QuestionAnswer
from core.utils import pagination
from knowledgebase.views import replacestring


def create_practice_test(request):
    categories = Category.objects.all()
    print "categories==>",categories
    topics = Topic.objects.all()
    print "topics==>",topics
    question = QuestionAnswer.objects.all()
    print "question==>",question
    response = render(request, 'assessment/create_practice_test.html',
                      {'categories': categories, 'topics': topics,
                       'question': question})
    return response

# Function for fetching the contents from url


def fetch_contents(request):
    data = request.COOKIES.get('take_test')
    data = data.split('&')
    no_of_questions = int(data[0])
    question_ids = replacestring(data[1])
    return no_of_questions, question_ids

# Function for filtering questions based on category, topics and
# difficulty levels


def filter_questions(category_id, topic_list, difficulties):
    category = Category.objects.filter(id=category_id)
    all_topics = Topic.objects.all()
    difficulties = [int(difficulty) for difficulty in difficulties]
    difficulty_questions = QuestionAnswer.objects.filter(
        state=QuestionAnswer.QuestionAnswerState.PUBLISH,
        is_delete=False,
        difficulty_level__in=difficulties)
    if topic_list:
        topics = [topic for topic_id in topic_list
                  for topic in all_topics.filter(id=topic_id)]
    else:
        topics = [topic for topic in all_topics.filter(categories=category)]

    if category:
        if topics:
            questions = [question for topic in topics
                         for question in difficulty_questions.filter(
                             categories=category,
                             topics=topic)]
        else:
            questions = [
                question for question in difficulty_questions.filter(
                    categories=category)]
    else:
        if topics:
            questions = [question for topic in topics
                         for question in difficulty_questions.filter(
                             topics=topic)]
        else:
            questions = difficulty_questions
    return questions


def take_practice_test(request):
    existing_answer = ""
    if request.method == 'POST':
        data = request.POST
        category_id = data.get('category')
        topic_list = data.getlist('topic_filter')
        no_of_questions = int(data.get('ques'))
        difficulties = data.getlist('difficulty')
        questions = filter_questions(category_id, topic_list, difficulties)
        question_ids = [question.id for question in questions]
        random.shuffle(question_ids)
        question_ids = question_ids[:no_of_questions]
        test_data = str(no_of_questions)+"&"+str(question_ids)

    else:
        no_of_questions, question_ids = fetch_contents(request)

    questions = [question for qid in question_ids
                 for question in QuestionAnswer.objects.filter(id=qid)]
    question_paginated = pagination(request, questions, count=1)
    response = render(request, 'assessment/take_practice_test.html',
                          {'questions': question_paginated,
                           'no_of_questions': no_of_questions})

    if request.method == 'POST':
        response.set_cookie('take_test', test_data)
        expires = 3 * 3600
        response.cookies['take_test']['expires'] = expires
    return response


def practice_test_result(request):
    no_of_questions, question_ids = fetch_contents(request)
    questions = [question for qid in question_ids
                 for question in QuestionAnswer.objects.filter(id=qid)]
    question_paginated = pagination(request, questions, count=1)
    response = render(request, 'assessment/practice_test_result.html',
                          {'questions': question_paginated,
                           'no_of_questions': no_of_questions})
    return response

# Function for checking whether questions exists or not


def check_results(request):
    if request.is_ajax():
        data = request.GET
        category_id = int(data.get('category_id'))
        topic_list = data.getlist('topic_list[]')
        difficulties = data.getlist('difficulty[]')
        questions = filter_questions(category_id, topic_list, difficulties)
    return HttpResponse(len(questions))
