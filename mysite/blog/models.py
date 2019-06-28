from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
# each blog post is going to connect to a model in our database
class Post(models.Model):

    # when we create a superuser that's going to be someone who can author new post
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now) # IMPORTANT: Here, the DateTimeField default receives the REFERENCE to the function!
                                                              # you shall NOT give the timezone.now(), but timezone.now
    # it can be blank because maybe you don't want to publish it yet
    # null meaning it can be empty
    published_date = models.DateTimeField(blank=True, null=True)
    

    def publish(self):
        # grab our actual published data attribute
        self.published_date = timezone.now()
        self.save()
    '''
    the blog post is being created with the current time but
    the publish date can be blank and it can also be null.
    when you hit publish It's the current time.
    '''

    def approve_comments(self):
        # we will have a list of comments and some will be approved and others will not
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})
        # this is like: go to the 'post_detail' view and inject the content of the post which has the primary key pk

    # title as the string representation of an object (post)
    def __str__(self):
        return self.title()

class Comment(models.Model):
    # to connect each comment to an actual post
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False) #default is that I have not approved the comment yet
                                                          # this approved_comment is used in the function approve_comments, under the filter
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    # since the comments are going to be approved only by super users on the website,
    #when the comment is written and posted, the user will be taken to the page with all
    #post listed.

    def get_absolute_url(self):
        return reverse('post_list')
