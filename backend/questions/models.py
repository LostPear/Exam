from django.db import models

class Question(models.Model):
    TYPE_CHOICES = [
        ('single', '单选题'),
        ('judge', '判断题'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    question = models.TextField()
    options = models.JSONField(default=list)
    correct_answer = models.IntegerField()
    explanation = models.TextField(blank=True, default='')
    image = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f"[{self.type}] {self.question[:40]}"
