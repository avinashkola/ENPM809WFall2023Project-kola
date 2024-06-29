from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class Chore(models.Model):
    chore = models.CharField(max_length=30)
    assigned_date = models.DateTimeField('date added')
    due_date = models.DateTimeField('due date')
    chore_assigner = models.CharField(max_length=30)
    assign_chore_to = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    chore_done_by = models.CharField(max_length=30, blank=True)
    chore_done_date = models.DateTimeField('done date', blank=True, null=True)
    chore_priority = models.CharField(max_length=30, blank=True)  # Added blank=True

    def __str__(self):
        return '{} by {}'.format(self.chore, self.assign_chore_to)

    def is_expired(self):
        return not self.chore_done_by and self.due_date < timezone.now()

    def calculate_priority(self):
        assigned_date = timezone.now()
        days_until_due = (self.due_date - assigned_date).days

        if days_until_due <= 2:
            return 'Urgent'
        elif days_until_due <= 4:
            return 'Required'
        else:
            return 'Low'

    def save(self, *args, **kwargs):
        self.chore_priority = self.calculate_priority()
        super(Chore, self).save(*args, **kwargs)
