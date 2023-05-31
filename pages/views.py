from django.shortcuts import render, redirect
from quiz.models import Announcement, ContactMessage, Question, Message, QuizProfile, Category
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, DetailView, TemplateView
from django.contrib import messages
from django.db.models import Count, Sum
import matplotlib.pyplot as plt
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
import base64
from chartjs.views.lines import BaseLineChartView

# Create your views here.


def home(request):
    if request.user.is_superuser == True:
        return redirect('/admin')
    else:
        if request.user.is_authenticated:
            quiz_profile = (
                QuizProfile.objects
                .filter(user=request.user)
                .annotate(total_score_annotation=Sum('total_score'))
                .first()
            )
            messages = Message.objects.filter(recipient=request.user)
            total_messages = len(messages)
            quiz_created_by_user = Question.objects.filter(author=request.user)
            total_quiz_created_by_user = len(quiz_created_by_user)
            quiz_profiles = (
                QuizProfile.objects
                .annotate(total_score_annotation=Sum('total_score'))
                .order_by('-total_score_annotation')
            )

            is_high_score = False
            if quiz_profile.total_score_annotation >= 5000:
                is_high_score = True

            context = {
                'quiz_profiles': quiz_profiles,
                'quiz_profile': quiz_profile,
                'total_messages': total_messages,
                'total_quiz_created_by_user': total_quiz_created_by_user,
                'is_high_score': is_high_score,
            }
            return render(request, 'index.html', context)
        return render(request, 'index.html')


class AboutPageView(TemplateView):
    template_name = 'about.html'


def ContactPageView(request):
    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        message = request.POST.get('message')

        error_message = "Please fill all fields!"

        if len(firstName) <= 0:
            messages.error(request, error_message)
            return redirect('contact_page')
        elif len(lastName) <= 0:
            messages.error(request, error_message)
            return redirect('contact_page')
        elif ContactMessage.objects.filter(email_address=email).exists():
            messages.error(request, "Sorry, you have already sent a message.")
            return redirect('contact_page')
        elif len(phoneNumber) < 7:
            messages.error(request, "Enter a valid phone number")
            return redirect('contact_page')
        elif len(message) <= 0:
            messages.error(request, error_message)
            return redirect('contact_page')
        else:
            contact = ContactMessage.objects.create(
                first_name=firstName, last_name=lastName, email_address=email, phone_number=phoneNumber, message=message)
            contact.save()
            messages.success(request, "Your message was sent successfully!")

        return render(request, "contact.html")
    else:
        return render(request, "contact.html")
