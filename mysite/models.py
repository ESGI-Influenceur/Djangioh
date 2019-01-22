from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Card(models.Model):
    name = models.CharField(max_length=200,unique=True)
    image = models.TextField()
    description = models.TextField()
    cardLevel = models.IntegerField()
    attaque = models.IntegerField()
    defense = models.IntegerField()
    numero = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=200)

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.title

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

class Forum(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title

    def num_posts(self):
        return sum([t.num_posts() for t in self.topic_set.all()])

    def last_post(self):
        if self.topic_set.count():
            last = None
            for t in self.topic_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.created > last.created: last = l
            return last

class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return max(0, self.post_set.count() - 1)

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    body = models.TextField(max_length=255)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.topic, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True

class ProfaneWord(models.Model):
    word = models.CharField(max_length=60)

    def __unicode__(self):
        return self.word
