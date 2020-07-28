This bot can welcome new chat members, delete messages with bad words and set, clear and get events. !!lets enjoy it

If you want to support me: Subscribe to my software development channel "Code With Yison" https://www.youtube.com/channel/UC0-0QRFUH9g221kSvRs9plA

Guide for deploy with docker telegram bots on heroku:

1. Install heroku, pyenv, docker on pc
2. Create heroku account and new app with name example: admingroup-bot-telegram
3. Go to app heroku settings and config environment vars
	*Add var: HEROKU_APP_NAME = admingroup-bot-telegram
	*Add var: MODE = prod
	*Add var: TOKEN = token code from botfather
4. Create a new file named "Dockerfile"
5. Create "requirements.txt" for install necessary modules on heroku
	*Open a new console window in the path of project
	*Create a virtual environment "pipenv shell"
	*To see the modules and libraries installed for the bot type "pip freeze"
	*To save that libraries and modules in a txt, type "pip freeze > requirements.txt"
6. Create docker container in the same console window, after to create the requirements.txt 
	*Init docker: "systemctl start docker"
	* type: "docker build -t image-bot-python ."
7. Login in heroku in the same console
	*type: "heroku login" and press any key
	*for see if you are logged successfully type: "heroku container:login"
8. Push container on heroku app project (in the same console window)
	*type: "heroku container:push web -a admingroup-bot-telegram" (insert the same name that in heroku app)
9. Release the app on heroku (in the same console Window)
	*Type: "heroku container:release web -a admingroup-bot-telegram"
10. Done!! for see the logs and if the bot is released correctly
	*Type in new console window: "heroku logs -t -a admingroup-bot-telegram"
11. If you change something in the code of bot:
	*Delete container: "heroku container:rm web -a admingroup-bot-telegram"
	*Set in project path for execute in console and do tests: "set TOKEN = bot token" and "set MODE = dev"
	*You can do tests now.
	*If you have new changes and you want to push again on heroku: go back to step 6
	
Developer: ZeuPlox, Yeison Builes
