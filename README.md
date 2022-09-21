# Cashbackhubsupportbot

## Installation instructions

### 1. Create <code>.env</code> file
~~~
BOT_TOKEN=<YouToken>
HOST=<YouHOST>
PORT=5000
DATABASE_NAME = 'application.db'

SEND_URL= Unique URL for sending events from the JIVO system
~~~

### 2. Run docker-compose.
#### Commands: <code>docker-compose up --build -d</code>

### 3. Settings for Jivo 
##### WEBHOOK_ENDPOINT:
- FOR_MESSAGE: <code>\<YouHOST>/jivo/wh</code>
- FOR_EVENT: <code>\<YouHOST>/jivo/wh/event</code>

### Ready! ✅
