from django.contrib import admin
from .models import AssetCategory, AssetStatus, Asset, Employee, AssetAssignment


class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AssetStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # search_fields = ('name',)

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'purchase_date', 'value', 'category', 'status')
    list_filter = ('asset_type', 'category', 'status')
    search_fields = ('name',)

# 添加一个新的 ModelAdmin 类为 Employee
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position')  # 根据您的需求自定义
    search_fields = ('user__username', 'department', 'position')  # 根据您的需求自定义

class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'assigned_date', 'returned_date')
    list_filter = ('asset', 'employee')

admin.site.register(AssetCategory, AssetCategoryAdmin)
admin.site.register(AssetStatus, AssetStatusAdmin)  # 仅注册 AssetStatus
admin.site.register(Employee, EmployeeAdmin)  # 单独注册 Employee
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetAssignment, AssetAssignmentAdmin)