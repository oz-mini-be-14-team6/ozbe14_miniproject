from tortoise import fields, models


class BlacklistedToken(models.Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=512, unique=True)
    blacklisted_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "blacklisted_tokens"

    def __str__(self):
        return f"BlacklistedToken(id={self.id}, token={self.token[:15]}...)"
