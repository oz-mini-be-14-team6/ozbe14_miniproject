from tortoise import fields
from tortoise.models import Model

class Question(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()

    class Meta:
        table = "questions"
