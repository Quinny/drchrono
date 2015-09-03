Dr. Chrono API Project
=======================

A small django application created using the Dr. Chrono API.

Allows doctors to wish their patients happy birthday.

Design Decisions
==================

Patient info is not stored
-------------------------------

Since doctors would most likely only be looking at this page once or twice a day, 
I decided not store patient info in the database.  Instead I request the info from the API 
each time.  This insures that the data is always up-to-date without the added headache of having to keep 
my database synced with the information that the API is providing.

Email bodies are not auto generated
-------------------------------------

I hate getting auto generated emails, and you probably do too.  The main reason 
a doctor would be using this app is to connect better with their patients, and so 
I believe that they should write the emails themselves to give it a better feel.

Make Reminders If we have no contact info
------------------------------------------

Doctors probably want at least one way to contact their patients, so I added 
a check where if the patients do not have any contact information, the doctor 
can make a reminder to ask them on their next visit.  They can also use this opportunity 
to wish them a belated birthday.

Requirements
-------------------

* Django 1.8.4
* Requests 2.5.3
