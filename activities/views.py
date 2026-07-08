from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.db.models.functions import TruncMonth
from reportlab.lib.pagesizes import A4
from datetime import date
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import black
from django.http import HttpResponse
import datetime
from django.db.models import Count
from django.http import JsonResponse
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from .models import Attachment
from django.views.decorators.http import require_POST
from itertools import groupby
import random
from .models import (
    Faculty,
    Activity,
    Submission,
    SubmissionFaculty,
    Attachment
)
from .models import ReportDownload
from .forms import SubmissionForm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.conf import settings
import os
import datetime
from django.db.models.functions import TruncMonth
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.http import JsonResponse
from django.http import FileResponse, Http404
import os

def register_view(request):

    # Allow registration only once
    if User.objects.exists():
        return redirect("login")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:

            return render(request,
                "activities/register.html",
                {
                    "error":"Passwords do not match."
                })

        User.objects.create_user(

            username=username,

            password=password

        )

        return redirect("login")

    return render(request,"activities/register.html")

def login_view(request):

    if not User.objects.exists():

        return redirect("register")

    if request.method=="POST":

        username=request.POST["username"]

        password=request.POST["password"]

        user=authenticate(

            request,

            username=username,

            password=password

        )

        if user:

            login(request,user)

            return redirect("home")

        return render(

            request,

            "activities/login.html",

            {

                "error":"Invalid Username or Password"

            }

        )

    return render(request,"activities/login.html")

def logout_view(request):

    logout(request)

    return redirect("login")

@login_required(login_url="login")
def home(request):

    return render(

        request,

        "activities/home.html"

    )

@login_required
def faculty_form_partial(request):

    form = SubmissionForm()

    return render(

        request,

        "activities/partials/faculty_form.html",

        {

            "form": form,

            "faculty": Faculty.objects.all(),

            "activity": Activity.objects.all()

        }

    )

def generate_faculty_id():

    while True:

        faculty_id = str(random.randint(12001, 12999))

        if not Faculty.objects.filter(faculty_id=faculty_id).exists():

            return faculty_id

@login_required
def monthly_report_partial(request):

    months = (
        Submission.objects.filter(user=request.user)

        .annotate(month=TruncMonth("activity_date"))

        .values_list("month", flat=True)

        .distinct()

        .order_by("-month")

    )

    return render(

        request,

        "activities/partials/monthly_report.html",

        {

            "months": months

        }

    )

@login_required
def show_activities_partial(request):

    months = (
        Submission.objects.filter(user=request.user)

        .annotate(month=TruncMonth("activity_date"))

        .values_list("month", flat=True)

        .distinct()

        .order_by("-month")

    )

    return render(

        request,

        "activities/partials/show_activities.html",

        {

            "months": months

        }

    )

@login_required
def faculty_form(request):

    form = SubmissionForm()

    context = {
        "form": form,
        "faculty": Faculty.objects.all(),
        "activity": Activity.objects.all(),
    }

    return render(request, "activities/form.html", context)


@login_required
@transaction.atomic
def submit_form(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid request."
            },
            status=400
        )

    # -------------------------------
    # Get Form Data
    # -------------------------------

    faculty_ids = request.POST.getlist("faculty")
    activity_id = request.POST.get("activity")
    activity_date = request.POST.get("activity_date")
    description = request.POST.get("description", "").strip()
    files = request.FILES.getlist("attachments")

    # -------------------------------
    # Validation
    # -------------------------------

    if not faculty_ids:
        return JsonResponse(
            {
                "status": "error",
                "message": "Please select at least one faculty."
            },
            status=400
        )

    if not activity_id:
        return JsonResponse(
            {
                "status": "error",
                "message": "Please select an activity."
            },
            status=400
        )

    if not activity_date:
        return JsonResponse(
            {
                "status": "error",
                "message": "Please select the activity date."
            },
            status=400
        )

    if not description:
        return JsonResponse(
            {
                "status": "error",
                "message": "Description cannot be empty."
            },
            status=400
        )

    if not files:
        return JsonResponse(
            {
                "status": "error",
                "message": "Please upload at least one PDF."
            },
            status=400
        )

    # -------------------------------
    # Activity
    # -------------------------------

    activity = get_object_or_404(
        Activity,
        id=activity_id
    )

    # -------------------------------
    # Create Submission
    # -------------------------------

    submission = Submission.objects.create(
        user=request.user,
        activity=activity,
        activity_date=activity_date,
        description=description
    )

    # -------------------------------
    # Save Faculty Mapping
    # -------------------------------

    faculties = Faculty.objects.filter(id__in=faculty_ids)

    SubmissionFaculty.objects.bulk_create([
        SubmissionFaculty(
            submission=submission,
            faculty=faculty
        )
        for faculty in faculties
    ])

    # -------------------------------
    # Save Attachments
    # -------------------------------

    MAX_FILE_SIZE = 10 * 1024 * 1024      # 10 MB

    for file in files:

        if (
            not file.name.lower().endswith(".pdf")
            or file.content_type != "application/pdf"
        ):
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"{file.name} is not a valid PDF."
                },
                status=400
            )

        if file.size > MAX_FILE_SIZE:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"{file.name} exceeds the 10 MB size limit."
                },
                status=400
            )

        Attachment.objects.create(
            submission=submission,
            uploaded_file=file,
            original_filename=file.name
        )

    # -------------------------------
    # Success
    # -------------------------------

    return JsonResponse({
        "status": "success",
        "message": "Form submitted successfully.",
        "submitted_at": timezone.localtime(
            submission.entry_datetime
        ).strftime("%d-%m-%Y %I:%M:%S %p")
    })

@login_required
def monthly_report(request):

    months = (
        Submission.objects.filter(user=request.user)
        .annotate(month=TruncMonth("activity_date"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("-month")
    )

    return render(
        request,
        "activities/monthly_report.html",
        {
            "months": months
        }
    )

@login_required
def download_report(request):

    month = request.POST.get("month")

    if not month:
        return HttpResponse("Month not selected.", status=400)

    year = int(month.split("-")[0])
    month_number = int(month.split("-")[1])

    submissions = Submission.objects.filter(
        user=request.user,
        activity_date__year=year,
        activity_date__month=month_number
    ).prefetch_related(
        "faculty_members__faculty"
    ).select_related(
        "activity"
    ).order_by(
        "activity__activity_name",
        "activity_date"
    )

    if not submissions.exists():
        return JsonResponse({
            "message": "No forms are submitted for the selected month."
        }, status=404)
    
    ReportDownload.objects.create(
        user=request.user,
        month=date(year, month_number, 1)
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Monthly_Report_{month}.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # ------------------------------------------------
    # LOGO
    # ------------------------------------------------

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "logo.png"
    )

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=4.8 * inch,
            height=0.95 * inch
        )
        logo.hAlign = "CENTER"
        elements.append(logo)

    elements.append(Spacer(1, 12))

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    title = styles["Title"]
    title.alignment = TA_CENTER

    title1 = styles["Heading2"]
    title1.alignment = TA_CENTER

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    elements.append(
        Paragraph(
            "<b>Faculty Monthly Activities Report</b>",
            title
        )
    )

    elements.append(
        Paragraph(
            "<b>Department of Information Technology</b>",
            title1
        )
    )

    elements.append(
        Paragraph(
            f"<b>Month :</b> {datetime.date(year, month_number, 1).strftime('%B %Y')}",
            heading
        )
    )

    elements.append(Spacer(1, 20))

    # ------------------------------------------------
    # EMPTY REPORT
    # ------------------------------------------------

    # ------------------------------------------------
    # TABLE
    # ------------------------------------------------

    for activity, records in groupby(
        submissions,
        key=lambda x: x.activity.activity_name
    ):

        elements.append(
            Paragraph(
                f"<b>Activity : {activity}</b>",
                styles["Heading3"]
            )
        )

        elements.append(Spacer(1, 8))

        data = [[
            "S.No",
            "Date of Entry",
            "Faculty Name (ID)",
            "Description"
            
        ]]

        for i, submission in enumerate(records, start=1):

            data.append([
                str(i),

                submission.entry_datetime.strftime("%d-%m-%Y"),

                Paragraph(
                    "<br/>".join(
                        f"<b>{sf.faculty.faculty_name}</b> ({sf.faculty.faculty_id})"
                        for sf in submission.faculty_members.all()
                    ),
                    styles["BodyText"]
                ),

                Paragraph(
                    submission.description,
                    styles["BodyText"]
                ),
            ])

        table = Table(
            data,
            colWidths=[40, 90, 150, 220],
            repeatRows=1
        )

        table.setStyle(TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,colors.black),
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#D9EAF7")),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("ALIGN",(0,0),(0,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("BOTTOMPADDING",(0,0),(-1,0),8),
            ("TOPPADDING",(0,1),(-1,-1),6),
            ("BOTTOMPADDING",(0,1),(-1,-1),6),
        ]))

        elements.append(table)
        elements.append(Spacer(1,18))

    document.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return response

def add_page_number(canvas, doc):

    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    canvas.drawString(
        35,
        25,
        "Generated on : " +
        timezone.localtime().strftime("%d-%m-%Y %I:%M %p")
    )

    canvas.drawRightString(
        560,
        25,
        f"Page {doc.page}"
    )

    canvas.restoreState()

@login_required
def show_activities(request):

    months = (
        Submission.objects.filter(user=request.user)

        .annotate(month=TruncMonth("activity_date"))

        .values_list("month", flat=True)

        .distinct()

        .order_by("-month")

    )

    return render(

        request,

        "activities/show_activities.html",

        {

            "months": months

        }

    )

@login_required
def get_activities(request):

    print(request.GET)

    month=request.GET.get("month")

    year=int(month.split("-")[0])

    month_number=int(month.split("-")[1])

    submissions = Submission.objects.filter(
        user=request.user,
        activity_date__year=year,
        activity_date__month=month_number
    ).prefetch_related(

        "faculty_members__faculty",

        "attachments"

    )

    from_date=request.GET.get("from_date")

    to_date=request.GET.get("to_date")

    if from_date and to_date:

        submissions=submissions.filter(

            activity_date__range=[

                from_date,

                to_date

            ]

        )

    data=[]

    for submission in submissions:

        attachments = []

        for attachment in submission.attachments.all():

            attachments.append({

                "id": attachment.id,

                "filename": attachment.original_filename

            })

        for sf in submission.faculty_members.all():

            data.append({

                "submission_id": submission.id,

                "faculty_id":sf.faculty.faculty_id,

                "faculty_name":sf.faculty.faculty_name,

                "activity":submission.activity.activity_name,

                "activity_date":submission.activity_date.strftime("%d-%m-%Y"),

                "entry_datetime": timezone.localtime(
                    submission.entry_datetime
                ).strftime("%d-%m-%Y %I:%M:%S %p"),

                "updated_at": timezone.localtime(
                    submission.updated_at
                ).strftime("%B %d, %Y, %I:%M:%S %p"),

                "description":submission.description,

                "attachments": attachments,

            })

    return JsonResponse({

        "data":data

    })

@login_required
def download_proof(request,file_id):

    attachment=Attachment.objects.get(id=file_id)

    path=attachment.uploaded_file.path

    if not os.path.exists(path):

        raise Http404()

    response=FileResponse(

        open(path,"rb"),

        as_attachment=True,

        filename=attachment.original_filename

    )

    return response

@login_required
def dashboard_partial(request):

    total_faculty = Faculty.objects.count()

    total_submissions = Submission.objects.filter(
        user=request.user
    ).count()

    today = timezone.now()

    reports_generated = ReportDownload.objects.filter(
        user=request.user,
        month__year=today.year,
        month__month=today.month
    ).count()

    current_month = timezone.now().month
    current_year = timezone.now().year

    month_activities = Submission.objects.filter(
        user=request.user,
        activity_date__month=current_month,
        activity_date__year=current_year
    ).count()

    recent = Submission.objects.filter(
        user=request.user
    ).select_related(
        "activity"
    ).order_by("-entry_datetime")[:10]

    return render(
        request,
        "activities/partials/dashboard.html",
        {
            "total_faculty": total_faculty,
            "total_submissions": total_submissions,
            "reports_generated": reports_generated,
            "month_activities": month_activities,
            "recent": recent,
        }
    )

@login_required
@require_POST
def delete_activity(request, id):

    try:

        submission = get_object_or_404(
            Submission,
            id=id,
            user=request.user
        )

        submission.delete()

        return JsonResponse({

            "status": "success",

            "message": "Activity deleted successfully."

        })

    except Submission.DoesNotExist:

        return JsonResponse({

            "status": "error",

            "message": "Activity not found."

        }, status=404)

@login_required
def edit_activity(request, id):

    submission = get_object_or_404(
        Submission,
        id=id,
        user=request.user
    )

    faculty_ids = list(

        submission.faculty_members.values_list(
            "faculty_id",
            flat=True
        )

    )

    attachment_data = []

    for attachment in submission.attachments.all():

        attachment_data.append({

            "id": attachment.id,

            "name": attachment.original_filename

        })

    return JsonResponse({

        "submission_id": submission.id,

        "activity": submission.activity.id,

        "activity_date": submission.activity_date.strftime("%Y-%m-%d"),

        "entry_date": submission.entry_datetime.strftime("%Y-%m-%d"),

        "description": submission.description,

        "faculty": faculty_ids,

        "attachments": attachment_data

    })

@login_required
@require_POST
def update_activity(request,id):

    submission = get_object_or_404(
        Submission,
        id=id,
        user=request.user
    )

    submission.activity_id=request.POST["activity"]

    submission.activity_date=request.POST["activity_date"]

    submission.description=request.POST["description"]

    submission.save()

    submission.faculty_members.all().delete()

    for faculty in request.POST.getlist("faculty"):

        SubmissionFaculty.objects.create(

            submission=submission,

            faculty_id=faculty

        )

    for file in request.FILES.getlist("attachments"):

        Attachment.objects.create(

            submission=submission,

            uploaded_file=file,

            original_filename=file.name

        )

    return JsonResponse({

        "message":"Activity updated successfully."

    })

@login_required
@require_POST
def delete_attachment(request, id):

    if request.method == "POST":

        attachment = Attachment.objects.get(id=id)

        # Delete the PDF from media folder
        if attachment.uploaded_file:
            if os.path.exists(attachment.uploaded_file.path):
                os.remove(attachment.uploaded_file.path)

        # Delete database record
        attachment.delete()

        return JsonResponse({
            "message": "Attachment deleted successfully."
        })

    return JsonResponse({
        "message": "Invalid request."
    }, status=400)

from django.http import JsonResponse
from .models import Faculty

@login_required
def add_faculty(request):

    if request.method == "POST":

        name = request.POST.get("faculty_name").strip()

        faculty = Faculty.objects.filter(
            faculty_name__iexact=name
        ).first()

        if faculty:

            return JsonResponse({

                "id": faculty.id,
                "name": faculty.faculty_name,
                "created": False

            })

        faculty = Faculty.objects.create(

            faculty_id=generate_faculty_id(),

            faculty_name=name

        )

        return JsonResponse({

            "id": faculty.id,
            "name": faculty.faculty_name,
            "created": True

        })
    
from .models import Activity

@login_required
def add_activity(request):

    if request.method=="POST":

        name=request.POST.get("activity_name").strip()

        activity,created=Activity.objects.get_or_create(

            activity_name=name

        )

        return JsonResponse({

            "id":activity.id,
            "name":activity.activity_name,
            "created":created

        })

@login_required
def get_faculty_list(request):

    faculty = Faculty.objects.all().order_by("faculty_name")

    return JsonResponse([
        {
            "id": f.id,
            "name": f.faculty_name
        }
        for f in faculty
    ], safe=False)

@login_required
def get_activity_list(request):

    activities = Activity.objects.all().order_by("activity_name")

    return JsonResponse([
        {
            "id": a.id,
            "name": a.activity_name
        }
        for a in activities
    ], safe=False)