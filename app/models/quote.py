from tortoise import fields, models


class Quote(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField(null=False)
    author = fields.CharField(max_length=100, null=False)

    class Meta:
        table = "quotes"

    def __str__(self):
        return f"{self.content} - {self.author}"
