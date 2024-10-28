# Chat-System

## About the project
This is a chat system built with Python. The goal of this project was to understand how socket communication and chat systems work, with a focus on the back-end (server) side. This is the first version, and it includes all core functionalities, such as login, user creation, user deletion, user information modification, chatting, and more. As mentioned, the project doesn’t focus on the front-end (client) side, so the client interface is command-line based (no GUI). Overall, most features are working, though the chat system has some bugs, and the client implementation is not fully complete.

⚠️ Anyway this was a descontinued version of this project.

## Used technology
- Python
- Docker
- MySQL
- Socket Protocol

## Installing the project
**1 -** Clone the project:
```
git clone https://github.com/GustavoHenriqueSchmitz/Chat-System.git
```
**2 -** Install [Python V3.10](https://www.python.org/downloads/)  
**3 -** Install [docker-compose](https://docs.docker.com/compose/install/)
**4 -** Install MySQL Development Libraries. `mysqlclient` requires MySQL development libraries.  
Visit the [MySQL Community Downloads](https://dev.mysql.com/downloads/). Alternatively, you can use the compatible [MariaDB Downloads](https://mariadb.com/downloads/).
**5 -** In the root directory of the project execute:
```
pip install -r requirements.txt
```

## Initializing the project
**1 -** Open a terminal and in the root directory execute:
```
docker-compose up
```

**3 -** To initialize the server, open a terminal and from the server root directory execute:
```
python server.py
```

**4 -** To initialize a client open a terminal and from the client root directory execute:
```
python client.py
```

## Author
**Gustavo Henrique Schmitz**

**Linkedin:** https://www.linkedin.com/in/gustavo-henrique-schmitz  
**Portfolio:** https://gustavohenriqueschmitz.com  
**Email:** gustavohenriqueschmitz568@gmail.com  
