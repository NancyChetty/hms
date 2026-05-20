import requests

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import SignupForm, SlotForm
from .models import User, Slot, Booking, Notification
from .calendar_service import create_event, delete_event

EMAIL_SERVICE_URL = "http://localhost:3000/send-email"


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'doctor':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'patient':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# =====================================================
# SIGNUP
# =====================================================

@ensure_csrf_cookie
def signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            requests.post(
                EMAIL_SERVICE_URL,
                json={
                    "type": "SIGNUP_WELCOME",
                    "email": user.email,
                    "username": user.username
                }
            )
            messages.success(request, 'Account created successfully.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


# =====================================================
# LOGIN
# =====================================================

@ensure_csrf_cookie
def login_view(request):

    if request.user.is_authenticated:
        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')
        return redirect('patient_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'core/login.html')


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):
    logout(request)
    return redirect('login')


# =====================================================
# DOCTOR DASHBOARD
# =====================================================

@ensure_csrf_cookie
@doctor_required
def doctor_dashboard(request):

    slots = Slot.objects.filter(
        doctor=request.user
    ).order_by('start_time')

    bookings = Booking.objects.filter(
        slot__doctor=request.user
    ).select_related('patient', 'slot')

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    return render(request, 'doctor_dashboard.html', {
        'slots': slots,
        'bookings': bookings,
        'notifications': notifications
    })


# =====================================================
# PATIENT DASHBOARD
# =====================================================

@ensure_csrf_cookie
@patient_required
def patient_dashboard(request):

    slots = Slot.objects.filter(
        is_booked=False
    ).order_by('start_time')

    my_bookings = Booking.objects.filter(
        patient=request.user
    ).select_related('slot', 'slot__doctor')

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    return render(request, 'patient_dashboard.html', {
        'slots': slots,
        'my_bookings': my_bookings,
        'notifications': notifications
    })


# =====================================================
# CREATE SLOT
# =====================================================

@doctor_required
def create_slot(request):

    if request.method == 'POST':
        form = SlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            messages.success(request, 'Slot created successfully.')
            return redirect('doctor_dashboard')
    else:
        form = SlotForm()

    return render(request, 'create_slot.html', {'form': form})


# =====================================================
# UPDATE SLOT
# =====================================================

@doctor_required
def update_slot(request, slot_id):

    slot = get_object_or_404(Slot, id=slot_id, doctor=request.user)

    if request.method == 'POST':
        form = SlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slot updated successfully.')
            return redirect('doctor_dashboard')
    else:
        form = SlotForm(instance=slot)

    return render(request, 'update_slot.html', {'form': form})


# =====================================================
# DELETE SLOT
# =====================================================

@doctor_required
def delete_slot(request, slot_id):

    slot = get_object_or_404(Slot, id=slot_id, doctor=request.user)
    slot.delete()
    messages.success(request, 'Slot deleted successfully.')
    return redirect('doctor_dashboard')


# =====================================================
# BOOK SLOT
# =====================================================

@patient_required
def book_slot(request, slot_id):

    slot = get_object_or_404(Slot, id=slot_id)

    if slot.is_booked:
        messages.error(request, 'Slot already booked.')
        return redirect('patient_dashboard')

    Booking.objects.create(
        patient=request.user,
        slot=slot,
        status='pending'
    )

    slot.is_booked = True
    slot.save()

    Notification.objects.create(
        user=slot.doctor,
        message=f"New appointment request from {request.user.username} for {slot.start_time}"
    )

    send_mail(
        'Appointment Request Sent',
        f'Hello {request.user.username},\n\nYour appointment request with Dr. {slot.doctor.username} has been sent.\n\nPlease wait for doctor approval.',
        'yourhospital@gmail.com',
        [request.user.email],
        fail_silently=True,
    )

    messages.success(request, 'Appointment request sent successfully.')
    return redirect('patient_dashboard')


# =====================================================
# UPDATE BOOKING STATUS
# =====================================================

@doctor_required
def update_booking_status(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':

        status = request.POST.get('status')
        booking.status = status
        booking.save()

        if status == 'confirmed':

            event_id = create_event(
                doctor_email='nancychetty48@gmail.com',
                patient_email='jazz142008@gmail.com',
                start_time=booking.slot.start_time,
                end_time=booking.slot.end_time
            )
            booking.calendar_event_id = event_id
            booking.save()

            Notification.objects.create(
                user=booking.patient,
                message=f"Your appointment with Dr. {booking.slot.doctor.username} on {booking.slot.start_time} has been confirmed."
            )

            send_mail(
                'Appointment Confirmed',
                f'Hello {booking.patient.username},\n\nYour appointment with Dr. {booking.slot.doctor.username} on {booking.slot.start_time} has been confirmed.',
                'yourhospital@gmail.com',
                [booking.patient.email],
                fail_silently=True,
            )

            messages.success(request, 'Appointment accepted.')

        elif status == 'cancelled':

            booking.slot.is_booked = False
            booking.slot.save()

            delete_event(booking.calendar_event_id)

            Notification.objects.create(
                user=booking.patient,
                message=f"Your appointment with Dr. {booking.slot.doctor.username} on {booking.slot.start_time} was rejected."
            )

            send_mail(
                'Appointment Rejected',
                f'Hello {booking.patient.username},\n\nYour appointment with Dr. {booking.slot.doctor.username} was rejected.',
                'yourhospital@gmail.com',
                [booking.patient.email],
                fail_silently=True,
            )

            messages.error(request, 'Appointment rejected.')

    return redirect('doctor_dashboard')


# =====================================================
# CANCEL BOOKING (patient)
# =====================================================

@patient_required
def cancel_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id, patient=request.user)
    doctor = booking.slot.doctor

    booking.status = 'cancelled'
    booking.save()

    booking.slot.is_booked = False
    booking.slot.save()

    delete_event(booking.calendar_event_id)

    Notification.objects.create(
        user=doctor,
        message=f"{request.user.username} cancelled their appointment on {booking.slot.start_time}."
    )

    send_mail(
        'Appointment Cancelled by Patient',
        f'Hello Dr. {doctor.username},\n\n{request.user.username} has cancelled their appointment on {booking.slot.start_time}.',
        'yourhospital@gmail.com',
        [doctor.email],
        fail_silently=True,
    )

    messages.success(request, 'Booking cancelled successfully.')
    return redirect('patient_dashboard')


# =====================================================
# COMPLETE BOOKING (doctor)
# =====================================================

@doctor_required
def complete_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id, slot__doctor=request.user)

    booking.status = 'completed'
    booking.save()

    delete_event(booking.calendar_event_id)

    Notification.objects.create(
        user=booking.patient,
        message=f"Your appointment with Dr. {request.user.username} on {booking.slot.start_time} has been marked as completed."
    )

    messages.success(request, 'Appointment marked as completed.')
    return redirect('doctor_dashboard')


# =====================================================
# DASHBOARD POLL API
# =====================================================

@auth_required
def dashboard_poll(request):

    if request.user.role == 'doctor':
        bookings = Booking.objects.filter(
            slot__doctor=request.user
        ).select_related('patient', 'slot')

        slots = Slot.objects.filter(doctor=request.user)

        data = {
            'stats': {
                'total_slots': slots.count(),
                'total_bookings': bookings.count(),
                'total_patients': bookings.values('patient').distinct().count(),
                'completed': bookings.filter(status='completed').count(),
            },
            'pending': [{'id': b.id, 'patient': b.patient.username, 'time': str(b.slot.start_time)} for b in bookings if b.status == 'pending'],
            'upcoming': [{'id': b.id, 'patient': b.patient.username, 'time': str(b.slot.start_time)} for b in bookings if b.status == 'confirmed'],
            'history': [{'id': b.id, 'patient': b.patient.username, 'time': str(b.slot.start_time), 'status': b.status} for b in bookings if b.status in ('completed', 'cancelled')],
            'notifications': [{'message': n.message, 'time': str(n.created_at), 'is_read': n.is_read} for n in Notification.objects.filter(user=request.user).order_by('-created_at')[:10]],
        }

    else:
        my_bookings = Booking.objects.filter(
            patient=request.user
        ).select_related('slot', 'slot__doctor')

        data = {
            'stats': {
                'my_bookings': my_bookings.count(),
                'available_slots': Slot.objects.filter(is_booked=False).count(),
                'upcoming': my_bookings.filter(status='confirmed').count(),
                'completed': my_bookings.filter(status='completed').count(),
            },
            'my_bookings': [{'id': b.id, 'doctor': b.slot.doctor.username, 'time': str(b.slot.start_time), 'status': b.status} for b in my_bookings],
            'upcoming': [{'id': b.id, 'doctor': b.slot.doctor.username, 'day': b.slot.start_time.strftime('%d'), 'mon': b.slot.start_time.strftime('%b'), 'time': b.slot.start_time.strftime('%I:%M %p')} for b in my_bookings if b.status == 'confirmed'],
            'notifications': [{'message': n.message, 'time': str(n.created_at), 'is_read': n.is_read} for n in Notification.objects.filter(user=request.user).order_by('-created_at')[:10]],
        }

    return JsonResponse(data)


# =====================================================
# SEND EMAIL TEST
# =====================================================

def send_email(request):
    return JsonResponse({'status': 'ok'})


# =====================================================
# GOOGLE CONNECT / CALLBACK (placeholder)
# =====================================================

def connect_google(request):
    return redirect('doctor_dashboard')


def google_callback(request):
    return redirect('doctor_dashboard')
