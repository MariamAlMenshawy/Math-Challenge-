from django.db import models
from django.conf import settings
# Create your models here.

class Session(models.Model):
    LEVEL_CHOICES = [
        ('easy',   'Easy'),
        ('medium', 'Medium'),
        ('hard',   'Hard'),
    ]
    LEVEL_TIME = {
        'easy':   50,
        'medium': 100,
        'hard':   180,
    }
    SESSION_SCORE = {
        'easy':   5,
        'medium': 10,
        'hard':   15,
    }
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    level = models.CharField(max_length=15,choices=LEVEL_CHOICES)
    time = models.IntegerField()
    
    total_score = models.IntegerField(default=0)
    user_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)  

    def save(self, *args, **kwargs):

        self.time = self.LEVEL_TIME[self.level]
        self.total_score = self.SESSION_SCORE[self.level]
        
        super().save(*args, **kwargs)

    def complete_session(self):
        if not self.is_completed:
            correct_count = self.question_set.filter(is_correct=True).count()
            
            score_per_question = self.total_score / 5
            self.user_score = correct_count * score_per_question
            
            self.is_completed = True
            self.save()

            self.user_id.points += self.user_score
            self.user_id.save()

    def __str__(self):
        return self.level
    


class Question(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    equation = models.CharField(max_length=250)
    correct_answer = models.FloatField(null=True, blank=True)
    user_answer = models.FloatField(null=True, blank=True)
    is_correct = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):

        if self.user_answer is not None :
            self.is_correct = round(self.correct_answer, 2) == round(self.user_answer, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.equation

