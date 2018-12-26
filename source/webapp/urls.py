from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from webapp.views import FoodDetailView, FoodCreateView, FoodUpdateView, OrderDetailView, OrderCreateView, \
    OrderUpdateView, OrderFoodCreateView, OrderListView, OrderRejectView, OrderDeliverView, \
    FoodDeleteView, OrderFoodUpdateView, FoodListView, OrderFoodDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('food/<int:pk>', FoodDetailView.as_view(), name='food_detail'),
    path('food/create', FoodCreateView.as_view(), name='food_create'),
    path('food/update/<int:pk>', FoodUpdateView.as_view(), name='food_update'),
    path('food/delete/<int:pk>', FoodDeleteView.as_view(), name='food_delete'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/food/create', OrderFoodCreateView.as_view(), name='order_food_create'),
    path('order/<int:pk>/food/update', OrderFoodUpdateView.as_view(), name='order_food_update'),
    path('order/<int:pk>/food/delete', OrderFoodDeleteView.as_view(), name='order_food_delete'),
    path('order/<int:pk>/cancel', OrderRejectView.as_view(), name='reject_order'),
    path('order/<int:pk>/deliver', OrderDeliverView.as_view(), name='order_deliver'),
    path('foods', FoodListView.as_view(), name='food_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)