import pytest
import requests, time

URL = 'http://127.0.0.1:8000/api/v1'

@pytest.fixture(scope='session')
def email():
    return  f"test_{int(time.time()*1000)}@g.com"

@pytest.fixture(scope='session')
def token(email):
    return requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","email":email,"password":"p","biometrics":"b","public_private_key_pair":"p"}).json()['token']

@pytest.fixture(scope='session')
def vtoken(token):
    return requests.post(f'{URL}/profile/share-create', data={"token":token,"service_id":"s","info_field":"i"}).json()['verification_token']

class TestRegister():
    def test_without_email(self):
        res = requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","password":"p","biometrics":"b","public_private_key_pair":"p"}).json()
        assert res['status'] == 'email and password must exist!'
    def test_without_password(self):
        res = requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","email":"e@g.com","biometrics":"b","public_private_key_pair":"p"}).json()
        assert res['status'] == 'email and password must exist!'
    def test_email_exists(self):
        requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","email":"test@g.com","password":"p","biometrics":"b","public_private_key_pair":"p"})
        res = requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","email":"test@g.com","password":"p","biometrics":"b","public_private_key_pair":"p"}).json()
        assert res['status'] == 'the email exists!'
    def test_register(self):
        res = requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","email":f"test_{int(time.time()*1000)}@g.com","password":"p","biometrics":"b","public_private_key_pair":"p"}).json()
        assert res['status'] == 'success'

class TestCredential():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/add-credential').json()
        assert res['status'] == 'token must exist!'
    def test_without_credential_type(self, token):
        res = requests.post(f'{URL}/profile/add-credential', data={"token":token,"credential_image":"i"}).json()
        assert res['status'] == 'credential_type,credential_image must exist!'
    def test_without_credential_image(self, token):
        res = requests.post(f'{URL}/profile/add-credential', data={"token":token,"credential_type":"t"}).json()
        assert res['status'] == 'credential_type,credential_image must exist!'
    def test_credential(self, token):
        res = requests.post(f'{URL}/profile/add-credential', data={"token":token,"credential_type":"t","credential_image":"i"}).json()
        assert res['status'] == 'success'

class TestShareCreate():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/share-create').json()
        assert res['status'] == 'token must exist!'
    def test_without_service_id(self, token):
        res = requests.post(f'{URL}/profile/share-create', data={"token":token,"info_field":"i"}).json()
        assert res['status'] == 'service_id,info_field must exist!'
    def test_without_info_field(self, token):
        res = requests.post(f'{URL}/profile/share-create', data={"token":token,"service_id":"s"}).json()
        assert res['status'] == 'service_id,info_field must exist!'
    def test_share_create(self, token):
        res = requests.post(f'{URL}/profile/share-create', data={"token":token,"service_id":"s","info_field":"i"}).json()
        assert res['status'] == 'success'

class TestGetShare():
    def test_without_token(self):
        res = requests.get(f'{URL}/profile/get-share').json()
        assert res['status'] == 'token must exist!'
    def test_without_verification_token(self, token):
        res = requests.get(f'{URL}/profile/get-share', params={"token":token,"service_id":'s'}).json()
        assert res['status'] == 'service_id,verification_token must exist!'
    def test_without_service_id(self, token, vtoken):
        res = requests.get(f'{URL}/profile/get-share', params={"token":token,"verification_token":vtoken}).json()
        assert res['status'] == 'service_id,verification_token must exist!'
    def test_share_not_exists(self, token, vtoken):
        res = requests.get(f'{URL}/profile/get-share', params={"token":token,"service_id":"a","verification_token":vtoken}).json()
        assert res['status'] == 'this user hasn’t agreed to share information!'
    def test_get_share(self, token, vtoken):
        res = requests.get(f'{URL}/profile/get-share', params={"token":token,"service_id":"s","verification_token":vtoken}).json()
        assert res['status'] == 'success'

class TestEmergencyAccess():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/emergency-access').json()
        assert res['status'] == 'token must exist!'
    def test_without_info_field(self, token):
        res = requests.post(f'{URL}/profile/emergency-access', data={"token":token,"trusted_contacts":'t',"emergency_info":"e","criteria":"c"}).json()
        assert res['status'] == 'info_field must exist!'
    def test_emergency_access(self, token):
        res = requests.post(f'{URL}/profile/emergency-access', data={"token":token,"info_field":"i","trusted_contacts":'t',"emergency_info":"e","criteria":"c"}).json()
        assert res['status'] == 'success'

class TestEmergencyAccessGrant():
    def test_without_responder_id(self):
        res = requests.post(f'{URL}/profile/emergency-access/grant', data={"reason":"r","email":"g@g.com"}).json()
        assert res['status'] == 'responder_id,reason,email must exist!'
    def test_without_reason(self):
        res = requests.post(f'{URL}/profile/emergency-access/grant', data={"responder_id":"r","email":"g@g.com"}).json()
        assert res['status'] == 'responder_id,reason,email must exist!'
    def test_without_email(self):
        res = requests.post(f'{URL}/profile/emergency-access/grant', data={"responder_id":"r","reason":"r"}).json()
        assert res['status'] == 'responder_id,reason,email must exist!'
    def test_email_not_exists(self):
        res = requests.post(f'{URL}/profile/emergency-access/grant', data={"responder_id":"r","reason":"r","email":f"test_{int(time.time()*1000)}@g.com"}).json()
        assert res['status'] == 'email must exist!'
    def test_access_not_set(self):
        email = f"test_{int(time.time()*1000)+1}@g.com"
        requests.post(f'{URL}/users/register', data={"name":"n","handle":"h","email":email,"password":"p","biometrics":"b","public_private_key_pair":"p"})
        res = requests.post(f'{URL}/profile/emergency-access/grant', data={"responder_id":"r","reason":"r","email":email}).json()
        assert res['status'] == 'this user hasn’t set emergency access!'

def test_emergency_access_grant(email, token):
    requests.post(f'{URL}/profile/emergency-access', data={"token":token,"info_field":"i","trusted_contacts":'t',"emergency_info":"e","criteria":"c"})
    res = requests.post(f'{URL}/profile/emergency-access/grant', data={"responder_id":"r","reason":"r","email":email}).json()
    assert res['status'] == 'success'

class TestPrivilegeRings():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/privilege-rings', data={"ring_name":"r","assigned_data":"a"}).json()
        assert res['status'] == 'token must exist!'
    def test_without_ring_name(self, token):
        res = requests.post(f'{URL}/profile/privilege-rings', data={"token":token,"assigned_data":"a"}).json()
        assert res['status'] == 'assigned_data must exist!'
    def test_without_assigned_data(self, token):
        res = requests.post(f'{URL}/profile/privilege-rings', data={"token":token,"ring_name":"r"}).json()
        assert res['status'] == 'assigned_data must exist!'
    def test_without_ring_name_error(self, token):
        res = requests.post(f'{URL}/profile/privilege-rings', data={"token":token,"ring_name":"r","assigned_data":"a"}).json()
        assert res['status'] == 'ring_name value must in public, semi-private, private, restricted!'
    def test_privilege_rings(self, token):
        res = requests.post(f'{URL}/profile/privilege-rings', data={"token":token,"ring_name":"public","assigned_data":"a"}).json()
        assert res['status'] == 'success'

class TestUpdateInfo():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/update-info').json()
        assert res['status'] == 'token must exist!'
    def test_without_updated_fields(self, token):
        res = requests.post(f'{URL}/profile/update-info', data={"token":token}).json()
        assert res['status'] == 'updated_fields must exist!'
    def test_profile_not_exists(self, token):
        res = requests.post(f'{URL}/profile/update-info', data={"token":token,"updated_fields":"u"}).json()
        assert res['status'] == ' Json Decode Error!'
    def test_update_info(self, token):
        res = requests.post(f'{URL}/profile/update-info', data={"token":token,"updated_fields":"{}"}).json()
        assert res['status'] == 'success'

class TestRevokeAccess():
    def test_without_token(self):
        res = requests.delete(f'{URL}/profile/revoke-access').json()
        assert res['status'] == 'token must exist!'
    def test_without_service_id(self, token):
        res = requests.delete(f'{URL}/profile/revoke-access', data={"token":token}).json()
        assert res['status'] == 'service_id must exist!'
    def test_revoke_access(self, token):
        res = requests.delete(f'{URL}/profile/revoke-access', data={"token":token,"service_id":"s"}).json()
        assert res['status'] == 'success'

class TestShareCreateLink():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/share-create-link').json()
        assert res['status'] == 'token must exist!'
    def test_without_doctor_email(self, token):
        res = requests.post(f'{URL}/profile/share-create-link', data={"token":token,"expiration_date":"e","health_records_info":"h"}).json()
        assert res['status'] == 'doctor_email, expiration_date, health_records_info must exist!'
    def test_without_expiration_date(self, token):
        res = requests.post(f'{URL}/profile/share-create-link', data={"token":token,"doctor_email":"d","health_records_info":"h"}).json()
        assert res['status'] == 'doctor_email, expiration_date, health_records_info must exist!'
    def test_without_health_records_info(self, token):
        res = requests.post(f'{URL}/profile/share-create-link', data={"token":token,"doctor_email":"d","expiration_date":"e"}).json()
        assert res['status'] == 'doctor_email, expiration_date, health_records_info must exist!'
    def test_share_create_link(self, token):
        res = requests.post(f'{URL}/profile/share-create-link', data={"token":token,"doctor_email":"d","expiration_date":"2024-12-30 12:01:01","health_records_info":"h"}).json()
        assert res['status'] == 'success'

class TestPublic():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/public').json()
        assert res['status'] == 'token must exist!'
    def test_without_public_info(self, token):
        res = requests.post(f'{URL}/profile/public', data={"token":token,"visibility":True}).json()
        assert res['status'] == 'public_info,visibility must exist!'
    def test_without_visiblity(self, token):
        res = requests.post(f'{URL}/profile/public', data={"token":token,"public_info":"p"}).json()
        assert res['status'] == 'public_info,visibility must exist!'
    def test_public(self, token):
        res = requests.post(f'{URL}/profile/public', data={"token":token,"public_info":"p","visibility":True}).json()
        assert res['status'] == 'success'

class TestExport():
    def test_without_token(self):
        res = requests.post(f'{URL}/profile/export').json()
        assert res['status'] == 'token must exist!'
    def test_export(self, token):
        res = requests.post(f'{URL}/profile/export', data={"token":token}).json()
        assert res['status'] == 'success'
