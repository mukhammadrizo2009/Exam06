from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Game"
        verbose_name_plural = "Games"