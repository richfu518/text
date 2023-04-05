from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Asset, AssetLog, Employee, AssetLending, AuditLog, SoftwareLicense
from .forms import AssetLogForm, EmployeeForm, AssetAssignForm, AssetLendingForm, SoftwareLicenseForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
from django.contrib.auth.views import LoginView

class AssetListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Asset
    template_name = 'asset_management/asset_list.html'
    context_object_name = 'assets'

    def test_func(self):
        return self.request.user.has_perm('asset_management.view_asset')

class AssetDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Asset
    template_name = 'asset_management/asset_detail.html'

    def test_func(self):
        return self.request.user.has_perm('asset_management.view_asset')

class AssetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Asset
    template_name = 'asset_management/asset_form.html'
    fields = ['name', 'asset_type', 'purchase_date', 'value', 'description', 'acquisition_date', 'category', 'status','image']

    def test_func(self):
        return self.request.user.has_perm('asset_management.add_asset')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AssetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Asset
    template_name = 'asset_management/asset_form.html'
    fields = ['name', 'asset_type', 'purchase_date', 'value', 'description', 'acquisition_date', 'category', 'status','image']

    def test_func(self):
        return self.request.user.has_perm('asset_management.change_asset')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AssetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Asset
    template_name = 'asset_management/asset_confirm_delete.html'
    success_url = reverse_lazy('assets:asset_list')

    def test_func(self):
        return self.request.user.has_perm('asset_management.delete_asset')

class AssetLogListView(ListView):
    model = AssetLog
    template_name = 'asset_managemen/asset_log_list.html'
    context_object_name = 'asset_logs'

class AssetLogCreateView(CreateView):
    model = AssetLog
    template_name = 'asset_managemen/asset_log_form.html'
    form_class = AssetLogForm

class AssetLogUpdateView(UpdateView):
    model = AssetLog
    template_name = 'asset_managemen/asset_log_form.html'
    form_class = AssetLogForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('assets:asset_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def asset_log_list(request):
    logs = AssetLog.objects.all()
    return render(request, 'asset_management/asset_log_list.html', {'logs': logs})

@login_required
def asset_log_create(request):
    if request.method == 'POST':
        form = AssetLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('assets:asset_log_list')
    else:
        form = AssetLogForm()
    return render(request, 'asset_management/asset_log_form.html', {'form': form})

@login_required
def asset_log_edit(request, pk):
    log = get_object_or_404(AssetLog, pk=pk)
    if request.method == 'POST':
        form = AssetLogForm(request.POST, instance=log)
        if form.is_valid():
            log = form.save()
            return redirect('assets:asset_log_list')
    else:
        form = AssetLogForm(instance=log)
    return render(request, 'asset_management/asset_log_form.html', {'form': form})

def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_add.html', {'form': form})

def employee_edit(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_edit.html', {'form': form, 'employee': employee})

def employee_list(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'employee_list.html', context)

def asset_assign(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetAssignForm(request.POST)
        if form.is_valid():
            asset_assignment = form.save(commit=False)
            asset_assignment.asset = asset
            asset_assignment.employee = form.cleaned_data['employee']
            asset_assignment.assigned_date = form.cleaned_data['assigned_date']
            asset_assignment.returned_date = form.cleaned_data['returned_date']
            asset_assignment.save()
            return redirect('assets:asset_list')
    else:
        form = AssetAssignForm()
    return render(request, 'assets/asset_assign.html', {'asset': asset, 'form': form})

@login_required
def asset_report(request):
    total_assets = Asset.objects.count()
    assigned_assets = AssetLog.objects.filter(return_status=False).count()
    returned_assets = AssetLog.objects.filter(return_status=True).count()
    scrapped_assets = Asset.objects.filter(is_scrapped=True).count()

    context = {
        'total_assets': total_assets,
        'assigned_assets': assigned_assets,
        'returned_assets': returned_assets,
        'scrapped_assets': scrapped_assets,
    }
    return render(request, 'asset_management/asset_report.html', context)

def asset_lending(request):
    if request.method == 'POST':
        form = AssetLendingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_lending_list')
    else:
        form = AssetLendingForm()
    return render(request, 'asset_management/asset_lending.html', {'form': form})

def asset_lending_list(request):
    lendings = AssetLending.objects.all()
    return render(request, 'asset_management/asset_lending_list.html', {'lendings': lendings})

@login_required
def audit_log(request):
    logs = AuditLog.objects.all()
    return render(request, 'asset_management/audit_log.html', {'logs': logs})

def asset_report_data(request):
    asset_count = Asset.objects.count()
    context = {
        'asset_count': asset_count,
    }
    return render(request, 'asset_management/asset_report_data.html', context)

def software_license_list(request):
    licenses = SoftwareLicense.objects.all()
    return render(request, 'asset_management/software_license_list.html', {'licenses': licenses})

def software_license_create(request):
    if request.method == 'POST':
        form = SoftwareLicenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('software_license_list')
    else:
        form = SoftwareLicenseForm()
    return render(request, 'asset_management/software_license_form.html', {'form': form})

def software_license_update(request, pk):
    license = SoftwareLicense.objects.get(pk=pk)
    if request.method == 'POST':
        form = SoftwareLicenseForm(request.POST, instance=license)
        if form.is_valid():
            form.save()
            return redirect('software_license_list')
    else:
        form = SoftwareLicenseForm(instance=license)
    return render(request, 'asset_management/software_license_form.html', {'form': form})

def software_license_delete(request, pk):
    license = get_object_or_404(SoftwareLicense, pk=pk)
    if request.method == 'POST':
        license.delete()
        return redirect('software_license_list')
    return render(request, 'software_license_delete_confirm.html', {'license': license})

def software_license_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        licenses = SoftwareLicense.objects.filter(
            Q(name__icontains=search_query) | Q(vendor__icontains=search_query)
        )
    else:
        licenses = SoftwareLicense.objects.all()
    return render(request, 'software_license_list.html', {'licenses': licenses})

from .forms import SoftwareLicenseForm, LicenseAttachmentForm

def software_license_detail(request, pk):
    license = get_object_or_404(SoftwareLicense, pk=pk)
    attachments = license.licenseattachment_set.all()

    if request.method == 'POST':
        form = LicenseAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.license = license
            attachment.uploaded_by = request.user
            attachment.save()
            return redirect('software_license_detail', pk=pk)
    else:
        form = LicenseAttachmentForm()

    return render(request, 'software_license_detail.html', {'license': license, 'attachments': attachments, 'form': form})