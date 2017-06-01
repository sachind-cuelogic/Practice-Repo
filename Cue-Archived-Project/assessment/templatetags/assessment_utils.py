from django import template
from knowledgebase.models import QuestionAnswer

register = template.Library()

@register.assignment_tag
def get_difficulty_levels():
    return QuestionAnswer.DifficultyLevels.choices()
