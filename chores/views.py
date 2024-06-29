import logging
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Chore
from .forms import CreateChoreForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

# Define a logger
logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'chores/index.html'

    def get_queryset(self):
        return Chore.objects.order_by('due_date')

@login_required(login_url='user_management:login')
@ensure_csrf_cookie
def complete_chore(request, chore_id):
    try:
        chore = Chore.objects.get(pk=chore_id)
    except Chore.DoesNotExist:
        logger.error(f"Chore with ID {chore_id} does not exist.")
        return HttpResponseRedirect(reverse('chores:index'))

    try:
        if chore.chore_done_by or not request.user.is_authenticated or chore.is_expired():
            return HttpResponseRedirect(reverse('chores:index'))

        chore.chore_done_by = request.user.username
        chore.chore_done_date = timezone.now()
        chore.save()

        return HttpResponseRedirect(reverse('chores:index'))

    except Exception as e:
        logger.exception(f"Error completing chore with ID {chore_id}: {e}")
        return HttpResponseRedirect(reverse('chores:index'))

@login_required(login_url='user_management:login')
@ensure_csrf_cookie
def delete_chore(request, chore_id):
    try:
        chore = get_object_or_404(Chore, pk=chore_id)

        if not request.user.is_authenticated or \
                (not request.user.is_superuser and chore.chore_assigner != request.user.username):
            return HttpResponseRedirect(reverse('chores:index'))

        chore.delete()

        return HttpResponseRedirect(reverse('chores:index'))

    except Exception as e:
        logger.exception(f"Error deleting chore with ID {chore_id}: {e}")
        return HttpResponseRedirect(reverse('chores:index'))

@login_required(login_url='user_management:login')
@ensure_csrf_cookie
def create_chore(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('chores:index'))

        if request.method == 'POST':
            form = CreateChoreForm(request.POST)
            if form.is_valid():
                chore_text = form.cleaned_data['chore']
                due_date = form.cleaned_data['due_date']
                assign_chore_to = form.cleaned_data['assign_chore_to']
                send_notification = form.cleaned_data.get('send_notification', False)

                chore = Chore(
                    chore=chore_text,
                    assigned_date=timezone.now(),
                    due_date=due_date,
                    chore_assigner=request.user.username,
                    assign_chore_to=assign_chore_to,
                )
                chore.save()

                if send_notification:
                    email_subject = "Household Chores Distributor"
                    email_message = (
                        f'You have a new chore assignment\n\n'
                        f'Chore: {chore.chore}\n'
                        f'Due Date: {chore.due_date}\n'
                        f'Assigned By: {chore.chore_assigner}'
                    )
                    sender_email = 'securecoding9@gmail.com'
                    recipient_email = assign_chore_to.email

                    send_mail(email_subject, email_message, sender_email, [recipient_email])

                return HttpResponseRedirect(reverse('chores:index'))

        form = CreateChoreForm()
        return render(request, 'chores/create_chore.html', {'form': form})

    except Exception as e:
        logger.exception(f"Error creating chore: {e}")
        return HttpResponseRedirect(reverse('chores:index'))
