from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
app_name = "computerapp"
urlpatterns = [
    url(r"^product_list/$",views.ProductListView.as_view(),name="product_list"),
    #详情Retrieve必须加PK
    url(r"^product_retrieve/(?P<pk>\d+)/$",views.ProductRetrieveView.as_view(), name="product_retrieve"),
    url(r"^product_list_by_category/$", views.ProductListByCategoryView.as_view(),
        name="product_list_by_category"),
    url(r"^product_list_by_category_manufacturer/$", views.ProductListByCategoryManufacturerView.as_view(),
        name="product_list_by_category_manufacturer"),
    url(r"^user_info/$",views.UserInfoView.as_view(),name="user_info"),
    url(r"^user_profile_ru/(?P<pk>\d+)/$", views.UserProfileRUView.as_view(), name="user_profile_ru"),
    url(r"^delivery_address_lc/$",views.DeliverAddressLCView.as_view(),name="delivery_address_lc"),
    url(r"^delivery_address_rud/(?P<pk>\d+)/$",views.DeliverAddressRUDView.as_view(),name="delivery_address_rud"),
    url(r"^cart_list/$",views.CartListView.as_view(),name = "cart_list"),
    url(r"^order_rud/(?P<pk>\d+)/$",views.OrderRUDView.as_view(),name = "order_rud"),
    url(r"^order_list/$",views.OrderListView.as_view(),name = "order_list"),
    url(r"^order_create/$",views.OrderCreateView.as_view(),name = "order_create"),
    # url(r"^user_create/$",views.UserCreateView.as_view(),name = "user_create"),
    url(r'^user_create/$', views.UserCreateView.as_view(), name='user_create'),


]
urlpatterns = format_suffix_patterns(urlpatterns,allowed=["api","json",])# 允许访问的接口类型









































