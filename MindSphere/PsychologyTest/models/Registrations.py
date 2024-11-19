from django.db import models
from django.core.exceptions import ValidationError
from . import Users, TestSchedules

class Registrations(models.Model):
    STATUS_CHOICES = (
        ('Waiting for Results', 'Waiting for Results'),
        ('Finished', 'Finished'),
    )

    User = models.ForeignKey(Users, limit_choices_to={'role': Users.PARTICIPANT}, on_delete=models.CASCADE)
    TestSchedule = models.ForeignKey(TestSchedules, on_delete=models.CASCADE)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting for Results')
    ParticipantNumber = models.IntegerField(unique=True)

    def clean(self):
        if Registrations.objects.filter(User=self.User, TestSchedule=self.TestSchedule).exists():
            raise ValidationError('This participant has already registered for this test.')

        total_registered = Registrations.objects.filter(TestSchedule=self.TestSchedule).count()
        if total_registered >= self.TestSchedule.Capacity:
            raise ValidationError('Test schedule has reached its maximum capacity.')

    def save(self, *args, **kwargs):
        self.clean()

        if not self.ParticipantNumber:
            total_registered = Registrations.objects.filter(TestSchedule=self.TestSchedule).count() + 1
            if total_registered > self.TestSchedule.Capacity:
                raise ValidationError('Test schedule has reached its maximum capacity.')
            self.ParticipantNumber = total_registered
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.User.username} - {self.TestSchedule.Name} ({self.Status})'
