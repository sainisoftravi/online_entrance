import uuid
import datetime
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from .utils import GenerateRandomURL


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    extension = filename.split('.')[-1]
    new_file_name = f'{uuid.uuid4().hex}.{extension}'

    return f'{instance.id}/profile/{new_file_name}'


class CustomUserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field
    """

    def _create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password
        """

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
        """
        Create and save a SuperUser with the given email and password
        """

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

    FullName = models.CharField(
                    max_length=100,
                    null = True,
                    blank = False
                )

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


class Exams(models.Model):
    class Meta:
        verbose_name_plural = "Exams"

    UserID = models.ForeignKey(
            "CustomUser",
            on_delete = models.CASCADE
        )

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    ProgrammeName = models.CharField(
                        null = False,
                        blank = False,
                        max_length = 10
                    )

    CorrectCounter = models.SmallIntegerField(
                        null = False,
                        blank = False,
                        default = 0
                    )

    Slug = models.SlugField(
                        null = False,
                        blank = False,
                        unique = True
                    )

    Date = models.DateField(
                null=False,
                blank=False,
                editable=False,
                default=datetime.date.today
            )

    def save(self, *args, **kwargs):
        self.Slug = GenerateRandomURL('Result')

        super(Exams, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.ID)


class ResultDetails(models.Model):
    class Meta:
        verbose_name_plural = "ResultDetails"

    ResultID = models.ForeignKey(
            "Exams",
            on_delete = models.CASCADE
        )

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    QuestionID = models.ForeignKey(
                    "Questions",
                    on_delete = models.CASCADE
                )

    UserAnswer = models.CharField(
                    null = False,
                    blank = False,
                    max_length = 20
                )


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

    def __str__(self):
        return self.Name


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

    def __str__(self):
        return self.Name


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

    def __str__(self):
        return str(self.ID)


class ReportQuestion(models.Model):
    class Meta:
        verbose_name_plural = 'ReportQuestion'

    UserID = models.ForeignKey(
            "CustomUser",
            on_delete = models.CASCADE
        )

    QuestionID = models.ForeignKey(
                    "Questions",
                    on_delete = models.CASCADE
                )

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    Issue = models.TextField(
                null=False,
                blank=False
            )

    IsMarked = models.BooleanField(
            null=False,
            blank=False,
            default=False
        )

    Date = models.DateField(
                null=False,
                blank=False,
                editable=False,
                default=datetime.date.today
            )


class FeedBack(models.Model):
    class Meta:
        verbose_name_plural = "FeedBack"

    ID = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )

    Name = models.CharField(
            null = False,
            blank = False,
            max_length = 100
        )

    Email = models.EmailField(
            null=False,
            blank=False
        )

    Message = models.TextField(
            null=False,
            blank=False
        )

    IsMarked = models.BooleanField(
            null=False,
            blank=False,
            default=False
        )

    Date = models.DateTimeField(
                null=False,
                blank=False,
                default=now,
                editable=False
            )

    def __str__(self):
        return str(self.ID)


@receiver(pre_save, sender=CustomUser)
def set_default_profile_picture(sender, instance, **kwargs):
    if instance.Gender == 'male' and not instance.ProfileImage:
        instance.ProfileImage = 'pp-male.jpg'
