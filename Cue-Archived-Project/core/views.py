from django.shortcuts import render
from knowledgebase.models import Category, Topic, QuestionAnswer
from core.models import HomePageConfig
from core.utils import get_latest_entries

def index(request):
    categories = Category.objects.all()
    topics = Topic.objects.all()
    questions = QuestionAnswer.objects.filter(is_delete=False, state=QuestionAnswer.QuestionAnswerState.PUBLISH)
    homepage_display_msg = HomePageConfig.objects.filter(active=True)
    questions = get_latest_entries(categories,questions)
    topics = get_latest_entries(categories,topics)
    
    return render(request, 'core/home.html',
                      {'categories': categories, 'topics': topics,
                       'questions': questions,'homepage_display_msg':homepage_display_msg})

def page_not_found(request):
    return render(request, 'core/page_not_found.html')
