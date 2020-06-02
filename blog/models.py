from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('auth.user',on_delete = models.CASCADE, null = True, blank=True)
    category = models.ForeignKey(Category,on_delete = models.CASCADE, null = True, blank=True)
    title = models.CharField(max_length=100) 
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    picture = models.FileField(upload_to="media/", null=True,blank=True)
    likes = models.ManyToManyField('auth.user',blank=True, related_name ='Post_likes')
    sads = models.ManyToManyField('auth.user',blank=True, null=True ,related_name ='Post_sads')
    hearts = models.ManyToManyField('auth.user',blank=True, null=True, related_name ='Post_hearts')
    
class Comment(models.Model):
    post = models.ForeignKey('post',on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    # class Meta:
    #     model = Comment
    #     fields = ('id', 'post', 'user', 'body', 'date_created')

    
