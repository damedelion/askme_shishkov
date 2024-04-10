from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Answer

class Command(BaseCommand):
    def handle(self, *args, **options):
        newQuestions = [Question(title=f'Question {i}', text=f'text {i}') for i in range (50)]
        Question.objects.bulk_create(newQuestions)
        newAnswers = [Answer(text=f'Answer{i}', rating=i) for i in range (50)]
        Answer.objects.bulk_create(newAnswers)