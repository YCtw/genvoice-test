👉 Features<br />
📑Clinician Management
- Register a new clinician (/register)
- Login as a clinician (/login)
- Promote (/promote) or demote (/demote) clinicians

📑Case Management
- View all cases (/cases)
- Add a new case (/case)

👉 URL: Request & Response Mapping<br />

💻 Root Endpoint<br />
GET /<br />
Response: "API for GenVoice -> Entrance point"<br />

💻 Register Clinician<br />
POST /register<br />
Request Body:<br />
{<br />
  "name": Clinician full name,<br />
  "user_name": Clinician user name,<br />
  "pwd": Clinician password<br />
}

Success Response (200 OK)<br />
{<br />
  "message": "User registered successfully"<br />
}<br />

Error Responses:<br />
(400 Bad Request) → Missing fields<br />
{<br /> 
    "error": "Missing required columns: name, username, password"<br /> 
}<br />
409 Conflict → Username already exists<br />
{<br />
    "error": "Username has already been taken"<br />
}<br />

💻 Login Clinician<br />
POST /login<br />
Request Body:<br />
{<br />
  "user_name": Clinician user name,<br />
  "pwd": Clinician password<br />
}

Success Response (200 OK)<br />
{<br />
  "message": "Login successful, role: {clinician.role}"<br />
}<br />

Error Responses:<br />
(400 Bad Request) → Missing fields<br />
{<br /> 
    "error": "Missing required columns: username, pwd"<br /> 
}<br />
404 Not Found → User not found<br />
{<br />
    "error": "Username not existed, you should register first"<br />
}<br />
401 Unauthorized → Incorrect password<br />
{<br />
    "error": "Incorrect password"<br />
}<br />

💻 Promote Clinician /><br />
POST /promote<br />
Request Body:<br />
{<br />
  "id": 1 (Clinician id) <br />
}

Success Response (200 OK)<br />
{<br />
  "message": "User promoted to Senior"<br />
}<br />

Error Responses:<br />
404 Not Found → User not found<br />
{<br />
    "error": "User id not existed"<br />
}<br />
409 Conflict → Already Senior<br />
{<br />
    "error": "User has already been Senior"<br />
}<br />

💻 Demote Clinician /><br />
POST /demote<br />
Request Body:<br />
{<br />
  "id": 1 (Clinician id) <br />
}

Success Response (200 OK)<br />
{<br />
  "message": "User demoted to Junior"<br />
}<br />

Error Responses:<br />
404 Not Found → User not found<br />
{<br />
    "error": "User id not existed"<br />
}<br />
409 Conflict → Already Junior<br />
{<br />
    "error": "User has already been Junior"<br />
}<br />

💻 View all cases /><br />
GET /cases<br />

Success Response (200 OK)<br /><br />
{<br />
  "cases": [<br />
      {"id": 1,<br />
      "name": "Case1 full name",<br />
      "description": "Description of case1"<br />
    }<br />,
      {"id": 2,<br />
      "name": "Case2 full name",<br />
      "description": "Description of case2"<br />
    }<br />
  ]<br />
}

💻 Add a case /><br />
POST /case<br />
Request Body:<br />
{<br />
  "name": Case name, <br />
  "description": Description of the case's situation.<br />
}<br />
}<br />

Success Response (200 OK)<br />
{<br />
  "message": "Case added successfully"<br />
}<br />

Error Responses:<br />
400 Bad Request → Missing fields<br />
{<br />
    "error": "Missing required columns: name, description"<br />
}<br />



