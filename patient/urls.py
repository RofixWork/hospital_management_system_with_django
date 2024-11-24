from django.urls import path

from . import views

urlpatterns = [
    path(
        "dashboard/",
        views.PatientDashboardView.as_view(),
        name="patient_dashboard",
    ),
    path(
        "dashboard/appointments/",
        views.PatientAppointmentsView.as_view(),
        name="patient_appointments",
    ),
    path(
        "dashboard/appointments/<str:pk>/",
        views.AppointmentDetailsView.as_view(),
        name="patient_appointment_details",
    ),
    # complete appointment
    path(
        "patient-complete-appointment/<str:appointment_id>",
        views.PatientCompleteAppointment.as_view(),
        name="patient_complete_appointment",
    ),
    # cancel appointment
    path(
        "patient-cancel-appointment/<str:appointment_id>",
        views.PatientCancelledAppointment.as_view(),
        name="patient_cancel_appointment",
    ),
    # activate appointment
    path(
        "patient-activate-appointment/<str:appointment_id>",
        views.PatientActivatedAppointment.as_view(),
        name="patient_activate_appointment",
    ),
    # payments
    path("payments/", views.PatientPaymentsView.as_view(), name="patient_payments"),
    # notifications
    path(
        "notifications/",
        views.PatientNotificationsView.as_view(),
        name="patient_notifications",
    ),
    # mark seen notification
    path(
        "patient-mark-notification-seen/<int:notification_id>",
        views.PatientMarkSeenNotificationView.as_view(),
        name="patient_mark_notification_seen",
    ),
    # doctor profile
    path(
        "patient-profile/", views.PatientProfileView.as_view(), name="patient_profile"
    ),
]
