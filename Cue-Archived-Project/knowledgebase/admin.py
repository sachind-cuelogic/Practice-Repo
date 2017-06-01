from django.contrib import admin
from django.utils.translation import ugettext as _

from knowledgebase.models import(
    Category,
    Topic,
    QuestionAnswer,
    Notification,
    QuestionReviewNote,
    QuestionAnswerFlag
)


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'state', 'date_added',)
    list_filter = ('difficulty_level', 'categories', 'topics',
                   'state', 'date_added')
    search_fields = ('question',)
    ordering = ('state',)
    list_display_links = ('question',)
    filter_horizontal = ('categories', 'topics',)

    def publish(self, request, queryset):
        questions_updated = queryset.update(state=3)
        message = _("%s Question were") % questions_updated
        self.message_user(request,
                          _("%s successfully marked as published.") % message)

    publish.short_description = _("Publish selected Question Answers")

    def unpublish(self, request, queryset):
        questions_updated = queryset.update(state=1)
        message = _("%s Question were") % questions_updated
        self.message_user(request,
                          _("%s successfully unpublished.") % message)

    unpublish.short_description = _("Unpublish selected Question Answers")

    actions = [publish, unpublish]

    def save_model(self, request, questionanswer, form, change):
        questionanswer.current_user = request.user
        questionanswer.save()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name', 'mentors',)
    filter_horizontal = ('mentors',)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name', 'categories')
    filter_horizontal = ('categories',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(Notification)
admin.site.register(QuestionReviewNote)
admin.site.register(QuestionAnswerFlag)
