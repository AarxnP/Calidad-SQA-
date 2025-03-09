from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    pokemon_id = models.IntegerField(unique=True)  # ID único del Pokémon
    image = models.URLField()
    type = models.CharField(max_length=255)
    weight = models.FloatField()
    height = models.FloatField()
    move = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name