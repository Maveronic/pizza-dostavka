from django.urls import path
from orders.views import OrderCreateListView, OrderDetailView, UpdateOrderStatusView, UserOrdersView, UserOrderDetail

urlpatterns = [
    path('', OrderCreateListView.as_view(), name='orders'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('update-status/<int:order_id>/', UpdateOrderStatusView.as_view(), name='order-update'),
    path('user/<int:user_id>/orders/', UserOrdersView.as_view(), name='users-orders'),
    path('user/<int:user_id>/orders/<int:order_id>/', UserOrderDetail.as_view(), name='user-specific-detail')

]
