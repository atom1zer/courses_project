from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import Http404, HttpResponse
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger


from apps.courses.models import (
    Courses,
    Courses_Categories,
    Courses_Sections,
    Lessons_Materials,
    Section_Lessons,
)
from apps.courses.api.v1.serializers import (
    CoursesSerializer,
    CoursesAddSerializer,
    Courses_CategoriesSerializer,
    Courses_SectionsSerializer,
    Lessons_MaterialsSerializer,
    Section_LessonsSerializer,
    AnautorizedSerializer,
)
from apps.courses.api.v1.serializers import (
    CourseDetailsSerializer,
    Courses_CategoriesDetailsSerializer,
    Courses_SectionDetailsSerializer,
)
from apps.courses.api.v1.serializers import (
    Section_LessonDetailsSerializer,
    Lessons_MaterialDetailsSerializer,
)
from core.utils.views import AbstractApiView, AbstractGetApiView, AbstractApiViewDetails
from drf_standardized_errors.openapi_serializers import Error401Serializer

from rest_framework.parsers import MultiPartParser #FileUploadParser

from core.utils.utils import upload_file_to_s3

from django.core.files.storage import FileSystemStorage

import os
from moviepy import VideoFileClip
import time

@extend_schema(tags=["Courses"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список курсов",
        request=CoursesSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=str),
        ],
        responses={200: CoursesSerializer, 401: Error401Serializer},
    ),
)
class CoursesView(AbstractGetApiView):
    permission_classes = [permissions.AllowAny]
    state_model = Courses
    serializer_class = CoursesSerializer


@extend_schema(tags=["Courses"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить полный список курсов",
        request=CoursesSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=str),
        ],
        responses={200: CoursesSerializer, 401: Error401Serializer},
    ),
)
class CoursesView(AbstractGetApiView):
    permission_classes = [permissions.AllowAny]
    state_model = Courses
    serializer_class = CoursesSerializer


@extend_schema(tags=["Courses"])
@extend_schema_view(
    post=extend_schema(
        summary="Создание нового курса",
        request=CoursesAddSerializer,
        responses={200: CoursesAddSerializer, 401: Error401Serializer},
    ),
    get=extend_schema(
        summary="Получить список курсов по заданной категории",
        request=CoursesSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=str),
        ],
        responses={200: CoursesSerializer, 401: Error401Serializer},
    ),
)
class CoursesFromCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    state_model = Courses
    foreign_model = Courses_Categories
    serializer_class = CoursesAddSerializer

    def get_object_by_public_id(self, public_id=None):
        try:
            return self.foreign_model.objects.get(public_id=public_id)
        except:
            return None
        
    def get_object(self, name=None):
        try:
            return self.state_model.objects.get(name=name)
        except:
            return None

    def post(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id)
                request.data["category"] = foreign_object.id
            except:
                raise Http404
        if self.get_object(request.data["name"]):
            return HttpResponse("Курс с таким названием уже существует!", status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id=public_id)
            except:
                raise Http404
        courses_object = self.state_model.objects.filter(category=foreign_object.id)
        paginator = Paginator(courses_object, 5)
        page = request.GET.get("page")
        try:
            courses_page_object = paginator.page(page)
        except PageNotAnInteger:
            courses_page_object = paginator.page(1)
        except EmptyPage:
            courses_page_object = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(courses_page_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Course_details"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить курс по public_id",
        request=CourseDetailsSerializer,
        responses={200: CourseDetailsSerializer, 401: Error401Serializer},
    ),
    patch=extend_schema(
        summary="Изменить конкретный курс",
        request=CourseDetailsSerializer,
        responses={200: CourseDetailsSerializer, 401: Error401Serializer},
    ),
    delete=extend_schema(
        summary="Удалить курс по public_id",
        request=CourseDetailsSerializer,
        responses={200: "", 401: Error401Serializer},
    ),
)
class CoursesDetailView(AbstractApiViewDetails):

    state_model = Courses
    foreign_model = Courses_Categories
    serializer_class = CourseDetailsSerializer
    foreign_key = "category"


@extend_schema(tags=["Course_categories"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список категорий",
        request=Courses_CategoriesSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Courses_CategoriesSerializer, 401: Error401Serializer},
    ),
    post=extend_schema(
        summary="Создание новой категории",
        request=Courses_CategoriesSerializer,
        responses={200: Courses_CategoriesSerializer, 401: Error401Serializer},
    ),
)
class Courses_CategoriesView(AbstractApiView):

    state_model = Courses_Categories
    serializer_class = Courses_CategoriesSerializer


@extend_schema(tags=["Course_categories_details"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить категорию по public_id",
        request=Courses_CategoriesDetailsSerializer,
        responses={200: Courses_CategoriesDetailsSerializer, 401: Error401Serializer},
    ),
    patch=extend_schema(
        summary="Изменить конкретную категорию",
        request=Courses_CategoriesDetailsSerializer,
        responses={200: Courses_CategoriesDetailsSerializer, 401: Error401Serializer},
    ),
    delete=extend_schema(
        summary="Удалить категорию по public_id",
        request=Courses_CategoriesDetailsSerializer,
        responses={200: "", 401: Error401Serializer},
    ),
)
class Courses_CategoriesDetailsView(AbstractApiViewDetails):

    state_model = Courses_Categories
    serializer_class = Courses_CategoriesDetailsSerializer


@extend_schema(tags=["Course_sections"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список разделов по конкретному курсу",
        request=Courses_SectionsSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Courses_SectionsSerializer, 401: Error401Serializer},
    ),
    post=extend_schema(
        summary="Создание нового раздела урока",
        request=Courses_SectionsSerializer,
        responses={200: Courses_SectionsSerializer, 401: Error401Serializer},
    ),
)
class Courses_SectionsFromCourseView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = Courses_Sections
    foreign_model = Courses
    serializer_class = Courses_SectionsSerializer

    def get_object_by_public_id(self, public_id=None):
        try:
            return self.foreign_model.objects.get(public_id=public_id)
        except:
            return None

    def post(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id)
                request.data["course"] = foreign_object.id
            except:
                raise Http404
        if self.get_object_by_public_id(request.data["name"]):
            return HttpResponse("Раздел с таким названием уже существует!", status=400)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id)
            except:
                raise Http404
        courses_object = self.state_model.objects.filter(course=foreign_object.id)
        paginator = Paginator(courses_object, 5)
        page = request.GET.get("page")
        try:
            courses_page_object = paginator.page(page)
        except PageNotAnInteger:
            courses_page_object = paginator.page(1)
        except EmptyPage:
            courses_page_object = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(courses_page_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Course_sections"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить полный список разделов",
        request=Courses_SectionsSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Courses_SectionsSerializer, 401: Error401Serializer},
    ),
)
class Courses_SectionsView(AbstractGetApiView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = Courses_Sections
    serializer_class = Courses_SectionsSerializer


@extend_schema(tags=["Course_sections_details"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить раздел по public_id",
        request=Courses_SectionDetailsSerializer,
        responses={200: Courses_SectionDetailsSerializer, 401: Error401Serializer},
    ),
    patch=extend_schema(
        summary="Изменить конкретный раздел",
        request=Courses_SectionDetailsSerializer,
        responses={200: Courses_SectionDetailsSerializer, 401: Error401Serializer},
    ),
    delete=extend_schema(
        summary="Удалить раздел по public_id",
        request=Courses_SectionDetailsSerializer,
        responses={200: "", 401: Error401Serializer},
    ),
)
class Courses_SectionDetailsView(AbstractApiViewDetails):

    state_model = Courses_Sections
    serializer_class = Courses_SectionDetailsSerializer
    foreign_model = Courses
    foreign_key = "course"


@extend_schema(tags=["Lessons_materials"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список материлов по конкретному уроку",
        request=Lessons_MaterialsSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Lessons_MaterialsSerializer, 401: Error401Serializer},
    ),
    post=extend_schema(
        summary="Добавение нового материала для конкретного урока",
        request=Lessons_MaterialsSerializer,
        responses={200: Lessons_MaterialsSerializer, 401: Error401Serializer},
    ),
)
class Lessons_MaterialsFromLessonView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = Lessons_Materials
    foreign_model = Section_Lessons
    serializer_class = Lessons_MaterialsSerializer
    parser_classes = [MultiPartParser,]
    resolutions = ['1920x1080', '1280x720', '640x360']

    def get_object(self, public_id=None):
        try:
            return self.state_model.objects.get(public_id=public_id)
        except:
            return None    

    def get_object_by_public_id(self, public_id=None):
        try:
            return self.foreign_model.objects.get(public_id=public_id)
        except:
            return None

    # def post(self, request, public_id=None):
    #     if public_id:
    #         try:
    #             self.get_object_by_public_id(public_id)
    #         except:
    #             return Response("Lesson not found", status=status.HTTP_404_NOT_FOUND) 
    #     if request.data['content']:
    #         uploaded_file = request.data['content']
    #         fs = FileSystemStorage()
    #         filename = fs.save(uploaded_file.name, uploaded_file) # Saves to MEDIA_ROOT
    #         file_path = fs.path(filename)
    #         upload_file_to_s3.delay(file_path,public_id) # Pass path to Celery
    #         return Response("Start upload file", status=status.HTTP_200_OK)
    #     return Response("File not found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, public_id=None):
        start_time = time.time()
        remove_list = []
        if public_id:
            try:
                self.get_object_by_public_id(public_id)
            except:
                return Response("Lesson not found", status=status.HTTP_404_NOT_FOUND) 
        if request.data['content']:
            uploaded_file = request.data['content']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file) # Saves to MEDIA_ROOT
            file_path = fs.path(filename)

            # Загрузите видео на Yandex Storage
            # with open(file_path, 'rb') as f:
            #     client.buckets().upload(os.getenv("AWS_STORAGE_BUCKET_NAME"), file_path, f.read())

            for resolution in self.resolutions:
                # Измените разрешение видео
                video = VideoFileClip(file_path)
                new_video = video.resized(width=int(resolution.split('x')[0]), height=int(resolution.split('x')[1]))

                # Создайте новое имя файла с указанным разрешением
                dst_filename = f'{uploaded_file.name}_{resolution}.mp4'

                # Сэкономите видео в Yandex Storage под новым именем
                new_video.write_videofile(dst_filename)
                with open(dst_filename, 'rb') as f:
                    upload_file_to_s3(dst_filename, public_id)
                    remove_list.append(dst_filename)
            remove_list.append(file_path)    
            for file in remove_list:
                os.remove(file)
            # upload_file_to_s3.delay(file_path,public_id) # Pass path to Celery
            end_time = time.time()
            print(f"Time execute upload function: {end_time-start_time}")
            return Response("Start upload file", status=status.HTTP_200_OK)
        return Response("File not found", status=status.HTTP_404_NOT_FOUND)


    def get(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id)
            except:
                raise Http404
        courses_object = self.state_model.objects.filter(lesson=foreign_object.id)
        paginator = Paginator(courses_object, 5)
        page = request.GET.get("page")
        try:
            courses_page_object = paginator.page(page)
        except PageNotAnInteger:
            courses_page_object = paginator.page(1)
        except EmptyPage:
            courses_page_object = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(courses_page_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Lessons_materials"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список материлов",
        request=Courses_SectionsSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Courses_SectionsSerializer, 401: Error401Serializer},
    ),
)
class Lessons_MaterialsView(AbstractGetApiView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = Lessons_Materials
    serializer_class = Lessons_MaterialsSerializer


@extend_schema(tags=["Lesson_material_details"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить материал по public_id",
        request=Lessons_MaterialDetailsSerializer,
        responses={200: Lessons_MaterialDetailsSerializer, 401: Error401Serializer},
    ),
    patch=extend_schema(
        summary="Изменить конкретный материал",
        request=Lessons_MaterialDetailsSerializer,
        responses={200: Lessons_MaterialDetailsSerializer, 401: Error401Serializer},
    ),
    delete=extend_schema(
        summary="Удалить материал по public_id",
        request=Lessons_MaterialDetailsSerializer,
        responses={200: "", 401: Error401Serializer},
    ),
)
class Lessons_MaterialDetailsView(AbstractApiViewDetails):

    state_model = Lessons_Materials
    serializer_class = Lessons_MaterialDetailsSerializer
    foreign_model = Section_Lessons
    foreign_key = "lesson"


@extend_schema(tags=["Section_lessons"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список уроков по конкретному разделу",
        request=Section_LessonsSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Section_LessonsSerializer, 401: Error401Serializer},
    ),
    post=extend_schema(
        summary="Добавление нового урока для конкретного раздела",
        request=Section_LessonsSerializer,
        responses={200: Section_LessonsSerializer, 401: Error401Serializer},
    ),
)
class Section_LessonsFromCourseSectionView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = Section_Lessons
    foreign_model = Courses_Sections
    serializer_class = Section_LessonsSerializer

    def get_object_by_public_id(self, public_id=None):
        try:
            return self.foreign_model.objects.get(public_id=public_id)
        except:
            return None

    def post(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id)
                request.data["section"] = foreign_object.id
            except:
                raise Http404
        if self.get_object_by_public_id(request.data["name"]):
            return HttpResponse("Урок с таким названием уже существует!", status=400)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, public_id=None):
        if public_id:
            try:
                foreign_object = self.get_object_by_public_id(public_id)
            except:
                raise Http404
        courses_object = self.state_model.objects.filter(section=foreign_object.id)
        paginator = Paginator(courses_object, 5)
        page = request.GET.get("page")
        try:
            courses_page_object = paginator.page(page)
        except PageNotAnInteger:
            courses_page_object = paginator.page(1)
        except EmptyPage:
            courses_page_object = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(courses_page_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Section_lessons"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список уроков",
        request=Section_LessonsSerializer,
        parameters=[
            OpenApiParameter(name="page", description="Page number", type=int),
        ],
        responses={200: Section_LessonsSerializer, 401: Error401Serializer},
    ),
)
class Section_LessonsView(AbstractGetApiView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = Section_Lessons
    serializer_class = Section_LessonsSerializer


@extend_schema(tags=["Section_lesson_details"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить урок по public_id",
        request=Section_LessonDetailsSerializer,
        responses={200: Section_LessonDetailsSerializer, 401: Error401Serializer},
    ),
    patch=extend_schema(
        summary="Изменить конкретный урок",
        request=Section_LessonDetailsSerializer,
        responses={200: Section_LessonDetailsSerializer, 401: Error401Serializer},
    ),
    delete=extend_schema(
        summary="Удалить урок по public_id",
        request=Section_LessonDetailsSerializer,
        responses={200: "", 401: Error401Serializer},
    ),
)
class Section_LessonDetailsView(AbstractApiViewDetails):

    state_model = Section_Lessons
    serializer_class = Section_LessonDetailsSerializer
    foreign_model = Courses_Sections
    foreign_key = "section"
