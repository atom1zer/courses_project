from django.db import models
from core.utils.models import (
    AbstractManager,
    AbstractModel,
)

# from utils.abstract.models import AbstractManager
from django.db.models import Count

from core.s3_storage import ClientDocsStorage
# from utils.abstract.models import AbstractModel


class CoursesManager(AbstractManager):
    pass


class Courses_CategoriesManager(AbstractManager):
    pass


class Courses_SectionsManager(AbstractManager):
    pass


class Section_LessonsManager(AbstractManager):
    pass


class Lessons_MaterialsManager(AbstractManager):
    pass


class Courses_Categories(AbstractModel):

    name = models.CharField(max_length=250, verbose_name="Categories name")

    objects = Courses_CategoriesManager()

    class Meta:
        db_table = "courses_categories"

    def __str__(self):
        return self.name


class Courses(AbstractModel):

    class Course_Status(models.TextChoices):
        CANCELLED = "CL", "Cancelled"
        WORK_IN_PROGRESS = "WIP", "Work in progress"
        REQUIRES_ATTENTION = "RA", "Requires attention"
        COMPLETE = "CT", "Complete"

    name = models.CharField(max_length=200, verbose_name="Course name")
    short_description = models.CharField(
        max_length=300, verbose_name="Course short description"
    )
    full_description = models.TextField(verbose_name="Course full description")
    teaser = models.FileField(upload_to=None, verbose_name="Course teaser", null=True)
    coast = models.PositiveSmallIntegerField(verbose_name="Course cost")
    category = models.ForeignKey(
        Courses_Categories, on_delete=models.CASCADE, verbose_name="Course category"
    )
    status = models.CharField(
        max_length=3,
        choices=Course_Status.choices,
        default=Course_Status.WORK_IN_PROGRESS,
        verbose_name="Course status",
    )
    duration = models.TimeField(verbose_name="Course duration", blank=True, null=True)

    objects = CoursesManager()

    class Meta(AbstractModel.Meta):
        db_table = "courses"

    def __str__(self):
        # return (self.get_status_display(), self.name)
        return self.name

    def get_count(self):
        return self.sections.all().count()    


class Courses_Sections(AbstractModel):

    name = models.CharField(max_length=200, verbose_name="Sections name")
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="Course",
    )

    objects = Courses_SectionsManager()

    def get_count(self):
        return self.lessons.all().count()

    class Meta(AbstractModel.Meta):
        db_table = "courses_sections"


class Section_Lessons(AbstractModel):

    # TODO: убрать test as default
    name = models.CharField(max_length=200, verbose_name="Lesson name", default="Test")
    # video = models.FileField(
    #     upload_to=None, verbose_name="Lesson section video", null=True
    # )
    description = models.TextField(verbose_name="Lesson section description")
    section = models.ForeignKey(
        Courses_Sections,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Course section",
    )
    # duration = models.TimeField(verbose_name="Lesson section duration",null=True)
    # additional_materials = models.FileField(
    #     upload_to=None, verbose_name="Lesson section additional materials", null=True
    # )

    objects = Section_LessonsManager()

    class Meta(AbstractModel.Meta):
        db_table = "section_lessons"

#TODO: убрать default
class Lessons_Materials(AbstractModel):
    lesson = models.ForeignKey(
        Section_Lessons, on_delete=models.CASCADE, verbose_name="Course section lesson"
    )
    content = models.FileField(storage=ClientDocsStorage,max_length=400)
    url = models.CharField(max_length=400, blank=True,null=True)
    objects = Lessons_MaterialsManager()

    class Meta(AbstractModel.Meta):
        db_table = "lessons_materials"
