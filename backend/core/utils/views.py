from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     permissions = super().get_permissions()
    #     return [permission() for permission in self.permission_classes]
    #     # return super().get_permissions()

    def handle_response(self, data, status_code) -> HttpResponse:
        return Response(data, status=status_code)

    def created_response(self, data) -> HttpResponse:
        return Response(
            {"status": "success", "message": "Successfully deleted", "details": data},
            status=status.HTTP_200_OK,
        )

    def delete_response(self, data) -> HttpResponse:
        return Response(
            {"status": "success", "message": "Successfully deleted", "details": data},
            status=status.HTTP_200_OK,
        )

class AbstractApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    # foreign_model = None
    state_model = None
    # foreign_model = None
    serializer_class = None

    # def get_object(self, public_id):
    #     try:
    #         return self.foreign_model.objects.get(public_id=public_id)
    #     except:
    #         return None

    def get(self, request):
        
        courses_object = self.state_model.objects.all()
        paginator = Paginator(courses_object, 10)
        page = request.GET.get('page')
        try:
            courses_page_object = paginator.page(page)
        except PageNotAnInteger:
            courses_page_object = paginator.page(1)
        except EmptyPage:
            courses_page_object = paginator.page(paginator.num_pages)

        serializer = self.serializer_class(courses_page_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # if public_id:
        #     try:
        #         foreign_object = self.get_object(public_id=public_id)
        #         request.data['category'] = foreign_object.id
        #     except:
        #         raise Http404
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AbstractGetApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = None
    serializer_class = None

    def get(self, request):
        courses_object = self.state_model.objects.all()
        paginator = Paginator(courses_object, 5)
        page = request.GET.get('page')
        try:
            courses_page_object = paginator.page(page)
        except PageNotAnInteger:
            courses_page_object = paginator.page(1)
        except EmptyPage:
            courses_page_object = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(courses_page_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class AbstractPostApiView(APIView):

#     permission_classes = [permissions.IsAuthenticated]
#     state_model = None
#     foreign_model = None
#     serializer_class = None

#     def get_object(self, public_id):
#         try:
#             return self.foreign_model.objects.get(public_id=public_id)
#         except:
#             return None

#     def post(self, request, public_id = None):

#         if public_id:
#             try:
#                 foreign_object = self.get_object(public_id=public_id)
#                 request.data['category'] = foreign_object.id
#             except:
#                 raise Http404
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbstractApiViewDetails(APIView):

    permission_classes = [permissions.IsAuthenticated]
    state_model = None
    serializer_class = None
    foreign_model = None
    foreign_key = None

    def get_object(self, public_id):
        try:
            return self.state_model.objects.get(public_id=public_id)
        except self.state_model.DoesNotExist:
            raise Http404
        
    def get_foreign_object_by_public_id(self, public_id=None):
        try:
            return self.foreign_model.objects.get(public_id=public_id)
        except:
            return None

    def get(self, request, public_id):
        course_object = self.get_object(public_id)
        serializer = self.serializer_class(course_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, public_id):
        try:
            if request.data[self.foreign_key]:
                try:
                    foreign_object = self.get_foreign_object_by_public_id(request.data[self.foreign_key])
                    request.data[self.foreign_key] = foreign_object.id
                except:
                    raise Http404
        except:
            pass
        course_object = self.get_object(public_id)
        serializer = self.serializer_class(course_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, public_id):
        course_object = self.get_object(public_id)
        course_object.delete()
        return Response(status=status.HTTP_200_OK)
