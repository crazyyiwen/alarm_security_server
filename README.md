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


Now you are hosting server side successfully, this is a server side light project using FastAPI(Python) + LangGraph + LangSmith(Trace).<br>

