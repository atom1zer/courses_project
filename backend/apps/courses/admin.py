from django.contrib import admin

from .models import Courses, Courses_Categories, Courses_Sections
from .models import Section_Lessons, Lessons_Materials

admin.site.register(Courses_Categories)
admin.site.register(Courses)
admin.site.register(Courses_Sections)
admin.site.register(Section_Lessons)
admin.site.register(Lessons_Materials)