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

### Examples
Note: 
For “Arm system“/”Disarm System”/”Door operation(open door)”, 
please use cmd like “I am …, please…“, this is to mock the voice differentiate the Admin user or client user(LLM will parse the exact value from message).
Case_1: Open the UI:<br>
<img src="media/ex1.png" width="600">
Case_2: Arm the system:<br>
<img src="media/ex2.png" width="600">
Case_3: Add user:<br>
<img src="media/ex3.png" width="600">
Case_4: Show all users:<br>
<img src="media/ex4.png" width="600">
Case_5: Remove user:<br>
<img src="media/ex5.png" width="600">
Case_6: Remove user - Admin user can not be removed:<br>
<img src="media/ex6.png" width="600">
Case_7: Open Door:<br>
It will be locked if password failed 3 times.<br>
<img src="media/ex7.png" width="600">
Case_8: Multiple users, one locked, another can open the door:<br>
<img src="media/ex8.png" width="600">
Case_9: Open door before or after system armed:<br>
1 before system armed, anyone can open the door<br>
2 But once system armed, only valid user can open the door<br>
<img src="media/ex9.png" width="600">
Case_10: Complex words parse:<br>
<img src="media/ex11.png" width="600">
<img src="media/ex12.png" width="600">


Now you are hosting server side successfully, this is a server side light project using FastAPI(Python) + LangGraph + LangSmith(Trace).<br>

