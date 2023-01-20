from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import date
from django.urls import reverse


class BlogManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BlogManager()
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['date_of_birth']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Profile(models.Model):
    sex = (
        ("Male","Male"),
        ("Female","Female")
    )
    User = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Profile_pic = models.FileField("Profile Pic",upload_to='uploads/',default='uploads/default.png',validators=[FileExtensionValidator(allowed_extensions=['jpg','png'],message='Please Upload The Fellowing Image Format jpg ord png')])
    bio = models.TextField(verbose_name='bio',max_length=255,blank=True,null=True)
    Gender = models.CharField(max_length=10,choices=sex,blank=True,null=True)

    def __str__(self) -> str:
        return self.User.email

class Article_Category(models.Model):
    Title = models.CharField(max_length=255,unique=True)

    def __str__(self) -> str:
        return self.Title
   
class Article(models.Model):
    headlines = models.CharField(max_length=255)
    body = models.TextField(max_length=255)
    Article_pic = models.FileField("Article Pic",upload_to='Articles/',validators=[FileExtensionValidator(allowed_extensions=['jpg','png'],message='Please Upload The Fellowing Image Format jpg ord png')],serialize=True)
    Category = models.ForeignKey(Article_Category,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.headlines
    
    class Meta:
       ordering = ['pub_date']
    

    def get_absolute_url(self):
        return reverse('blog:details', kwargs={'pk' : self.pk})

    

class Comment(models.Model):
    comments = models.CharField(max_length=255)
    Article = models.ForeignKey(Article,on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.comments
    class Meta:
       get_latest_by = ['comment_date']