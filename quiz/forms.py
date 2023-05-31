from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from .models import Question, Choice, Category, Message

User = get_user_model()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['author', 'category']

        def __init__(self, *args, **kwargs):
            self.author = kwargs.pop('author', None)
            super().__init__(*args, **kwargs)
            self.fields['category'].widget.attrs.update(
                {'class': 'form-control'})

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.author = self.author
            if commit:
                instance.save()
            return instance


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['author', 'question', 'category', 'image']

        def __init__(self, *args, **kwargs):
            self.author = kwargs.pop('author', None)
            super().__init__(*args, **kwargs)
            self.fields['question'].widget.attrs.update(
                {'class': 'form-control'})
            self.fields['image'].widget.attrs.update(
                {'class': 'form-control-file'})

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.author = self.author
            if commit:
                instance.save()
            return instance


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'message']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 80})
        }


class ChoiceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ChoiceInlineFormset, self).clean()

        correct_choices_count = 0
        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and form.cleaned_data.get('is_correct') is True:
                correct_choices_count += 1

        try:
            assert correct_choices_count == Question.ALLOWED_NUMBER_OF_CORRECT_CHOICES
        except AssertionError:
            raise forms.ValidationError(
                _('Exactly one correct choice is allowed.'))
