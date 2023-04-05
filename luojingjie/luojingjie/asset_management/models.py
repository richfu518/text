from django.db import models
from django.contrib.auth.models import User

class AssetCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="资产分类名称")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "资产分类"


class AssetStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name="资产状态名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "资产状态"

class Asset(models.Model):
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=100)
    purchase_date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    acquisition_date = models.DateField(verbose_name='采购日期', blank=True, null=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, verbose_name="资产分类")
    status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE, verbose_name="资产状态")
    employee = models.ForeignKey('Employee', null=True, blank=True, on_delete=models.SET_NULL)
    is_scrapped = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="负责人")
    image = models.ImageField(upload_to='assets/', null=True, blank=True)
    class Meta:
        pass
    def __str__(self):
        return self.name

class AssetLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name="资产")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    issue_date = models.DateField(verbose_name="借出日期")
    return_date = models.DateField(null=True, blank=True, verbose_name="归还日期")
    notes = models.TextField(blank=True, verbose_name="备注")
    return_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asset.name} - {self.user.username}"

class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100, default='默认部门')
    position = models.CharField(max_length=100, default='默认职位')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} -> {self.employee.first_name} {self.employee.last_name}"


class AssetLending(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    date_borrowed = models.DateField()
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.asset.name} - {self.borrower.username}'

class AuditLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class SoftwareLicense(models.Model):
    name = models.CharField(max_length=100, verbose_name="软件名称")
    license_key = models.CharField(max_length=255, verbose_name="许可证密钥")
    purchase_date = models.DateField(verbose_name="购买日期")
    expiration_date = models.DateField(verbose_name="到期日期")
    vendor = models.CharField(max_length=100, verbose_name="供应商")
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "软件许可证"

class LicenseAttachment(models.Model):
    license = models.ForeignKey(SoftwareLicense, on_delete=models.CASCADE)
    file = models.FileField(upload_to='license_attachments/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.license.name} - {self.file.name}"