from django.db import models
from django.utils.timezone import now
from . import Registrations

class Results(models.Model):
    Registration = models.ForeignKey(Registrations, on_delete=models.CASCADE)
    Date = models.DateTimeField(default=now)
    Summary = models.TextField()
    Recommendation = models.TextField(null=True, blank=True)
    ResultNumber = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.ResultNumber:
            test_name = self.Registration.TestSchedule.Name.replace(' ', '-')
            reg_participant_number = self.Registration.ParticipantNumber
            day = self.Date.day
            month = self.Date.month
            year = self.Date.year

            roman_month = self.convert_to_roman(month)

            self.ResultNumber = f"MS/{test_name}/{day}/{roman_month}/{year}/{reg_participant_number}"

        super().save(*args, **kwargs)

    def convert_to_roman(self, number):
        roman_numerals = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
            7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
        }
        return roman_numerals.get(number, '')

    def __str__(self):
        return f'Result for {self.registration}'
