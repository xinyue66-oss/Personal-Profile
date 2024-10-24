import os, hashlib, json
from warnings import catch_warnings

from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.utils import timezone
from app import models

def register(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    name = request.POST.get('name')
    email = request.POST.get('email')
    handle = request.POST.get('handle')
    password = request.POST.get('password')
    biometrics = request.POST.get('biometrics')
    public_private_key_pair = request.POST.get('public_private_key_pair')
    if not email or not password:
        return JsonResponse({'status':'email and password must exist!'})
    user = models.Users.objects.filter(email=email).first()
    if user:
        return JsonResponse({'status':'the email exists!'})
    user = models.Users(name=name, email=email, handle=handle, password_hash=password,
        biometrics=biometrics, public_private_key_pair=public_private_key_pair)
    user.save()
    token = models.Token(user_id=user.user_id, token=hashlib.md5(os.urandom(32)).hexdigest(),
                        expired_at=timezone.now()+timezone.timedelta(days=1))
    token.save()
    data = request.POST.get('data')
    if not data:
        data = '{}'
    profile = models.Profiles(user_id=user.user_id, data=data)
    profile.save()

    return JsonResponse({'user_id':user.user_id, 'token':token.token,
            'profile_id':profile.profile_id, 'status':'success'})

def add_credential(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        credential_type = request.POST.get('credential_type')
        credential_image = request.POST.get('credential_image')
        if not credential_type or not credential_image:
            return JsonResponse({'status':'credential_type,credential_image must exist!'})
        credential = models.Credential(user_id=token.user_id,
            credential_type=credential_type, credential_image=credential_image)
        credential.save()
        return JsonResponse({'credential_id':credential.credential_id, 'status':'success'})

def share_create(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        service_id = request.POST.get('service_id')
        info_field = request.POST.get('info_field')
        if not service_id or not info_field:
            return JsonResponse({'status':'service_id,info_field must exist!'})
        verification_token = hashlib.md5(os.urandom(32)).hexdigest()
        expires_at = timezone.now() + timezone.timedelta(days=7)
        share = models.SharedInfo(user_id=token.user_id, service_id=service_id,
            info_field=info_field, verification_token=verification_token,
            expires_at=expires_at)
        share.save()
        return JsonResponse({'verification_token':verification_token, 'status':'success'})

def get_share(request):
    if request.method != 'GET':
        return JsonResponse({'status':'get required'})
    token = request.GET.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        service_id = request.GET.get('service_id')
        verification_token = request.GET.get('verification_token')
        if not service_id or not verification_token:
            return JsonResponse({'status':'service_id,verification_token must exist!'})
        share = models.SharedInfo.objects.filter(user_id=token.user_id,
                service_id=service_id, verification_token=verification_token,
                expires_at__gte=timezone.now()).first()
        if not share:
            return JsonResponse({'status':'this user hasn’t agreed to share information!'})
        else:
            share = models.SharedInfo.objects.filter(user_id=token.user_id).order_by('-shared_at').first()
            if not share:
                return JsonResponse({'status':'this user does not exsit!'})
            else:
                return JsonResponse({'user_data':share.info_field, 'status':'success'})

def emergency_access(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        info_field = request.POST.get('info_field')
        trusted_contacts = request.POST.get('trusted_contacts')
        emergency_info = request.POST.get('emergency_info')
        criteria = request.POST.get('criteria')
        if not info_field:
            return JsonResponse({'status':'info_field must exist!'})
        access = models.EmergencyAccess.objects.filter(user_id=token.user_id).first()
        if not access:
            access = models.EmergencyAccess(user_id=token.user_id,
                trusted_contacts=trusted_contacts,
                emergency_info=emergency_info, criteria=criteria)
        else:
            access.trusted_contacts = trusted_contacts
            access.emergency_info = emergency_info
            access.criteria = criteria
            access.updated_at = timezone.now()
        access.save()
        return JsonResponse({'access_id':access.access_id, 'status':'success'})

########################################
####Defined by Gloria on Oct 07, 2024###
########################################
def emergency_access_grant(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    responder_id = request.POST.get('responder_id')
    reason = request.POST.get('reason')
    email = request.POST.get('email')
    if not responder_id or not reason or not email:
        return JsonResponse({'status':'responder_id,reason,email must exist!'})
    user = models.Users.objects.filter(email=email).first()
    if not user:
        return JsonResponse({'status':'email must exist!'})
    user_id = user.user_id
    log = models.EmergencyAccessLog(user_id=user_id, responder_id=responder_id,
            reason=reason, access_time=timezone.now())
    log.save()
    access = models.EmergencyAccess.objects.filter(user_id=user_id).first()
    if not access:
        return JsonResponse({'status':'this user hasn’t set emergency access!'})
    emergency_info = access.emergency_info
    return JsonResponse({'emergency_info':emergency_info, 'status':'success'})

def privilege_rings(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        ring_name = request.POST.get('ring_name')
        assigned_data = request.POST.get('assigned_data')
        if not ring_name or not assigned_data:
            return JsonResponse({'status':'assigned_data must exist!'})
        if not ring_name in {'public', 'semi-private', 'private', 'restricted'}:
            return JsonResponse({'status':'ring_name value must in public, semi-private, private, restricted!'})
        user = models.Users.objects.filter(user_id=token.user_id).order_by('-updated_at').first()
        if not user:
            return JsonResponse({'status':'this user does not exsit!'})
        ring = models.PrivilegeRings(user_id=token.user_id, ring_name=ring_name,
                assigned_data=assigned_data)
        ring.save()
        ring_id = ring.ring_id
        return JsonResponse({'ring_id':ring_id, 'status':'success'})

def update_info(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    queryDict = QueryDict(request.body)
    token = queryDict.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        updated_fields = queryDict.get('updated_fields')
        if not updated_fields:
            return JsonResponse({'status':'updated_fields must exist!'})
        profile = models.Profiles.objects.filter(user_id=token.user_id).first()
        if not profile:
            return JsonResponse({'status':'this user’s profile does not exsit!'})
        try:
            updated_fields = json.loads(updated_fields)
        except:
                return JsonResponse({'status':' Json Decode Error!'})
        profile.data = updated_fields
        profile.save()
        return JsonResponse({'status': 'success'})

def revoke_access(request):
    if request.method != 'DELETE':
        return JsonResponse({'status':'delete required'})
    queryDict = QueryDict(request.body)
    token = queryDict.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        service_id = queryDict.get('service_id')
        if not service_id:
            return JsonResponse({'status':'service_id must exist!'})
        records = models.SharedInfo.objects.filter(user_id=token.user_id,
                    service_id=service_id, expires_at__gt=timezone.now())
        for record in records:
            record.expires_at = timezone.now()
            record.save()
        return JsonResponse({'status':'success'})

def share_create_link(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        doctor_email = request.POST.get('doctor_email')
        expiration_date = request.POST.get('expiration_date')
        health_records_info = request.POST.get('health_records_info')
        if not doctor_email or not expiration_date or not health_records_info:
            return JsonResponse({'status':'doctor_email, expiration_date, health_records_info must exist!'})
        access_link = hashlib.md5(os.urandom(32)).hexdigest()
        record = models.ShareHealthRecords(user_id=token.user_id,
                    health_records_info=health_records_info, access_link=access_link,
                    expiration_date=expiration_date)
        record.save()
        return JsonResponse({'access_link':access_link, 'status':'success'})

def public(request):
    if request.method != 'POST':
        return JsonResponse({'status':'post required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        public_info = request.POST.get('public_info')
        visibility = request.POST.get('visibility')
        if not public_info or not visibility:
            return JsonResponse({'status':'public_info,visibility must exist!'})
        public_profile_link = hashlib.md5(os.urandom(32)).hexdigest()
        profile = models.PublicProfiles(user_id=token.user_id,
                public_info=public_info, visibility=visibility,
                public_profile_link=public_profile_link)
        profile.save()
        return JsonResponse({'public_profile_link':public_profile_link, 'status':'success'})

def export(request):
    if request.method != 'POST':
        return JsonResponse({'status':'put required'})
    token = request.POST.get('token')
    token = models.Token.objects.filter(token=token).first()
    if not token:
        return JsonResponse({'status':'token must exist!'})
    elif token.expired_at <= timezone.now():
        token.token = hashlib.md5(os.urandom(32)).hexdigest()
        token.expired_at = timezone.now() + timezone.timedelta(days=1)
        token.save()
        return JsonResponse({'status':'token has expired!'})
    else:
        p = models.Profiles.objects.filter(user_id=token.user_id).order_by('-updated_at').first()
        data = p.data
        exported_data = {'profile_id':p.profile_id, 'user_id':p.user.user_id,
                         'data':data, 'created_at':p.created_at.strftime('%Y-%m-%d %H:%M'),
                         'updated_at':p.updated_at.strftime('%Y-%m-%d %H:%M')}
        log = models.ExportLogs(user_id=token.user_id, export_format='json',
                export_time=timezone.now(), exported_data=json.dumps(exported_data))
        log.save()
        return JsonResponse({'exported_data':exported_data, 'status':'success'})
