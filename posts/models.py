from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length=250)
	date = models.DateField(auto_now_add=True)
	content = models.TextField()
	user = models.ForeignKey(User)
	coments_permission = models.BooleanField(default = True)

	  
class Coment(models.Model):
	content = models.TextField()
	post = models.ForeignKey(Post)
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User)
	
# Create your models here.