from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)

    class Meta:
        table = "users"  #  테이블 이름을 명시하는 게 안전함

    def __str__(self):
        return self.username
