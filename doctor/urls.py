from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.DoctorDashboardView.as_view(), name="doctor_dashboard"),
    path(
        "dashboard/appointments/",
        views.DoctorAppointmentsView.as_view(),
        name="doctor_appointments",
    ),
    path(
        "dashboard/appointments/<str:pk>/",
        views.AppointmentDetailsView.as_view(),
        name="doctor_appointment_details",
    ),
    # create new medical record
    path(
        "create-medical-record/<str:appointment_id>",
        views.DoctorCreateMedicalRecordView.as_view(),
        name="create_medical_record",
    ),
    # update medical record
    path(
        "edit-medical-record/<int:medical_record_id>/<str:appointment_id>",
        views.DoctorEditMedicalRecordView.as_view(),
        name="edit_medical_record",
    ),
    # create new labtest
    path(
        "create-lab-test/<str:appointment_id>",
        views.DoctorCreateLabTestView.as_view(),
        name="create_lab_test",
    ),
    # update medical record
    path(
        "edit-lab-test/<int:lab_test_id>/<str:appointment_id>",
        views.DoctorEditLabTestView.as_view(),
        name="edit_lab_test",
    ),
    # create prescription
    path(
        "create-prescription/<str:appointment_id>",
        views.DoctorCreatePrescriptionView.as_view(),
        name="create_prescription",
    ),
    # update prescription
    path(
        "edit-prescription/<int:prescription_id>/<str:appointment_id>",
        views.DoctorEditPrescriptionView.as_view(),
        name="edit_prescription",
    ),
    # complete appointment
    path(
        "complete-appointment/<str:appointment_id>",
        views.DoctorCompleteAppointment.as_view(),
        name="doctor_complete_appointment",
    ),
    # cancel appointment
    path(
        "cancel-appointment/<str:appointment_id>",
        views.DoctorCancelledAppointment.as_view(),
        name="doctor_cancel_appointment",
    ),
    # activate appointment
    path(
        "activate-appointment/<str:appointment_id>",
        views.DoctorActivatedAppointment.as_view(),
        name="doctor_activate_appointment",
    ),
    # payments
    path("payments/", views.DoctorPaymentsView.as_view(), name="doctor_payments"),
    # notifications
    path(
        "notifications/",
        views.DoctorNotificationsView.as_view(),
        name="doctor_notifications",
    ),
    # mark seen notification
    path(
        "mark-notification-seen/<int:notification_id>",
        views.DoctorMarkSeenNotificationView.as_view(),
        name="mark_notification_seen",
    ),
    # doctor profile
    path("profile/", views.DoctorProfileView.as_view(), name="doctor_profile"),
]
