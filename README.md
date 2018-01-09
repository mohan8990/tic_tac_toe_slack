# tic_tac_toe_slack
Slack bot for playing tic-tac-toe

# prerequisite
- Python 2.7 
- Pip/Setup tools installed (See https://pip.pypa.io/en/stable/installing/)
- Preferrable to have a virtual env.

# Start server

\# In the $PROJECT_HOME directory execute the following

- pip install -r requirements.txt
- cd ./tic_tac_toe/
- python manage.py migrate
- python manage.py runserver 80

\# Please make sure to populate l./tic_tac_toe/tic_tac_toe/local_settings.py with proper value from your app's OAUTH and Permissions tab

# Start Web tunnel to your server in separate shell

\# Download pagekite
- curl -s https://pagekite.net/pk/ |sudo bash
- pagekite.py mohan.pagekite.me // mohan.pagekite.me could be anything, but make sure you give the same Response URL in slash command of your app. Follow the instructions in command line.
 
 \# Alternatively you can use ngrok, which doesn't require any signups.

