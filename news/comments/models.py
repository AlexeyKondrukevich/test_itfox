from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import User


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class News(models.Model):
    text = models.TextField("Текст новости")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name="Пользователь",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return f"{self.pub_date} {self.author}"

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} {self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)
