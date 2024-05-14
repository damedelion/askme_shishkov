from django.core.management.base import BaseCommand, CommandError
from app.models import *
from random import choice, randint, sample

""" ratio = 100

users_count = ratio
questions_count = 10 * ratio
answers_count = 100 * ratio
tags_count = ratio
likes_count = 200 * ratio """

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)
        
    def handle(self, *args, **options):
        ratio = options["ratio"]
        users_count = ratio
        questions_count = 10 * ratio
        answers_count = 100 * ratio
        tags_count = ratio
        likes_count = 200 * ratio

        newUsers = []
        for i in range(1, users_count + 1):
            newUsers.append(User(username=f'User {i}', password=f'User {i}'))
            if i % 100000 == 0:
                User.objects.bulk_create(newUsers)
                newUsers=[]
        if len(newUsers) > 0:        
            User.objects.bulk_create(newUsers)

        newProfiles=[]
        for i in range(1, users_count + 1):
            newProfiles.append(Profile(user=User.objects.get(pk=i), name=f'Profile {i}'))
            if i % 100000 == 0:
                Profile.objects.bulk_create(newProfiles)
                newProfiles=[]
        if len(newProfiles) > 0:
            Profile.objects.bulk_create(newProfiles)


        newQuestions = []
        for i in range (1, questions_count + 1):
            newQuestions.append(Question(title=f'Question {i}', text=f'text {i}', author=Profile.objects.get(pk=randint(1, users_count))))
            if i % 100000 == 0:
                Question.objects.bulk_create(newQuestions)
                newQuestions=[]
        if len(newQuestions) > 0:
            Question.objects.bulk_create(newQuestions)
        

        newAnswers = []
        for i in range (1, answers_count + 1):
            newAnswers.append(Answer(text=f'Answer {i}', author=Profile.objects.get(pk=randint(1, users_count)), question=Question.objects.get(pk=randint(1, questions_count)), is_correct=choice([True,False])))
            if i % 100000 == 0:
                Answer.objects.bulk_create(newAnswers)
                newAnswers=[]
        if len(newAnswers) > 0:
            Answer.objects.bulk_create(newAnswers)


        newTags=[]
        for i in range(1, tags_count + 1):
            newTags.append(Tag(name=f'tag{i}'))
            if i % 100000 == 0:
                Tag.objects.bulk_create(newTags)
                newTags=[]
        if len(newTags) > 0:
            Tag.objects.bulk_create(newTags)


        """ for i in range(len(Question.objects.all())):
            q=Question.objects.get(pk=i+1)
            newTags=[Tag.objects.get(pk=i%ratio + 1), Tag.objects.get(pk=(i+1)%ratio + 1), Tag.objects.get(pk=(i+2)%ratio + 1)]
            q.tag.add(*newTags) """

        for i in range(1, questions_count + 1):
            q=Question.objects.get(pk=i)
            newTags=[]
            while(len(newTags) < 3):
                t=Tag.objects.get(pk=randint(1, tags_count))
                if (t not in Tag.objects.filter(question=q)):
                    newTags.append(t)

            q.tag.add(*newTags)


        """ newQuestionLikes=[]
        for i in range(200 * ratio):
            q=choice(Question.objects.all())
            u=choice(Profile.objects.all())
            if (len(QuestionLike.objects.filter(question=q,user=u)) == 0):
                q.likes_count = q.likes_count + 1
            q_like=QuestionLike(is_liked=True, question=q, user=u)
            newQuestionLikes.append(q_like)
        QuestionLike.objects.bulk_create(newQuestionLikes) """

        """ for i in range(likes_count):
            if (i % (likes_count / 10) == 0):
                print(f'questionlike {i}')
            q=Question.objects.get(pk=randint(1, questions_count))
            u=Profile.objects.get(pk=randint(1, users_count))
            while (len(QuestionLike.objects.filter(question=q,user=u)) != 0):
                q=Question.objects.get(pk=randint(1, questions_count))
                u=Profile.objects.get(pk=randint(1, users_count))
            q.likes_count = q.likes_count + 1
            q_like=QuestionLike(is_liked=True, question=q, user=u)
            q.save()
            q_like.save() """
        

        """ for i in range(likes_count):
            if (i % (likes_count / 10) == 0):
                print(f'answerlike {i}')
            a=Answer.objects.get(pk=randint(1, answers_count))
            u=Profile.objects.get(pk=randint(1, users_count))
            while (len(AnswerLike.objects.filter(answer=a,user=u)) != 0):
                a=Answer.objects.get(pk=randint(1, answers_count))
                u=Profile.objects.get(pk=randint(1, users_count))
            a.likes_count = a.likes_count + 1
            a_like=AnswerLike(is_liked=True, answer=a, user=u)
            a.save()
            a_like.save() """


        if (questions_count < 100000):
            likes_per_user=questions_count
        else:
            likes_per_user=100000

        cur_likes_count=0
        user_id=1
        while (cur_likes_count < likes_count and user_id <= users_count):
            print(f'question_like: {cur_likes_count} / {likes_count}')
            newQuestionLikes=[]
            u=Profile.objects.get(pk=user_id)
            count=randint(1, likes_per_user)
            q_id_list=sample(range(1, questions_count + 1), count)
            for id in q_id_list:
                q=Question.objects.get(pk=id)
                newQuestionLikes.append(QuestionLike(is_liked=True, question=q, user=u))
                q.likes_count = q.likes_count + 1
                q.save()
            QuestionLike.objects.bulk_create(newQuestionLikes)
            cur_likes_count=cur_likes_count+count
            user_id=user_id+1

        cur_likes_count=0
        user_id=1
        while (cur_likes_count < likes_count and user_id <= users_count):
            print(f'answer_like: {cur_likes_count} / {likes_count}')
            newAnswerLikes=[]
            u=Profile.objects.get(pk=user_id)
            count=randint(1, likes_per_user)
            a_id_list=sample(range(1, answers_count + 1), count)
            for id in a_id_list:
                a=Answer.objects.get(pk=id)
                newAnswerLikes.append(AnswerLike(is_liked=True, answer=a, user=u))
                a.likes_count = a.likes_count + 1
                a.save()
            AnswerLike.objects.bulk_create(newAnswerLikes)
            cur_likes_count=cur_likes_count+count
            user_id=user_id+1