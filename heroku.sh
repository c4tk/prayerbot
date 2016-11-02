heroku login
#heroku git:remote -a prayerbotc4k
#git add .
#git commit -m "Demo"
git push heroku master
#heroku ps:scale web=1
heroku open
heroku logs --tail
#heroku config:set CCESS_TOKEN=VALUE
#heroku config:unset CCESS_TOKEN
heroku config
