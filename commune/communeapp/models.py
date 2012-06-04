from django.db import models

# Create your models here.
class Room(models.Model):
	# ...
	def __unicode__(self):
		return self.name + "\t" + self.video
	name = models.CharField(max_length=8)
	chat = models.CharField(max_length=50)
	creation = models.IntegerField()
	video = models.CharField(max_length=80)
	pause_duration = models.IntegerField()
	autoplay = models.BooleanField()
	empty = models.BooleanField()
	total_users = models.IntegerField()
	current_users = models.IntegerField()
