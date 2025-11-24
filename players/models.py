from django.db import models

# Create your models here.

class Player(models.Model):
    nickname = models.CharField(
        max_length=50,
        unique=True,
    )
    country = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nickname
    
    class Meta:
        ordering = ['-rating' , 'nickname']
        verbose_name = "Player"
        verbose_name_plural = 'Players'