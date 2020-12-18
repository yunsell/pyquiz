from django.db import models

class Question(models.Model):
    subject = models.CharField(max_length=200) #제한된 텍스트는 CharField 를 사용
    content = models.TextField() #무제한 텍스트
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #question과 연결된 answer도 삭제
    content = models.TextField()
    create_date = models.DateTimeField()