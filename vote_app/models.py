from django.db import models

# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length= 200)

    def __str__(self):
        return self.name

class Poll_Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.text