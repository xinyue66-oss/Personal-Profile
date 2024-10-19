# Personal-Profile
Secure Personal Profile Development

# 项目启动命令：
python3 manage.py makemigrations  
python3 manage.py migrate  
python3 manage.py runserver 0.0.0.0:8000  


# API 1
User Case1: User Registration and Profile Creation
Actor: New User
Description: A new user signs up for the system and creates their Secure Personal Profile.
Steps:
1. User downloads and opens the app
2. User chooses to create a new account
3. User provides basic information (e.g., name, email, handle)
4. User sets up strong authentication (e.g., password, biometrics, public-private key pair)
5. User is prompted to start adding information to their profile
6. System creates a unique, portable digital container for the user’s profile

**request params:**  
○      name: String (User's full name)  
○      email: String (User's email)  
○      handle: String (User's handle)  
○      password: String (Encrypted)  
○      biometrics: String (Encrypted)  
○      public-private key pair: String:(Encrypted)  

**respond params:**
○      user\_id: String (Unique ID for the user)  
○      token(token of user)  
○      profile\_id: String (ID of the created profile)  
○      status: String (Success or error message)  

**request：** 
POST http://127.0.0.1:8000/api/v1/users/register  
<img width="442" alt="截屏2024-10-15 18 41 00" src="https://github.com/user-attachments/assets/a686d1e0-3db9-410b-94c2-86903f6bd1f1">  


**respond：**  
○ success：  
{  
    "user_id": 2,  
    "token": "adbcf08f16f04d7fd79c77ad0e1bd6e8",  
    "profile_id": 2,  
    "status": "success"  
}  

○ fail:  
{  
    "status": "the email exists!"  
}  

**database:**
app_users、app_token      


# API 2
User Case2: Adding Government-Issued Credentials
Actor: Registered User
Description: User adds their driver’s license to their Secure Personal Profile.
Steps:
1. User navigates to the “Add Credential” section
2. User selects “Government ID” and then “Driver’s License”
3. User is prompted to scan or photograph their physical license
4. System extracts and verifies the information
5. User confirms the extracted data
6. System securely stores the credential in the user’s profile

**request params:**  
○	token(token of user)  
○	credential_type: String (e.g., Driver's License)  
○	credential_image: File (Scanned image or photo of the credential)  

**respond params:**
○○	credential_id: String (ID of the added credential)    
○	status: String (Success or error message)  

**request：** 
POST http://127.0.0.1:8000/api/v1/profile/add-credential  
<img width="533" alt="截屏2024-10-15 18 40 38" src="https://github.com/user-attachments/assets/f33aa2a4-1fc0-4477-b660-2e08a8229647">  


**respond：**  
○ success：   
{  
    "credential_id": 1,  
    "status": "success"  
}  

○ fail:  
{  
    "status": "credential_type,credential_image must exist!"  
}  

**database:**  
app_credential      


# API 3  
User Case3: Selective Information Sharing
Actor: User, Third-party Service
Description: User shares only their age from their driver’s license with a third-party service.
Steps:
1. Third-party service requests age verification
2. User receives notification of the request
3. User chooses to share information from their driver’s license
4. User selects only the “Age” field to share
5. System generates a temporary, verifiable credential containing only the age
6. Third-party service receives and verifies the age credential  

**request params:**  
○	token(token of user)  
○	service\_id: String (ID of the requesting third-party service)  
○	info\_field: String (e.g., Age)  

**respond params:**
○	verification\_token: String (Temporary token for the third-party to verify the information)  
○	status: String (Success or error message)  

**request：** 
POST http://127.0.0.1:8000/api/v1/profile/share-create  
<img width="539" alt="截屏2024-10-15 18 39 28" src="https://github.com/user-attachments/assets/c6807b18-67be-4dc2-b336-5af357b30bca">  


**respond：**  
○ success：   
{  
    "verification_token": "079517a38770039662c1006252ae7d50",  
    "status": "success"  
}  

○ fail:  
{  
    "status": "token must exist!"  
}  

**database:**  
app_sharedinfo    


# API 4  
User Case4: Setting Up Emergency Access
Actor: User
Description: User configures the “Break the Glass” feature for emergency situations.
Steps:
1. User navigates to the “Emergency Access” settings
2. User selects information to be accessible in emergencies
3. User defines criteria for emergency access (e.g., unconsciousness)
4. User adds trusted contacts who can trigger emergency access
5. System encrypts and stores the emergency information separately

**request params:**  
○	token(token of user)  
○	trusted_contacts: Array of Strings (List of trusted contacts)  
○	emergency_info: Object (Details of information to be accessible)  
○	criteria: Json(e.g., unconsciousness)  

**respond params:**  
○	access_id: String (ID of the added emergency\_access)  
○	status: String (Success or error message)  

**request：**  
POST http://127.0.0.1:8000/api/v1/profile/emergency-access  
<img width="534" alt="截屏2024-10-15 18 50 42" src="https://github.com/user-attachments/assets/c9147a52-cd7e-4a78-a8b0-aa6eb053b25a">  

**respond：**  
○ success：   
{  
    "access_id": 1,  
    "status": "success"  
}  

○ fail:  
{  
    "status": "token must exist!"  
}  

**database:**  
app_emergencyaccess   


# API 5 
User Case5: Emergency Information Access
Actor: Emergency Responder, System
Description: An emergency responder accesses critical health information during an emergency.
Steps:
1. Emergency responder locates user’s device
2. Responder initiates “Break the Glass” procedure
3. Responder provides their identification and reason for access
4. System verifies the responder’s credentials
5. System grants access to predefined emergency information
6. System logs the access event and notifies user’s emergency contacts  

**request params:**  
○	responder_id: String (ID of the emergency responder)  
○	reason: String (Reason for access request)  
○	email: String (email of the user)  

**respond params:**  
○	emergency_info: Object (Predefined emergency information)  
○	status: String (Success or error message)  

**request：**  
POST http://127.0.0.1:8000/api/v1/profile/emergency-access/grant  
<img width="453" alt="截屏2024-10-15 18 59 24" src="https://github.com/user-attachments/assets/6a382349-9f24-438f-ad82-c86972fc27e6">  

**respond：**  
○ success：   
{  
    "emergency_info": "{HOME:Burnaby 4024}",  
    "status": "success"  
}  

○ fail:  
{  
    "status": "responder_id,reason,email must exist!"  
}  

**database:**  
app_emergencyaccesslog   


# API 6 
User Case6: Configuring Privilege Rings
Actor: User
Description: User sets up different levels of information access for their profile.
Steps:
1. User accesses the “Privacy Settings” section
2. User reviews default privilege rings (public, semi-private, private, restricted)
3. User assigns different types of information to appropriate rings
4. User can create custom rings for specific purposes
5. System applies the configured privacy settings to all stored information
N.B. Here, the use of the term “rings” is from the Operating Systems language. Other terms may
be more helpful.

**request params:**  
○	token(token of user)  
○	assigned_data: Object (Configuration of access levels for various data)  
○	ring_name  

**respond params:**  
○	ring_id(ID of the privilege\_rings)  
○	status: String (Success or error message)  

**request：**  
POST http://127.0.0.1:8000/api/v1/profile/privilege-rings  
<img width="552" alt="截屏2024-10-19 06 35 23" src="https://github.com/user-attachments/assets/6edf176e-4fa4-415b-9af9-bb03cc8ac083">  

**respond：**  
○ success：   
{  
    "ring_id": 1,  
    "status": "success"  
}  

○ fail:    
{  
    "status": "token has expired!"  
}  

**database:**   
app_privilegerings  


# API 7 
User Case7: Updating Personal Information 
Actor: User  
Description: User updates their home address in their profile, all references are updated.  
Steps:  
1. User navigates to the “Personal Information” section  
2. User updates their home address  
3. All documents containing references to the Profile are automatically current  
4. This implies the Documents may have a field saying “ home address”  
5. This Document may retrieve and expose the address only for the Role it was intended for  
N.B. This is a massive Use Case, and probably the most important. With one change, all Government  
and Commercial databases pointing to this profile are updated.  

**request params:**   
○	token(token of user)  
○	updated_fields: Object (Fields to be updated, e.g., home address)  

**respond params:**   
○	status: String (Success or error message)  

**request：**   
POST http://127.0.0.1:8000/api/v1/profile/update-info  
<img width="546" alt="截屏2024-10-19 06 39 49" src="https://github.com/user-attachments/assets/377d475b-b718-48d5-ad1a-807cf93d3913">  

**respond：**   
○ success：    
{   
    "status": "put required"  
}  

○ fail:   
{  
    "status": "token has expired!"  
}  

**database:**    
app_profiles   


# API 8 
User Case8: Revoking Access
Actor: User
Description: User revokes a third-party service’s access to their information.
Steps:
1. User views list of services with access to their information
2. User selects a service to revoke access
3. System displays what information the service currently has access to
4. User confirms revocation of access
5. System updates access permissions and notifies the third-party service
6. The permissions may be identified as the set of Roles belonging to the third party services

**request params:**  
○	token(token of user)   
○	service_id: String (ID of the third-party service)  

**respond params:**   
○	status: String (Success or error message)  

**request：**    
POST http://127.0.0.1:8000/api/v1/profile/revoke-access   
<img width="550" alt="截屏2024-10-19 06 46 13" src="https://github.com/user-attachments/assets/4655c5bd-3398-4209-970e-373e3444877b">  

**respond：**    
○ success：     
{
    "status": "delete required"  
}  

○ fail:   
{  
    "status": "token has expired!"  
}  

**database:**   
app_sharedinfo  


# API 9  
User Case10: Sharing Health Records with a New Doctor
Actor: User, Healthcare Provider
Description: User securely shares relevant health records with a new doctor.
Steps:
1. User receives request for health information from new doctor
2. User accesses their health records in the profile
3. User selects specific records to share or export (e.g., immunizations, allergies)
4. User sets an optional expiration date for the shared information
5. System generates a secure, time-limited access link
6. User sends the access link to the doctor’s verified email
   
**request params:**   
○	token(token of user)  
○	health_records_info: Object (User selects specific records to share)  
○	doctor_email: String (Verified email of the doctor)  
○	expiration_date: Date (Optional expiration date for access)  

**respond params:**    
○	access_link: String (Link to access the health records)  
○	status: String (Success or error message)  

**request：**     
POST http://127.0.0.1:8000/api/v1/profile/share-create-link     
<img width="553" alt="截屏2024-10-19 06 52 17" src="https://github.com/user-attachments/assets/ec674799-9e17-40c3-b345-6b3c30f99d3f">   

**respond：**    
○ success：     
{
    "access_link": "2e05ac0128cffc7f3e49f75e31a1f83f",
    "status": "success"
}

○ fail:   
{  
    "status": "token has expired!"  
}  

**database:**   
app_sharehealthrecords  

