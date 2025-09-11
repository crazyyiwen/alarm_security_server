<picture class="github-only">
  <img alt="Alarm.com Logo" src="https://media.licdn.com/dms/image/v2/C4E0BAQH7Ef_zBPUQnw/company-logo_200_200/company-logo_200_200/0/1631327773224?e=1760572800&v=beta&t=F4eDHsvrfiFP7QhJraL5DjXVaeiKeSSlcwtZ-z8Nt1g" width="40%">
</picture>

<div>
<br>
</div>

## Get started

### Quick start
```
docker pull crazyyiwen/alarm-server:latest
docker run -d -p 8000:8000 --name alarm-server crazyyiwen/alarm-server:latest

docker pull crazyyiwen/alarm-chat-client:latest
docker run -d -p 5173:80 --name alarm-chat-client crazyyiwen/alarm-chat-client:latest
open http://localhost:5173/
```

(Optional)Download and host Docker file - alarm-chat-client and alarm-server:<br>

```
docker build -t alarm-chat-client .
docker run -d -p 5173:80 --name alarm-chat-client alarm-chat-client

docker build -t alarm-server .
docker run -d -p 8000:8000 --name alarm-server alarm-server
```

### Architecture Diagram
<img src="media/Alarm_work_flow.png" width="600">


### Code Structure
<img src="media/Alarm_code_structure.png" width="600">

### Strategy:

** Based on user input, LLM will decide how to route to different node<br>

** Using system prompt to guide LLM to make decision<br>

1.  If the system not armed or disarmed, all users can issue an order without password.

1.  If the system armed, all users must issue an order with password, otherwise, system will deny.

1.  “Arm system“/”Disarm System”/”Door operation(open door)”, please use cmd like “I am …, please…“, this is to mock the voice to differentiate the Admin user or client user(LLM will parse the exact value from message).

1.  For now, I only setup one admin user, normal user can not remove admin user.

1.  Now, any valid user can add new user, should provide password, start_date and end_date are optional.

1.  If user input the password fails 3 times, system will block the user.

1.  if one user is locked due to multiple ties failure, another user can help to open the door.
1.  LLM will check if system armed, username, password, expiration time range fetching.
1.  LLM will check how many times password input failure, if multiple times failed, user will be locked.

Now you are hosting server side successfully, this is a server side light project using FastAPI(Python) + LangGraph + LangSmith(Trace).<br>

