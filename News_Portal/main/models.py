from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# from django.core.validators import MinValueValidator
from django.urls import reverse

# импортируем «ленивый» геттекст с подсказкой
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
 


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)
        
    def update_rating(self):

        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(Sum('post_rating'))['post_rating__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']
        rating_of_comments_under_posts_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']
            
        self.user_rating = rating_of_posts_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_of_author
        self.save()
        return self.user_rating


class Category(models.Model):

    # добавим переводящийся текст подсказку к полю
    # name = models.CharField(max_length=100, help_text=_('category name'))
    
    sport = "ST"
    education = "ED"
    music = "MS"
    nature = "NT"

    CATEGORIES = [
        (sport, 'Спорт'),
        (education, 'Образование'),
        (music, 'Музыка'),
        (nature, 'Природа')
] 
    category_name = models.CharField(max_length=2, unique=True, choices=CATEGORIES, default="ED", help_text=_('category name'))
    
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')

    def __str__(self):
        return self.get_category_name_display()


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )


class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    article = "AC"
    news = "NS"

    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=article)
    time_in = models.DateTimeField(auto_now_add = True)

    title = models.CharField(max_length=255)
    content = models.TextField()
    post_rating = models.FloatField(default=0.0)

    category = models.ManyToManyField(Category, through = 'PostCategory', related_name='news')


    def like(self):
        self.post_rating  += 1
        self.save()

    def dislike(self):
        self.post_rating  -= 1
        self.save()

    def preview(self):
        return f'{self.content[0:124]}...'

    def __str__(self):
        return f'{self.title.title()}: "{self.content[:20]}..." { self.time_in: %d %m %y}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField(blank=True)

    comment_time_in = models.DateTimeField(auto_now_add = True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating  += 1
        self.save()

    def dislike(self):
        self.comment_rating  -= 1
        self.save()