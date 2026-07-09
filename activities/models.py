from django.db import models
import os
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, unique=True)
    faculty_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100, default="IT")

    class Meta:
        ordering = ['faculty_name']

    def __str__(self):
        return f"{self.faculty_name} ({self.faculty_id})"


class Activity(models.Model):
    activity_name = models.CharField(max_length=300, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['activity_name']

    def __str__(self):
        return self.activity_name


class Submission(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE
    )

    activity_date = models.DateField()

    description = models.TextField()

    entry_datetime = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.activity} - {self.activity_date}"


class SubmissionFaculty(models.Model):

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="faculty_members"
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="activity_submissions"
    )


def attachment_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{extension}"
    return os.path.join("uploads", unique_name)


class Attachment(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="attachments"
    )

    uploaded_file = models.FileField(
        upload_to=attachment_upload_path
    )

    original_filename = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename

class ReportDownload(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    month = models.DateField()

    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"