from django.contrib import admin
from .models import (
    Region,
    City,
    JobTitleKeyword,
    Job,
)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(JobTitleKeyword)
admin.site.register(Job)
