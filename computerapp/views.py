from django.shortcuts import render
from .models import Product, UserProfile, DeliveryAddress, Order
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ProductListSerializer, ProductRetrieveSerializer, UserInfoSerializer, \
    UserProfileSerializer, DeliverAddressSerializer, OrderListSerializer, OrderCreateViewSerializer,\
    OrderRUDSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)  # 访问控制
    filter_backends = (SearchFilter, OrderingFilter,)  # 过滤-后端
    search_fields = ("description", "model")  # 搜索功能
    ordering_fields = ("category", "manufacturer", "created", "sold",)  # 排序功能
    ordering = ("id",)  # 默认排序
    pagination_class = LimitOffsetPagination  # 分页功能


class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = (permissions.AllowAny,)  # 加括号


class ProductListByCategoryView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("description", "model")
    ordering_fields = ("category", "manufacturer", "created", "sold", "stock", "price")
    ordering = ("id",)

    def get_queryset(self):
        category = self.request.query_params.get("category", None)
        if category:
            queryset = Product.objects.filter(category=category)
        else:
            queryset = Product.objects.all()
        return queryset


class ProductListByCategoryManufacturerView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("description", "model")
    ordering_fields = ("category", "manufacturer", "created", "sold", "stock", "price")
    ordering = ("id",)

    # pagination_class = LimitOffsetPagination
    def get_queryset(self):  # 列表传get_object
        category = self.request.query_params.get("category", None)  # query_params等于request.GET
        manufacturer = self.request.query_params.get("manufacturer", None)
        if category is not None:
            queryset = Product.objects.filter(category=category, manufacturer=manufacturer)
        else:
            queryset = Product.objects.all()
        return queryset


class UserInfoView(APIView):  # 使用当前的用户、商品等用这种方法
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user  # 获取当前用户
        serializer = UserInfoSerializer(user)  # 格式转换成字典
        return Response(serializer.data)


# class UserInfoView(generics.RetrieveAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = UserInfoSerializer
#     def get_object(self): #详情传get_object
#         user = self.request.user
#         obj = User.objects.get(id=user.id)#get的参数只能是对象里的一个值，不能是整个对象
#         return obj
class UserProfileRUView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):  # 详情传get_object
        user = self.request.user
        obj = UserProfile.objects.get(user=user)  # 这里的user虽然是对象，但在UserProfile里是值
        return obj


class DeliverAddressLCView(generics.ListCreateAPIView):
    serializer_class = DeliverAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # 查询所有，List功能
        user = self.request.user
        queryset = DeliveryAddress.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):  # create功能
        user = self.request.user
        # 执行并返回序列器执行后的对象
        s = serializer.save(user=user)
        # 修改用户默认地址
        profile = user.profile_of  # 获取档案对象
        profile.delivery_address = s  # 再次强调，ForenginKey存储的是一个对象
        profile.save()


class DeliverAddressRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeliverAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):  # 详情传get_object
        user = self.request.user
        try:
            obj = DeliveryAddress.objects.get(id=self.kwargs["pk"], user=user)
            # self.kwargs["pk"]用来获取url里关键字参数，参数名在后端urls文件里定义
            # self.request.query_params用来获取url里键值对参数，参数名在前端url里定义
        except Exception as e:
            raise NotFound("not found")
        return obj


# class CartListView(generics.ListAPIView):
#     serializer_class = OrderListSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Order.objects.filter(user =user ,status = "0")
#         return queryset
class CartListView(generics.ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status="0")
        return queryset


# def OrderDetail(request,pk):
#     obj = Order.objects.get(pk=pk)
#     obj.status = "1"
#     obj.save()
#     return HttpResponseRedirect(reverse("computerapp:order_list"))
class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status__in=["1", "2", "3", "4"])
        return queryset


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateViewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get("product")
        serializer.save(user=user, price=product.price, address=self.request.user.profile_of.delivery_address)

class OrderRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderRUDSerializer
    queryset = Order.objects.all()
    def get_object(self):
        user = self.request.user
        obj = Order.objects.filter(pk=self.kwargs['pk'],user=user)[0]
        return obj
    def perform_update(self, serializer):
        user = self.request.user
        # obj = Order.objects.filter(pk=self.kwargs['pk'], user=user)[0]
        # obj.status="1"
        # obj.save()
        serializer.save(user =user,status = "1")
    def perform_destroy(self, instance):
        user = self.request.user
        obj = Order.objects.filter(pk=self.kwargs['pk'], user=user)[0]
        obj.delete()


# class UserCreateView(generics.CreateAPIView):
#     serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

























