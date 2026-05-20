from django.urls import path
from . import views
from .views import send_email

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('create-slot/', views.create_slot, name='create_slot'),
    path('update-slot/<int:slot_id>/', views.update_slot, name='update_slot'),
    path('delete-slot/<int:slot_id>/', views.delete_slot, name='delete_slot'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('update-booking-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('complete-booking/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('dashboard-poll/', views.dashboard_poll, name='dashboard_poll'),
    path('connect-google/', views.connect_google, name='connect_google'),
    path('google-callback/', views.google_callback, name='google_callback'),
    path('send-email/', send_email, name='send_email'),
]