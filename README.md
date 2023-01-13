# Seshnet

Seshnet is a decentralized open source communcation app similar to slack or discord.
Each session (server) contains it's own community that has it's own users and rules.

This is application is still being developed, but the functionality of this web app can be seen here:
[SeshNet Video](https://rumble.com/v1fhf7v-seshnet-i-made-a-real-time-chat-app.html)

This application is built with [Django](https://www.djangoproject.com/).

The eventual goal of this application is to be easily self-hosted or deployed on an AWS EC2 or Linode virtual server.

To acheive the real-time chat functionality, Django channels is utilized to manage websockets and Redis is used as the websocket server.
Memcached is being used to track online activity which can be hidden if chosen by the user.

Eventually I would like to make this application into a Progressive Web App.
