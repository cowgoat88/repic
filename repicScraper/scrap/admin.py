from django.contrib import admin

# Register your models here.
from .models import Submission

@admin.register(Submission)
class ExplorationsAdmin(admin.ModelAdmin):
	pass
