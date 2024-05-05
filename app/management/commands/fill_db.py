from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Answer, User, Profile, Tag
from random import choice

class Command(BaseCommand):
    def handle(self, *args, **options):
        newQuestions = [Question(title=f'Question {i}', text=f'text {i}') for i in range (50)]
        Question.objects.bulk_create(newQuestions)
        
        newAnswers = [Answer(text=f'Answer{i}', question=Question.objects.get(pk=i+1), is_correct=choice([True,False]), rating=i) for i in range (50)]
        Answer.objects.bulk_create(newAnswers)

        newUsers = [User(username=f'User{i}', password=f'User{i}') for i in range(50)]
        User.objects.bulk_create(newUsers)

        newProfiles=[Profile(user=User.objects.all()[i], name=f'Profile{i}') for i in range(50)]
        Profile.objects.bulk_create(newProfiles)

        newTags=[Tag(name=f'Tag{i}') for i in range(20)]
        Tag.objects.bulk_create(newTags)

        for i in range(len(Question.objects.all())):
            q=Question.objects.get(pk=i+1)
            newTags=[Tag.objects.get(pk=i%20 + 1), Tag.objects.get(pk=(i+1)%20 + 1), Tag.objects.get(pk=(i+2)%20 + 1)]
            q.tag.add(*newTags)