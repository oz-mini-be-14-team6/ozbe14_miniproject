from tortoise import fields, models


class Bookmark(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="bookmarks", on_delete=fields.OnDelete.CASCADE
    )
    quote = fields.ForeignKeyField(
        "models.Quote", related_name="bookmarks", on_delete=fields.OnDelete.CASCADE
    )

    class Meta:
        table = "bookmarks"

    def __str__(self):
        return f"{self.user.username} → {self.quote.id}"
