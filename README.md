# Seshnet

Seshnet is a decentralized open source communcation app similar to slack or discord.
Each session (server) contains it's own community that has it's own users and rules.

This is application is still being developed.

This application is built with [Django](https://www.djangoproject.com/).

The eventual goal of this application is to be easily self-hosted or deployed on an AWS EC2 or Linode server.

To acheive the real-time chat functionality, Django channels is utilized to manage websockets and Redis is used to deliver the messages.
Memcached is being used to track online activity which can be hidden if chosen by the user.

Eventually I would like to make this application into a Progressive Web App and enable it to be considered a Fediverse application.
