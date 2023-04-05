from django import forms
from .models import Asset, AssetAssignment, Employee, AssetLog, AssetLending, SoftwareLicense, LicenseAttachment


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'category','acquisition_date', 'value', 'category', 'status', 'is_scrapped','owner']

class AssetLogForm(forms.ModelForm):
    class Meta:
        model = AssetLog
        fields = ('asset', 'user', 'issue_date', 'return_date', 'return_status')

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone']

class AssetAssignForm(forms.ModelForm):
    class Meta:
        model = AssetAssignment
        fields = ('employee', 'assigned_date','returned_date')

class AssetLendingForm(forms.ModelForm):
    class Meta:
        model = AssetLending
        fields = ['asset', 'borrower', 'date_borrowed', 'date_returned']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('name', 'category', 'description', 'image')

class SoftwareLicenseForm(forms.ModelForm):
    class Meta:
        model = SoftwareLicense
        fields = ['name', 'license_key', 'purchase_date', 'expiration_date', 'vendor', 'description']

class LicenseAttachmentForm(forms.ModelForm):
    class Meta:
        model = LicenseAttachment
        fields = ['file']