# scrubmylist
An email validation application developed using test driven development principles (TDD)

# Problem Statement
Email marketing is the best way for selling products to consumers online. Companies and businesses usually build up an email list from users signing up for their web app and or their newsletter. To have effective email marketing campaigns, it is imperative that the email addresses in the email lists be verified before sending an email out to a client. 

# Solution
Scrub My List allows users to upload an email list and download the results of the email validation. By using Scrub My List users can be confident that they will know the true health of their email list and be able to isolate and use active, valid email addresses.

# User Stories
As a user, I can register for an account using an email address and password.  
As a user, when I register for an account I receive a confirmation link to verify my email address I used to create an account.  
As a registered user, I can login and logout of the application.  
As a logged in user, I can reset my password.  
As a logged in user, I can request for the email confirmation link to be resent if it expired before I confirmed my account.  
As a logged in user, I can upload a csv file format email list to the application.  
As a logged in user, I can delete any file I uploaded.  
As a logged in user, I can request for a file I uploaded to be validated.  
As a logged in user, I can download the validation results of my email list as a csv file.  

# Application Architecture
Flask - web development  
Celery - background tasks (sending emails)  
Flask-Mail - sending emails  
Flask-WTF - forms  
Flask-Bootstrap - styling  
Flask-Login - login and logout functionality  
Flask-SQLAlchemy and Flask-Migrate - database management  
CSV and Pandas - reading/writing csv files  
Pytest - testing  
Requests - HTTP calls to 3rd party API    
Mailboxvalidator - 3rd Party email validation API  
Docker  
Postgres  

# Development Process
1. Project Setup
2. User management system - registration, login, logout, email confirmation link, password reset, user profile
3. Email list validation - file upload, calling 3rd party API for email verification, file download
4. Containerization
5. Deployment to AWS

# Challenges and lessons learned
-Had to figure out how to set up Celery in a flask application structured using application factory pattern myself as there weren't any upto date, working tutorials online.    
-Developing complex features using TDD is very hard, but powerful and worth the effort.    
-The cornerstone of a good CICD pipeline is unit and integration tests.   
-Building CICD pipeline starts getting difficult and complex as the libraries used in the application increase. In my CI pipeline all the tests passed except tests related to sending email (smtplib.SMTPAuthenticationError: Please log in via your web browser and then try again). 

# Future Projects
Additional features I would like to add to the application in the future include:  
1. Ability for users to view email validation results graphically within the application using chart.js or similar.  
2. Ability for users to download cleaned email list (email list containing only valid email addresses)  
3. Investigate why tests related to sending email failed in the CI pipeline

# Video demonstration
















