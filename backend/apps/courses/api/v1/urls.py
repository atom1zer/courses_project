from django.urls import path
from apps.courses.api.v1 import views

urlpatterns = [
    # path("courses_list", views.CoursesView.as_view()),
    # path("categories_list", views.Courses_CategoriesView.as_view()),
    # path("courses_sections_list", views.Courses_SectionsView.as_view()),
    # path("lessons_materials_list", views.Lessons_MaterialsView.as_view()),
    # path("sections_lessons_list", views.Section_LessonsView.as_view()),
    # path("course_details/<uuid:public_id>", views.CoursesDetailView.as_view()),
    # path(
    #     "category_details/<uuid:public_id>",
    #     views.Courses_CategoriesDetailsView.as_view(),
    # ),
    # path(
    #     "course_section_details/<uuid:public_id>",
    #     views.Courses_SectionDetailsView.as_view(),
    # ),
    # path(
    #     "lesson_materials_details/<uuid:public_id>",
    #     views.Lessons_MaterialDetailsView.as_view(),
    # ),
    # path(
    #     "section_lessons_details/<uuid:public_id>",
    #     views.Section_LessonDetailsView.as_view(),
    # ),
    # path("courses_add", views.CoursesAddView.as_view()),
    


    # path("categories", views.Courses_CategoriesView.as_view()),
    # path("categories/<uuid:categories_id>/course", views.CoursesAddView.as_view()),
    # path(
    #     "course/<uuid:course_id>/courses_section",
    #     views.Courses_SectionsView.as_view(),
    # ),
    # path(
    #     "courses_section/<uuid:courses_section_id>/sections_lesson",
    #     views.Section_LessonsView.as_view(),
    # ),
    # path(
    #     "sections_lesson/<uuid:sections_lesson_id>/lessons_materials_list",
    #     views.Lessons_MaterialsView.as_view(),
    # ),

    path(
        "category_details/<uuid:public_id>",
        views.Courses_CategoriesDetailsView.as_view(),
    ),
    path("categories", views.Courses_CategoriesView.as_view()),


    path("categories/<uuid:public_id>/course", views.CoursesFromCategoryView.as_view()),
    path("courses_list", views.CoursesView.as_view()),
    path("course_details/<uuid:public_id>", views.CoursesDetailView.as_view()),


    path(
        "course/<uuid:public_id>/courses_section",
        views.Courses_SectionsFromCourseView.as_view(),
    ),
    path("courses_sections_list", views.Courses_SectionsView.as_view()),
    path(
        "course_section_details/<uuid:public_id>",
        views.Courses_SectionDetailsView.as_view(),
    ),


    path(
        "courses_section/<uuid:public_id>/sections_lesson",
        views.Section_LessonsFromCourseSectionView.as_view(),
    ),
    path(
        "section_lessons_list",
        views.Section_LessonsView.as_view(),
    ),
    path(
        "section_lessons_details/<uuid:public_id>",
        views.Section_LessonDetailsView.as_view(),
    ),


    path(
        "sections_lesson/<uuid:public_id>/lessons_materials",
        views.Lessons_MaterialsFromLessonView.as_view(),
    ),
    path(
        "lessons_materials_list",
        views.Lessons_MaterialsView.as_view(),
    ),
    path(
        "lesson_materials_details/<uuid:public_id>",
        views.Lessons_MaterialDetailsView.as_view(),
    ),
    
]
