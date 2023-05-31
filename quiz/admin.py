from django.contrib import admin
from .models import Question, Choice, Category, Announcement, Message, QuizProfile, ContactMessage
from .forms import QuestionForm, ChoiceForm, ChoiceInlineFormset, MessageForm, CategoryForm


class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICE_COUNT
    min_num = Choice.MAX_CHOICE_COUNT
    form = ChoiceForm
    formset = ChoiceInlineFormset


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline,)
    list_display = ['author', 'category', 'question',
                    'image', 'created_at', 'updated_at']
    search_fields = ['category', 'author', 'choices__choice_text', 'question']
    actions = None
    form = QuestionForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.author = request.user  # Set the author to the current logged-in user
        return form


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['author', 'category']
    list_display_links = ['author', 'category']
    form = CategoryForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.author = request.user  # Set the author to the current logged-in user
        return form


class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    list_display = ['title', 'created_at', 'updated_at']


class QuizProfileAdmin(admin.ModelAdmin):
    model = QuizProfile
    list_display = ['user', 'total_score', 'question']


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['sender', 'recipient', 'message',
                    'sent', 'received', 'created_at', 'updated_at']
    form = MessageForm


class ContactMessageAdmin(admin.ModelAdmin):
    model = ContactMessage
    list_display = ['first_name', 'last_name', 'email_address',
                    'phone_number', 'message', 'created_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(QuizProfile, QuizProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
