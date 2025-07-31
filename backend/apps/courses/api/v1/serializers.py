from rest_framework import serializers
from apps.courses.models import (
    Courses,
    Courses_Categories,
    Courses_Sections,
    Lessons_Materials,
    Section_Lessons,
)
# from django.core.serializers.json import Serializer


class CoursesSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    status_name = serializers.ReadOnlyField(source="get_status_display")
    count_lessons = serializers.SerializerMethodField("get_lessons_count")

    class Meta:
        model = Courses
        fields = [
            "public_id",
            "name",
            "category_name",
            "short_description",
            "full_description",
            "teaser",
            "coast",
            "category",
            "status",
            "duration",
            "status_name",
            "created",
            "count_lessons",
        ]

        extra_kwargs = {
            "public_id": {"read_only": True},
            "category_name": {"read_only": True},
            "category": {"write_only": True},
            
            "full_description": {"write_only": True},
            "teaser": {"write_only": True},
            "status": {"write_only": True},
            "count_lessons": {"read_only": True},
            # "duration": {"write_only": True},
        }

    def get_lessons_count(self, object_course):
        return Section_Lessons.objects.filter(section__course=object_course).count()


class CoursesAddSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    status_name = serializers.ReadOnlyField(source="get_status_display")
    
    # count_lessons = serializers.SerializerMethodField("get_lessons_count")

    class Meta:
        model = Courses
        fields = [
            "public_id",
            "name",
            "category_name",
            "short_description",
            "full_description",
            "teaser",
            "coast",
            "category",
            "status",
            "duration",
            "status_name",
            "created",
            # "count_lessons",
        ]

        extra_kwargs = {
            "public_id": {"read_only": True},
            "category_name": {"read_only": True},
            "category": {"write_only": True},
            
            "full_description": {"write_only": True},
            "teaser": {"write_only": True},
            "status": {"write_only": True},
            "count_lessons": {"read_only": True},
            "duration": {"read_only": True},
        }

    # def get_lessons_count(self, object_course):
    #     return Section_Lessons.objects.filter(section__course=object_course).count()


class CourseDetailsSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField("get_lessons_count")
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Courses
        fields = [
            "public_id",
            "name",
            "short_description",
            "full_description",
            "teaser",
            "coast",
            "category",
            "category_name",
            "status",
            "duration",
            "created",
            "updated",
            "count_lessons",
        ]

        extra_kwargs = {
            "category_name": {"read_only": True},
            "category": {"write_only": True},
        }

    def create(self, validated_data):
        return Courses.objects.create(**validated_data)

    def get_lessons_count(self, object_course):
        return Section_Lessons.objects.filter(section__course=object_course).count()


class Courses_CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses_Categories
        fields = ["public_id", "name"]


class Courses_CategoriesDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses_Categories
        fields = ["public_id", "name", "created", "updated"]


class Courses_SectionsSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source="course.name")

    class Meta:
        model = Courses_Sections
        fields = ["public_id","name", "course", "course_name"]

        extra_kwargs = {
            "course_name": {"read_only": True},
            "course": {"write_only": True},
        }


class Courses_SectionDetailsSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source="courses.name")

    class Meta:
        model = Courses_Sections
        fields = ["public_id", "name", "course","course_name", "created", "updated"]

        extra_kwargs = {
            "course_name": {"read_only": True},
            "course": {"write_only": True},
        }


class Section_LessonsSerializer(serializers.ModelSerializer):
    section_name = serializers.ReadOnlyField(source="section.name")

    class Meta:
        model = Section_Lessons
        fields = ["public_id","name", "description", "section", "section_name"]

        extra_kwargs = {
            "section_name": {"read_only": True},
            "section": {"write_only": True},
        }


class Section_LessonDetailsSerializer(serializers.ModelSerializer):
    section_name = serializers.ReadOnlyField(source="section.name")

    class Meta:
        model = Section_Lessons
        fields = [
            "public_id",
            "name",
            # "video",
            "description",
            "section",
            "section_name",
            # "duration",
            # "additional_materials",
            "created",
            "updated",
        ]

        extra_kwargs = {
            "section_name": {"read_only": True},
            "section": {"write_only": True},
        }


class Lessons_MaterialsSerializer(serializers.ModelSerializer):
    lesson_name = serializers.ReadOnlyField(source="lesson.name")

    class Meta:
        model = Lessons_Materials
        fields = ["public_id","lesson", "content", "lesson_name"]

        extra_kwargs = {
            "lesson_name": {"read_only": True},
            "lesson": {"write_only": True},
        }


class Lessons_MaterialDetailsSerializer(serializers.ModelSerializer):
    lesson_name = serializers.ReadOnlyField(source="lesson.name")

    class Meta:
        model = Lessons_Materials
        fields = ["public_id", "lesson","lesson_name", "content", "created", "updated"]
        extra_kwargs = {
            "lesson_name": {"read_only": True},
            "lesson": {"write_only": True},
        }

    
class AnautorizedSerializer(serializers.Serializer):
    class Meta:
        # model = Courses
        extra_kwargs =  {
        "message" : {    
        "type": "client_error",
        "errors": [
            {
            "code": "not_authenticated",
            "detail": "Учетные данные не были предоставлены.",
            "attr": "null"
            }
        ],
        "success": False,
        "message": "Unauthorized"}}
        fields = 'message'
