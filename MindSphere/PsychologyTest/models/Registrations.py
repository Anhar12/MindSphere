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
    ParticipantNumber = models.IntegerField()

    def save(self, *args, **kwargs):
        if Registrations.objects.filter(User=self.User, TestSchedule=self.TestSchedule).exists():
            raise ValidationError(f'{self.User.username} participant has already registered for {self.TestSchedule}')

        total_registered = Registrations.objects.filter(TestSchedule=self.TestSchedule).count()
        if total_registered >= self.TestSchedule.Capacity:
            raise ValidationError('Test schedule has reached its maximum capacity.')

        if not self.ParticipantNumber:
            self.ParticipantNumber = total_registered + 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.User.username} - {self.TestSchedule.Name} ({self.Status})'
