from model_bakery import baker

# category = baker.make('courses.Courses_Categories')

# course = baker.make('courses.Courses')

# course = baker.make('courses.Courses', _quantity=5)
# assert len(course) == 5

"""Добавление 5 записей в таблицу материалов уроков, а также остальных связанных таблиц (по 1 связ записи в каждой таблице)"""
lesson_material = baker.make('courses.Lessons_Materials', _quantity=5)
assert len(lesson_material) == 5

"""Добавление 3 курсов для категории с id 30"""
# course = baker.make(
#         'courses.Courses',
#         category__id = 30,
#         category__created = dt.now(),
#         _quantity=3
#         ) 
# assert len(course) == 3