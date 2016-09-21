# FIIR-backend
Database and API endpoints for FIIR app

## API Endpoints

### Done
POST  pics/create  {}


### Upcoming
GET   pics/created  
POST  pics/update  
GET   friends/list  
POST  friends/add  
POST  friends/remove  
POST  settings/update_email  
POST  settings/update_phone

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
