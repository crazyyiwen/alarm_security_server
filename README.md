<picture class="github-only">
  <img alt="Alarm.com Logo" src="https://media.licdn.com/dms/image/v2/C4E0BAQH7Ef_zBPUQnw/company-logo_200_200/company-logo_200_200/0/1631327773224?e=1760572800&v=beta&t=F4eDHsvrfiFP7QhJraL5DjXVaeiKeSSlcwtZ-z8Nt1g" width="40%">
</picture>

<div>
<br>
</div>

## Get started

Quick start: [Docs](https://crazyyiwen2015.atlassian.net/wiki/x/vgAC){target=_blank}:

Download and host Docker file - alarm-server:

```
docker build -t alarm-server .
docker run -d -p 8000:8000 --name alarm-server alarm-server
```

Now you are hosting server side successfully, this is a server side light project using FastAPI(Python) + LangGraph + LangSmith(Trace).<br>

Documentation: [Server side documentation](https://crazyyiwen2015.atlassian.net/wiki/x/i4AB){target=_blank}:<br>

