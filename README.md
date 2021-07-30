# Web based database management program.
- I used python flask to connect MySQL database besides i used basic level HTML and CSS.

## The main purpose of this program is to manage database with a simple web based interface
- I used XAMPP to run my MySQL server. you have to run project.ipynb after your MySQL has run. Check the password or name of your connection in project.ipynb to crete and fill the tables correctly.
- project.ipynb : i created my database and filled the tables also i write down the complex command that i used.
- app.py : When you run it, it leads you to a a web page of my database user interface where you can add,show and execute complex command.
- For the signup page you must enter any password with more than 10 characters in length, there are no correct password i just wanna use flash() method in Flask.

## Errors that i didnt work on them;

- Remove button returns succesfull operation everytime because on mysql terminal it also works without any error when you try to delete an item that even not exists.
- On GYM TABLE oldest person's age (2nd complex operation) not comes with error case. It just returns "none" when gym has 0 subscribers.
- On PERSONAL TRAINER TABLE for 2nd complex operation it returns also "none" like in the gym_table. Another problem is it return average age with a string "Decimal" on front on it //Ex: ((Decimal,,32,455))

I didn't wanna work on them because they really are not big problem. I know how to fix them but it will be a lot of waste of time for me. I will learn how to fetch data as dictionary by using flask to fix some of these problems.
