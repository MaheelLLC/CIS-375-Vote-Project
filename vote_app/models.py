from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length= 200)
    user = models.CharField(max_length= 200, default="")
    slug = models.SlugField(max_length=200)
    voters = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            
            num = 1
            
            while Poll.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1
        super(Poll, self).save(*args, **kwargs)

class Poll_Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.text