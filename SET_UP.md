# IS Lab 2017 

### Reach the website:
 - [Website Link](http://129.132.114.13:8000/instaTrack/)
 - Login with: 
  - user: admin
  - pass: adminadmin

### Dependencies for the backend:
- Django
- Channels	
- MongoDB
- Twisted: ATTENTION: after this you MUST do pip install -U channels (to downgrade twisted so it works)
- Redis
- CoreNLP

### Necessary commands for running the server:
 - run NLP server from nlp/lib: `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000` (run in screen)
 - run mongodb: `sudo service mongod start`
 - run schedualed job: `python manage.py myschedule`

### login and DB data:
 - admin login: admin
 - admin pass: adminadmin
 - MongoDB database name: team42

### Setup your local sql:
 - if models changed, first run: `python manage.py makemigrations`
 - Create/Update the database with `python manage.py migrate`
 - Create an admin username: `python manage.py createsuperuser`
 - Then go on [admin](http://129.132.114.13:8000/admin/) page and create a 
    userprofile for yourself. This is temporarily and will be changed when 
**Sign Up** feature is implemented. 

### Some usefull mongoDB commands:
 - start(stop) mongodb: `sudo service mongod start`(stop)
 - mongodb terminal: `mongo`
 - show all databeses on the computer: `show dbs`
 - switch tou our DB: `use team42`
 - print all documents of type WeTrackUser: `db.we_track_user.find().pretty()`

### *Optional:* Commands for starting server with multiple workers:
 - redis server: `redis-server` (run in screen)
 - `python manage.py runworker`   (later we will run more of these)
 - `daphne team42.asgi:channel_layer`


