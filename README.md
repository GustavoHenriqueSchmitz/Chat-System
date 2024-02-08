# Chat-System

**Description**: It's a chat system made using python, the objective with this project was understand how socket comunication/chat works, focusing more on the back-end side (server). This version is the old one, the first made. The project has all functionalities like, login, user creation, delete a user, modify user information, chatting and so on. How i said this project wasn't focused on the front-end (client) side, so the client here is used by a terminal (don't have a GUI). Everthing in general is working, but the chatting system has some bugs and the client part for this isn't completely finished. 

⚠️ Anyway this was a descontinued version of this project.

## How to initialize the project (Guide for linux preferencially)

**1 -** In the root directory execute (Install the requirements for the project):
```
pip install -r requiremets.txt
```

**2 -** In the root directory execute (Initialize the DB):
```
sudo docker-compose up
```

**3 -** To initialize the server, open a terminal and from the root directory execute:

```
cd src/server
python server.py
```
**4 -** To initialize a client open a terminal (multiple clients can connect in the server) and from the root directory execute:
```
cd src/client
python client.py
```
