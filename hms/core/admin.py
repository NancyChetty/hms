from django.contrib import admin

from .models import User
from .models import Slot
from .models import Booking


admin.site.register(User)
admin.site.register(Slot)
admin.site.register(Booking)