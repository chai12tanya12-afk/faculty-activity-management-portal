from django.contrib import admin

from .models import *

admin.site.register(Faculty)

admin.site.register(Activity)

admin.site.register(Submission)

admin.site.register(SubmissionFaculty)

admin.site.register(Attachment)

admin.site.register(ReportDownload)