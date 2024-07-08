from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Poll(models.Model):
    # every poll has a title
    title = models.CharField(max_length=200)
    # every poll should have its own url name, called a slug
    slug = models.SlugField(max_length=200)
    # what is the poll asking?
    question = models.TextField(blank=True, null=True)
    # count the total number of votes in the poll
    total_vote = models.IntegerField(default=0)
    # recall all voters of a poll
    voters = models.ManyToManyField(User, blank=True)
    # attribute a single User as the owner of a poll
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_polls")

    def __str__(self):
        return self.title
    
    # the slug needs to be automatically filled when the User creates a new poll
    def save(self, *args, **kwargs):
        # the User won't get a chance to fill in the slug
        if not self.slug:
            # we'll make the slug from the title
            self.slug = slugify(self.title)
            original_slug = self.slug
            num = 1
            # just in case a previous poll exists with the same name
            # we're gonna at least need a different slug since it's a url
            while Poll.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1
        # call the original save function with its unknown arguments
        super(Poll, self).save(*args, **kwargs)
    
class Option(models.Model):
    # every poll option has a "name"
    name = models.CharField(max_length=200)
    # count how many people voted for the option
    total_vote = models.IntegerField(default=0)
    # connect the option to a single poll
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    # recall who voted for this option
    voters = models.ManyToManyField(User, blank=True)

    # calculate what percent of votes goes to this option
    @property
    def percent_vote(self):
        poll_votes = self.poll.total_vote
        option_votes = self.total_vote

        if poll_votes == 0:
            percent_vote = 0
        else:
            percent_vote = (option_votes / poll_votes) * 100
        return percent_vote
    
    def __str__(self):
        return self.title
    
