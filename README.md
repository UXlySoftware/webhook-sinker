# Webhook Sinker

This tiny repo implements a docker stack for locally testing webhooks. It uses [ngrok](https://ngrok.com) to establish an introspective
tunnel from you local machine to a public URL which you can use as a webhook URL is various webhook services. 


## Build the Python server

First build the python server which will implement a route for your webhook:
```
docker build -t python-server -f src/python/Dockerfile
```

They [python server](./src/python/main.py) uses [fastapi](https://fastapi.tiangolo.com/). You can modify it as necessary for your purposes. 

## Run the Docker Stack

Next, grab your auth token from the ngrok dashboard and bring up the Docker webhook sinker stack:

```
sudo NGROK_AUTHTOKEN=<my-auth-token> docker compose up -d
```

You can open [http://localhost:4040](http://localhost:4040) to see the ngrok dashboard to see the public URL assigned to your session and also
any requests made against it. 