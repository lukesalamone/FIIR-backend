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

## REST API Endpoints

Promo code is known as `token` in the following
                        
| Endpoint                                      | Type | Parameters-example                                              | Done? | Port |
| ----------------------                        | ---- | --------------------------------------------------------------- | ----- | ---- |
| [/users/create](#/users/create)               | POST | {phone:"phonenumber", invitedby:"userid", email:"emailaddress"} | yes   | 9096 |
| [/users/verify](#/users/verify)                   | POST | {"user":1, "verification":"896154"}                             | yes   | 9096 |
| /users/setPromo             | POST | {key:"key", user:"userid", promoCode:"code"}                    | yes   | 9096 |
| /pics/create                | POST | {key:"key", user:"userid", price:"price", token:"code/null"}    | yes   | 9096 |
| /pics/created               | GET  | {key:"key", user:"userid"}                                      | yes   | 9096 |
| /pics/flag                  | POST | {key:"key", user:"userid", picId:"picture ID"}                  | yes   | 9096 |
| /pics/hide                  | POST | {key:"key", user:"userid", picId:"picture ID"}                  | yes   | 9096 |
| /friends/list               | GET  | {key:"key", user:"userid"}                                      | yes   | 9096 |
| /friends/add                | POST | {key:"key", user:"userid", friend:"userid"}                     | yes   | 9096 |
| /friends/remove             | POST | {key:"key", user:"userid", friend:"userid"}                     | yes   | 9096 |
| /settings/update_email      | POST | {key:"key", user:"userid", email:"emailaddress"}                | yes   | 9096 |
| /settings/update_phone      | POST | {key:"key", user:"userid", phone:"phonenumber"}                 | yes   | 9096 |
| /newest/pics                | GET  | {}                                                              | yes   | 9096 |


## Starting & Stopping Back-end Server


to start the server, go to ./python and run:

`nohup ./server.py >> ../../server.py.out &`

to stop the server:

`killall python3`

## API details


### /newest/pics

request type: GET

end-point: http://fiirapp.ddns.net:9096/newest/pics

header: {'Content-Type': 'application/json'}

example response(200):

{"status":"success","num_pic":10,"pictures":[{"id":20,"price":-1,"date_added":"2016-10-12 20:09:52"}{"id":19,"price":-1,"date_added":"2016-10-12 19:31:27"}{"id":18,"price":-1,"date_added":"2016-10-08 11:51:17"}{"id":17,"price":-1,"date_added":"2016-09-25 23:11:45"}{"id":16,"price":-1,"date_added":"2016-09-25 23:11:28"}{"id":15,"price":-1,"date_added":"2016-09-25 23:10:24"}{"id":14,"price":-1,"date_added":"2016-09-25 23:06:16"}{"id":13,"price":-1,"date_added":"2016-09-25 22:59:11"}{"id":12,"price":-1,"date_added":"2016-09-25 22:55:46"}{"id":11,"price":-1,"date_added":"2016-09-25 22:31:00"}]}



### /users/verify

request type: POST

end-point: http://fiirapp.ddns.net:9096/pics/hide

header: {'Content-Type': 'application/json'}

query sample: '{"user": 10, "verification":"859278"}'

example response(200):

{"status":"user successfully verified","auth_token":"03X4I8HYJK6X71ASI2712U2ZM7SHMUB9"}


### /users/create

request type: POST

end-point: http://fiirapp.ddns.net:9096/pics/hide

header: {'Content-Type': 'application/json'}

query sample: '{"phone":"(608)320-7727", "invitedby": 1, "email":"zarickzheng@gmail.com"}'

example response(200):

{"status":"user successfully created","user_id":"20"}




### /pics/hide

request type: POST

end-point: http://fiirapp.ddns.net:9096/pics/hide

header: {'Content-Type': 'application/json'}

query sample: '{"key":"DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS", "user": 1, "picId":"18"}'


example response(200):

{"status":"success","msg":"picture 18 successfully hided"}

example response(400 user not exist):

{"status":"error","msg":"invalid user id"}

example response(400 invalid key):

{"status":"error","msg":"invalid key"}

example response(400 invalid picture id)

{"status":"error","msg":"this picture is not owned by 1"}




### /pics/flag

request type: POST

end-point: http://fiirapp.ddns.net:9096/pics/flag

header: {'Content-Type': 'application/json'}

query sample: '{"key":"DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS", "user": 1, "picId":"18"}'


example response(200):

{"status":"success","msg":"picture 18 successfully flagged"}

example response(400 user not exist):

{"status":"error","msg":"invalid user id"}

example response(400 invalid key):

{"status":"error","msg":"invalid key"}

example response(400 invalid picture id)

{"status":"error","msg":"this picture is not owned by 1"}




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
