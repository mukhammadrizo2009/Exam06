from django.db import models

# Create your models here.

from games.models import Game
from players.models import Player

class Score(models.Model):
    
    RESULT_CHOICES = [
        ('win' , 'Win'),
        ('draw' , 'Draw'),
        ('lose' , 'Lose'),
    ]
    
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name='scores'
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='scores'
    )
    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES
    )
    points = models.IntegerField()
    opponent_name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.nickname} - {self.result} ({self.game.title})"
    
    def save(self, a , b ):
        if not self.pk:
            self.points = self.player.rating
            
            if self.result == 'win':
                self.player.rating += 10
            elif self.result == 'draw':
                self.player.rating += 5
            elif self.result == 'lose':
                self.player.rating += 0
                
            self.player.save()
            
        super().save(a , b)
        
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Score"
        verbose_name_plural = "Scores"