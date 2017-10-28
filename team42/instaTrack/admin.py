from django.contrib import admin

from .models import UserProfile, WeFollowID, WeTrackID, WeFollowUser

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WeFollowID)
admin.site.register(WeTrackID)