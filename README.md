# FIIR-backend
Database and API endpoints for FIIR app

## REST API Endpoints

Promo code is known as `token` in the following
                        
| Endpoint                    | Type | Parameters                                                      | Done? | Port |
| ----------------------      | ---- | --------------------------------------------------------------- | ----- | ---- |
| /users/create               | POST | {phone:"phonenumber", invitedby:"userid", email:"emailaddress"} | yes   | 9096 |
| /users/setPromo             | POST | {key:"key", user:"userid", promoCode:"code"}                    | no    | 9096 |
| /pics/create                | POST | {key:"key", user:"userid", price:"price", token:"code/null"}    | yes   | 9096 |
| /pics/created               | POST | {key:"key", user:"userid"}                                      | no    | 9096 |
| /pics/flag                  | POST | {key:"key", user:"userid", picId:"picture ID"}                  | no    | 9096 |
| /pics/hide                  | POST | {key:"key", user:"userid", picId:"picture ID"}                  | no    | 9096 |
| /friends/list               | POST | {key:"key", user:"userid"}                                      | no    | 9096 |
| /friends/add:               | POST | {key:"key", user:"userid", friend:"userid"}                     | yes   | 9096 |
| /friends/remove             | POST | {key:"key", user:"userid", friend:"userid"}                     | yes   | 9096 |
| /settings/update_email      | POST | {key:"key", user:"userid", email:"emailaddress"}                | yes   | 9096 |
| /settings/update_phone      | POST | {key:"key", user:"userid", phone:"phonenumber"}                 | yes   | 9096 |

## Starting & Stopping Back-end Server

to start the server, go to ./python and run:

```
nohup ./server.py >> ../../server.py.out &

```

to stop the server:

```
killall python3
```

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
