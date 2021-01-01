from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제
    subject = models.CharField(max_length=200) #제한된 텍스트는 CharField 를 사용
    content = models.TextField() #무제한 텍스트
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #question과 연결된 answer도 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)