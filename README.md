# Seshnet

Seshnet is a decentralized open source communcation app similar to slack or discord.
Each session (server) contains it's own community that has it's own users and rules.

This is application is still being developed, but an early version of the app can be experienced here: http://seshnet.net

This application is built with Django (a Python web framework)

The eventual goal of this application is to be easily self-hosted or deployed on an AWS EC2 or Linode virtual server.

To acheive the real-time chat functionality, Django channels is utilized to manage websockets and Redis is used as the websocket server.

Memcached is being used to track online activity which can be hidden if chosen by the user.
