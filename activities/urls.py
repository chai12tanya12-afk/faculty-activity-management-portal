from django.urls import path
from . import views

urlpatterns = [

    path("", views.login_view, name="login"),

    path("register/",views.register_view,name="register"),

    path("home/",views.home,name="home"),

    path("logout/",views.logout_view,name="logout"),

    path(
        "faculty-form/",
        views.faculty_form_partial,
        name="faculty_form"
    ),

    path(
        "monthly-report/",
        views.monthly_report_partial,
        name="monthly_report"
    ),

    path(
        "show-activities/",
        views.show_activities_partial,
        name="show_activities"
    ),

    path(
        "submit/",
        views.submit_form,
        name="submit_form"
    ),

    path(
        "download-report/",
        views.download_report,
        name="download_report"
    ),

    path(
        "get-activities/",
        views.get_activities,
        name="get_activities"
    ),

    path(
        "download-proof/<int:file_id>/",
        views.download_proof,
        name="download_proof"
    ),

    path(
        "dashboard/",
        views.dashboard_partial,
        name="dashboard"
    ),

    path(
        "delete-activity/<int:id>/",
        views.delete_activity,
        name="delete_activity"
    ),

    path(
        "edit-activity/<int:id>/",
        views.edit_activity,
        name="edit_activity"
    ),

    path(
        "update-activity/<int:id>/",
        views.update_activity,
        name="update_activity"
    ),

    path(

        "delete-attachment/<int:id>/",

        views.delete_attachment,

        name="delete_attachment"

    ),

    path("add-faculty/", views.add_faculty, name="add_faculty"),
    path("add-activity/", views.add_activity, name="add_activity"),

    path("faculty-list/", views.get_faculty_list),
    path("activity-list/", views.get_activity_list),
]