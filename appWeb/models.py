from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='fotoPerfil', default='escom.png')

	def __str__(self):
		return f'Perfil de {self.user.username}'

	def likes(self):
		post_ids = Like.objects.filter(user_id=self.user).values_list('post_id', flat=True)
		return post_ids

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
								.values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
								.values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.TextField()
	likes = models.PositiveIntegerField(default=0)
	user_likes = models.ManyToManyField(User, related_name='postUser')
	user_comments = models.ManyToManyField(User, related_name='postComment')

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f'{self.user.username}: {self.content}'

	def comments(self, post_id):
		comments = Comment.objects.filter(post_id=post_id)
		return comments

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentUser')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentPost')
	content = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"{self.user} comment {self.post}"

class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'

	class Meta:
		indexes = [
		models.Index(fields=['from_user', 'to_user']),
		]


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likeUsers")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likePosts")
	alreadyLiked = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user} liked {self.post}"
	
	class Meta:
		indexes = [
		models.Index(fields=['user', 'post']),
		]
