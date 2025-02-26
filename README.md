# Chat-System

## About
It's a chat system made using python, the objective with this project was understand how socket communication/chat works, focusing more on the back-end side (server). The project has all functionalities like, login, user creation, delete a user, modify user information, chatting and so on. How i said this project wasn't focused on the front-end (client) side, so the client here is used by a terminal (don't have a GUI). Everything in general is working, but the chatting system has some bugs and the client part for this isn't completely finished.

## Project demonstration video
[![Chat System Demo](https://img.youtube.com/vi/urEdKk-7yp0/0.jpg)](https://www.youtube.com/watch?v=urEdKk-7yp0)

## Used technologies
- Python
- MySQL
- Socket Protocol

## Installation
It's important to note that the commands described here are specified for the Linux operating system. However, the concept is the same.

### Project clone

```
git clone https://github.com/GustavoHenriqueSchmitz/LoginSystem.git
```

### Install Dependencies
```
pip install -r requirements.txt
```

## Running the app

**1 -** In the root directory execute (Initialize the DB):
```
sudo docker-compose up
```

**2 -** To initialize the server, open a terminal and from the root directory execute:

```
cd src/server
python server.py
```
**3 -** To initialize a client open a terminal (multiple clients can connect in the server) and from the root directory execute:
```
cd src/client
python client.py
```

## Author
**Gustavo Henrique Schmitz**

**Linkedin:** https://www.linkedin.com/in/gustavo-henrique-schmitz  
**Portfolio:** https://gustavohenriqueschmitz.com  
**Email:** gustavohenriqueschmitz568@gmail.com  
