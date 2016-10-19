# FIIR  
All files of or related to F.I.I.R.  
  
##Installing  
Make sure you have git installed:  
  
`sudo apt-get install git`  
  
Clone the project:  
  
`git clone git@github.com:lukesalamone/FIIR.git`  
  
[Make sure you have Android Studio installed](http://developer.android.com/sdk/installing/index.html)  
  
##Android Projects  
###FIIRapp  
Working version of Android application  
  
###POST Test  
Demo of simple POST requests to server.  
  
© 2016 FIIR  
=======  
# FIIR-backend  
Database and API endpoints for FIIR app  
  
## Starting & Stopping Back-end Server  
  
  
to start the server in debug mode(messages will be printed out to std), go to ./python and run:  
`./server.py`  
to start the server in production mode(messages will be logged in ../../server.py.out), go to ./python and run:  
`nohup ./server.py >> ../../server.py.out &`  
to check if server is running, type:  
`ps -fC python3`  
and if it shows an entry ending with 'python3 ./server.py', it means server is running(it will also show the PID of server)  
  
to stop the server, type:  
`kill XXX`  
where XXX is the PID of server  
  
  
## REST API Endpoints  
  
Promo code is known as `token` in the following  
  
| Endpoint                                      | Type | Parameters-example                                              | Done? | Port |  
| ----------------------                        | ---- | --------------------------------------------------------------- | ----- | ---- |  
| [/users/create](#userscreate)               | POST | {"phone":"phonenumber", "invitedby":"userid", "email":"emailaddress"} | yes   | 9096 |  
| [/users/create](#userscreate-overloaded)               | POST | {"phone":"phonenumber", "invitedby":"userid", "email":"emailaddress", "carrier":"carrier"} | yes  | 9096 |  
| [/users/verify](#usersverify)                   | POST | {"user":1, "verification":"896154"}                             | yes   | 9096 |  
| [/users/setPromo](#userssetPromo)             | POST | {"key":"key", "user":"userid", "promoCode":"code"}                    | yes   | 9096 |  
| [/pics/create](#picscreate)                | POST | {"key":"key", "user":"userid", "price":"price", "token":"code/null"}    | yes   | 9096 |  
| [/pics/created](#picscreated)               | GET  | {key:"key", user:"userid"}                                      | yes   | 9096 |  
| [/pics/flag](#picsflag)              | POST | {key:"key", user:"userid", picId:"picture ID"}                  | yes   | 9096 |  
| [/pics/hide](#picshide)              | POST | {key:"key", user:"userid", picId:"picture ID"}                  | yes   | 9096 |  
| [/friends/list](#friendslist)           | GET  | {key:"key", user:"userid"}                                      | yes   | 9096 |  
| [/friends/add](#friendsadd)            | POST | {key:"key", user:"userid", friend:"userid"}                     | yes   | 9096 |  
| [/friends/remove](#friendsremove)         | POST | {key:"key", user:"userid", friend:"userid"}                     | yes   | 9096 |  
| [/settings/update_email](#settingsupdate_email)  | POST | {key:"key", user:"userid", email:"emailaddress"}                | yes   | 9096 |  
| [/settings/update_phone](#settingsupdate_phone)  | POST | {key:"key", user:"userid", phone:"phonenumber"}                 | yes   | 9096 |  
| [/newest/pics](#newestpics)            | GET  | {}                                                              | yes   | 9096 |  
  
## API details  
  
### /users/create  
  
Request type: POST  
Endpoint: http://fiirapp.ddns.net:9096/users/create  
Header: {'Content-Type': 'application/json'}  
query sample: `{"phone":"(608)320-7727", "invitedby": 1, "email":"zarickzheng@gmail.com"}`  
example response(200):  
`{"status":"ok", "msg":"user successfully created","user_id":"20"}`  
This endpoint may also errorback to request for phone carrier:  
`{"status":"err", msg:"carrier not found"}`  
  
### /users/create (overloaded)  
  
Request type: POST  
Endpoint: http://fiirapp.ddns.net:9096/users/create  
Header: {'Content-Type': 'application/json'}  
Query sample: `{"phone":"(608)867-5309", "invitedby":-1, "email":"buckybadger@wisc.edu", "carrier":"att"}`  
example response (200):  
`{"status":"ok", "msg":"user successfully created","user_id":"30"}`  
  
Carriers will be sent as the following abbreviations:  
  
| Company | Abbreviation |  
| ------- | ------------ |  
| Alltel | alltel |  
| AT&T | att |  
| Boost Mobile | boost |  
| Sprint | sprint |  
| T-Mobile | tmobile |  
| US Cellular | uscellular |  
| Verizon | verizon |  
| Virgin Mobile | virgin |  
  
  
### /users/verify  
  
Request type: POST  
Endpoint: http://fiirapp.ddns.net:9096/users/verify  
Header: {'Content-Type': 'application/json'}  
query sample: `{"user": 10, "verification":"859278"}`  
  
#### Example response(200):  
`{"status":"user successfully verified","auth_token":"03X4I8HYJK6X71ASI2712U2ZM7SHMUB9"}`  
  
#### Example response(400 user verified already)  
`{status:"error", msg:"user not verifiable"}`  
  
#### Example response(400 invalid activation code):  
`{"status":"error","msg":"wrong activation code"}`  
  
  
### /users/setPromo  
  
#### Example request (POST)  
`{"key":"QWERTYUIOPLKJHGFDSAQWER123456789", "user":1, "promo":"deeznuts"}`  
  
#### Example response  
`{"status":"ok", "msg":"updated with token deeznuts"}`  
Server may also errorback:  
`{"status":"err", "msg":"token not found"}`  
  
### /newest/pics  
  
request type: GET  
end-point: http://fiirapp.ddns.net:9096/newest/pics  
header: `{'Content-Type': 'application/json'}`  
  
#### Example response(200):  
  
`{"status":"success","num_pic":10,"pictures":[{"id":20,"price":-1,"date_added":"2016-10-12 20:09:52"}{"id":19,"price":-1,"date_added":"2016-10-12 19:31:27"}{"id":18,"price":-1,"date_added":"2016-10-08 11:51:17"}{"id":17,"price":-1,"date_added":"2016-09-25 23:11:45"}{"id":16,"price":-1,"date_added":"2016-09-25 23:11:28"}{"id":15,"price":-1,"date_added":"2016-09-25 23:10:24"}{"id":14,"price":-1,"date_added":"2016-09-25 23:06:16"}{"id":13,"price":-1,"date_added":"2016-09-25 22:59:11"}{"id":12,"price":-1,"date_added":"2016-09-25 22:55:46"}{"id":11,"price":-1,"date_added":"2016-09-25 22:31:00"}]}`  
  
### /pics/hide  
  
request type: POST  
end-point: http://fiirapp.ddns.net:9096/pics/hide  
header: `{'Content-Type': 'application/json'}`  
query sample: `{"key":"DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS", "user": 1, "picId":"18"}`  
  
#### Example response(200):  
`{"status":"success","msg":"picture 18 successfully hidden"}`  
  
example response(400 user not exist):  
`{"status":"error","msg":"invalid user id"}`  
  
example response(400 invalid key):  
`{"status":"error","msg":"invalid key"}`  
  
example response(400 invalid picture id)  
`{"status":"error","msg":"this picture is not owned by 1"}`  
  
  
### /pics/flag  
  
request type: POST  
end-point: http://fiirapp.ddns.net:9096/pics/flag  
header: {'Content-Type': 'application/json'}  
query sample: `{"key":"DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS", "user": 1, "picId":"18"}`  
  
#### Example response(200):  
`{"status":"success","msg":"picture 18 successfully flagged"}`  
  
#### Example response(400 user not exist):  
{"status":"error","msg":"invalid user id"}  
  
#### Example response(400 invalid key):  
`{"status":"error","msg":"invalid key"}`  
  
#### Example response(400 invalid picture id):  
`{"status":"error","msg":"this picture is not owned by 1"}`  
  
  
## Number verification  
We will be using API of numverify.con to determine carriers for any given number. We will then use the email to SMS gateway to send messages to the correct carrier:  
  
Alltel 	`1234567890@message.alltel.com`  
AT&T (formerly Cingular) 	`1234567890@txt.att.net`  
Boost Mobile 	`1234567890@myboostmobile.com`  
Nextel (now Sprint Nextel) 	`1234567890@messaging.nextel.com`  
Sprint PCS (now Sprint Nextel) 	`1234567890@messaging.sprintpcs.com`  
T-Mobile 	`1234567890@tmomail.net`  
US Cellular 	`1234567890email.uscc.net`  
Verizon 	`1234567890@vtext.com`  
Virgin Mobile USA 	`1234567890@vmobl.com`  
 

