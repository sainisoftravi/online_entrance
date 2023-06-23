import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.id}/profile/{filename}'


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_('email address'), unique=True)
    Gender = models.CharField(
                max_length=6,
                null = True,
                blank = False
            )

    DOB = models.DateField(
                null=True,
                blank=True
            )

    ProfileImage = models.ImageField(
                blank=True,
                null=True,
                default='pp-female.jpg',
                upload_to=user_directory_path
            )

    MemberSince = models.DateTimeField(
                null=False,
                blank=False,
                default=now,
                editable=False,
            )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Programme(models.Model):
    class Meta:
        verbose_name_plural = "Programme"

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    Name = models.CharField(
            null = False,
            blank = False,
            max_length = 10
        )


class Subject(models.Model):
    class Meta:
        verbose_name_plural = "Subject"

    ProgrammeID = models.ForeignKey(
            "Programme",
            on_delete = models.CASCADE
        )

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    Name = models.CharField(
            null = False,
            blank = False,
            max_length = 50
        )

    TotalQuestionsToSelect = models.SmallIntegerField(
            null = False,
            blank = False,
            default=1
        )


class Questions(models.Model):
    class Meta:
        verbose_name_plural = "Questions"

    SubjectID = models.ForeignKey(
            'Subject',
            on_delete = models.CASCADE
        )

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    Title = models.TextField(
                null = False,
                blank = False
        )

    Answer = models.CharField(
                null = False,
                blank = False,
                max_length = 20
        )

    OptionOne = models.CharField(
                    null = False,
                    blank = False,
                    max_length = 20
        )

    OptionTwo = models.CharField(
                    null = False,
                    blank = False,
                    max_length = 20
        )

    OptionThree = models.CharField(
                    null = False,
                    blank = False,
                    max_length = 20
        )

    OptionFour = models.CharField(
                    null = False,
                    blank = False,
                    max_length = 20
        )
