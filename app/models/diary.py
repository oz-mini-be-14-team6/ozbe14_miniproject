from tortoise import fields, models


class Diary(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="diaries", on_delete=fields.OnDelete.CASCADE
    )
    diary_title = fields.CharField(max_length=100, null=False)
    diary_content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "diaries"

    def __str__(self):
        return f"{self.diary_title} ({self.user.username})"
