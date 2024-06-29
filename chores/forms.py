from django import forms
from django.contrib.auth.models import User 

class CreateChoreForm(forms.Form):
    chore = forms.CharField(max_length=200)
    due_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    assign_chore_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Assign Chore To",
        empty_label="Select a user",
    )  
    send_notification = forms.BooleanField(label='Send Notification', required=False)



