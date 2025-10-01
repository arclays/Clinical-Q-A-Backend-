# models.py
from django.db import models

class DS_Questions(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('disabled', 'Disabled'),
    ]
    
    question = models.TextField()
    disease = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.disease or 'General'}: {self.question[:40]}..."


class DS_Answers(models.Model):
    question = models.ForeignKey(DS_Questions, on_delete=models.CASCADE)
    answer = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Answer to: {self.question}"
        
class DS_Views(models.Model):
    question = models.ForeignKey(DS_Questions, on_delete=models.CASCADE)
    number_of_clicks = models.PositiveIntegerField(default=0)
    date_asked = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.number_of_clicks} Views for {self.question}: "


    
class CustomQuestion(models.Model):
    question_text = models.TextField()
    requestors_contact = models.CharField(max_length=255)
    date_of_request = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"Q#{self.id}: {self.question_text[:40]}... (answered: {self.is_answered})"
