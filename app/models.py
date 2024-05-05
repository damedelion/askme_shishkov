from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by("-created_at")
    
class AnswerManager(models.Manager):
    def get_best(self):
        return self.order_by("-rating")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(null=True,max_length=255)
    text = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    objects = QuestionManager()

class Answer(models.Model):
    text = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT)
    rating = models.IntegerField(null=True)
    is_correct = models.BooleanField(null=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    objects = AnswerManager()


class QuestionLike(models.Model):
    is_liked = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    #class Meta:
    #    unique_together = ('question', 'user')

class AnswerLike(models.Model):
    is_liked = models.BooleanField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

