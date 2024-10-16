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
POST http://127.0.0.1:8000/api/v1/users/register?email=2393573104@qq.com&password=123&name=xinyue  

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
users、token    


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
POST http://127.0.0.1:8000/api/v1/profile/add-credential?token&credential_type=Driver's License&credential_image  

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
credential    


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
credential  

