from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)

    class Meta:
        table = "users"  # ✅ 테이블 이름을 명시하는 게 안전함


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


class Quote(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField(null=False)
    author = fields.CharField(max_length=100, null=False)

    class Meta:
        table = "quotes"


class Bookmarks(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="bookmarks", on_delete=fields.OnDelete.CASCADE
    )
    quote = fields.ForeignKeyField(
        "models.Quote", related_name="bookmarks", on_delete=fields.OnDelete.CASCADE
    )

    class Meta:
        table = "bookmarks"


class BlacklistedToken(models.Model):
    id = fields.IntField(pk=True)
    token = fields.TextField(unique=True)  # JWT 문자열
    blacklisted_at = fields.DatetimeField(auto_now_add=True)  # 블랙리스트 등록 시각

    def __str__(self):
        return f"BlacklistedToken(id={self.id}, token={self.token[:15]}...)"
