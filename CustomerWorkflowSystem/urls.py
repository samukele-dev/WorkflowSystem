from django.urls import path, include
from .views import capture_customer_info, render_temporal_graph


urlpatterns = [
    path('', capture_customer_info, name='capture_customer'),  # Add this line for the empty path
    path('capture/', capture_customer_info, name='capture_customer'),
    path('graph/<int:customer_id>/', render_temporal_graph, name='temporal_graph'),
]
