from django.db import models
from django.utils import timezone

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    handle = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    biometrics = models.CharField(max_length=255)
    public_private_key_pair = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Token(models.Model):
    user_id = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField()

class Profiles(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Credential(models.Model):
    credential_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    credential_type = models.CharField(max_length=100)
    credential_image = models.JSONField()
    added_at = models.DateTimeField(auto_now_add=True)

class SharedInfo(models.Model):
    shared_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=255)
    info_field = models.CharField(max_length=100)
    verification_token = models.CharField(max_length=255)
    shared_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

class EmergencyAccess(models.Model):
    access_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    trusted_contacts = models.JSONField()
    emergency_info = models.JSONField()
    criteria = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmergencyAccessLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    responder_id = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    access_time = models.DateTimeField(auto_now=True)

class PrivilegeRings(models.Model):
    ring_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ring_name = models.CharField(max_length=100)
    access_level = models.CharField(max_length=50)
    assigned_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HealthRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=100)
    record_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShareHealthRecords(models.Model):
    share_health_records_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    health_records_info = models.JSONField()
    access_link = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PublicProfiles(models.Model):
    public_profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    public_info = models.JSONField()
    visibility = models.BooleanField(default=True)
    public_profile_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExportLogs(models.Model):
    export_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    export_format = models.CharField(max_length=50)
    export_time = models.DateTimeField(auto_now_add=True)
    exported_data = models.JSONField()