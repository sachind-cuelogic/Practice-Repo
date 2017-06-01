import os, sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
sys.path.append(rootDir)
os.environ["DJANGO_SETTINGS_MODULE"] = "prepairit.settings"

import django
django.setup()

import csv
import psycopg2

from knowledgebase.models import Category, Topic, QuestionAnswer
from ppiauth.models import PPIUser

def populate():
    admin = PPIUser.objects.get_or_create(email="admin@prepair.it")[0]
    populate_database_reader = csv.reader(open('populate_database.csv','rb'))

    for populate_data in populate_database_reader:
        category_add(name=populate_data[0],
            user=admin)
        topic_add(name=populate_data[1],
            user=admin,
            categories=Category.objects.filter(name__iexact=populate_data[0])[0])
        question_answer_add(question=populate_data[2],
            answer=populate_data[3],
            user=admin,
            difficulty_level=populate_data[4],
            categories=Category.objects.filter(name__iexact=populate_data[0])[0],
            topics=Topic.objects.filter(name__iexact=populate_data[1])[0])


def category_add(name, user):
    if not Category.objects.filter(name__iexact=name):
        category = Category.objects.get_or_create(name=name, user=user)[0]
        category.save()
        return category

def topic_add(name,user,categories):
    if not Topic.objects.filter(name__iexact=name):
        topic = Topic.objects.get_or_create(name=name, user=user)[0]
        topic.categories.add(categories)
        topic.save()
        return topic

def question_answer_add(question,answer,user,difficulty_level,categories,topics):
    question_answer = QuestionAnswer.objects.get_or_create(question=question,
        answer=answer,user=user)[0]
    question_answer.difficulty_level = difficulty_level
    question_answer.categories.add(categories)
    question_answer.topics.add(topics)
    question_answer.save()
    return question_answer

# Start execution here!
if __name__ == '__main__':
    populate()
