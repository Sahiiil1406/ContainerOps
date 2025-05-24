from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=150, blank=False)
    
    uid = models.AutoField(primary_key=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class RepoData(models.Model):
    username = models.CharField(max_length=200)
    git_url = models.URLField(blank=False)
    
    def __str__(self):
        return self.username
    
class Deployments(models.Model):
    class StatusChoices(models.TextChoices):
        READY = "ready"
        BUILDING = "building"
        FAILED = "failed"
        DEPLOYED = "deployed"
     
    git_repo = models.ForeignKey(RepoData, on_delete=models.CASCADE)
    branch= models.CharField(max_length=100, default='main')
    deployed_domain = models.URLField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices = StatusChoices.choices,
        default=StatusChoices.BUILDING
    )

    user = models.ForeignKey(User, to_field='username',on_delete=models.CASCADE)
    
    def __str__(self):
        deployment_details=[
            f"Deployment by {self.user.username} | "
            f"Repo: {self.git_repo} | "
            f"Branch: {self.branch} | "
            f"Status: {self.status} | "   
        ]

        if(self.status=="deployed"):
            deployment_details.append(f"Domain: {self.deployed_domain} |")

        return deployment_details








