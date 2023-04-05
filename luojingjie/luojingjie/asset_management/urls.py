from django.urls import path, include
from . import views
from django.contrib import admin
from .views import CustomLoginView, asset_log_list

app_name = 'assets'

urlpatterns = [
    path('', views.AssetListView.as_view(), name='asset_list'),
    path('asset/<int:pk>/', views.AssetDetailView.as_view(), name='asset_detail'),
    path('asset/add/', views.AssetCreateView.as_view(), name='asset_create'),
    path('asset/<int:pk>/edit/', views.AssetUpdateView.as_view(), name='asset_update'),
    path('asset/<int:pk>/delete/', views.AssetDeleteView.as_view(), name='asset_delete'),

    # 添加新的URL路径
    path('logs/', views.asset_log_list, name='asset_log_list'),
    path('logs/new/', views.asset_log_create, name='asset_log_create'),
    path('logs/edit/<int:pk>/', views.asset_log_edit, name='asset_log_edit'),

    # 添加用户注册 URL
    path('accounts/signup/', views.signup, name='signup'),

    path('employee/', views.employee_list, name='employee_list'),
    path('employee/add/', views.employee_add, name='employee_add'),
    path('employee/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),

    # 添加资产分配 URL
    path('asset/<int:pk>/assign/', views.asset_assign, name='asset_assign'),

    path('report/', views.asset_report, name='asset_report'),

    path('asset/lending/', views.asset_lending, name='asset_lending'),
    path('asset/lending/list/', views.asset_lending_list, name='asset_lending_list'),

    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('audit_log/', views.audit_log, name='audit_log'),
    path('reports/', views.asset_report, name='asset_report'),
    path('reports/data/', views.asset_report_data, name='asset_report_data'),
    path('software_licenses/', views.software_license_list, name='software_license_list'),
    path('software_licenses/create/', views.software_license_create, name='software_license_create'),
    path('software_licenses/update/<int:pk>/', views.software_license_update, name='software_license_update'),
    path('software_licenses/<int:pk>/', views.software_license_detail, name='software_license_detail'),

]