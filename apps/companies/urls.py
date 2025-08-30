from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # Company endpoints
    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    
    # Department endpoints
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    
    # Employee endpoints
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/profile/', views.EmployeeProfileView.as_view(), name='employee-profile'),
    
    # Project endpoints
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    
    # Performance Review endpoints
    path('performance-reviews/', views.PerformanceReviewListView.as_view(), name='performance-review-list'),
    path('performance-reviews/<int:pk>/', views.PerformanceReviewDetailView.as_view(), name='performance-review-detail'),
    path('performance-reviews/<int:pk>/transition/', views.PerformanceReviewTransitionView.as_view(), name='performance-review-transition'),
]
