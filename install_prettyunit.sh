#!/bin/bash

echo "[+] Creating db"
rm -rf logs
echo "[+] Dropping old logs"
mkdir logs
touch logs/prettyunit.log
echo "[+] Initializing new log file"
rm -rf migrations
python manage.py _dropdb_script >logs/prettyunit.log 2>&1
rm -f prettysite/prettyunit.db
echo "[+] Existing db dropped"
sleep 1
python manage.py db init >logs/prettyunit.log 2>&1
echo "[+] New db initialized"
sleep 1
python manage.py db upgrade 
sleep 1
python manage.py db migrate -m "First" 
sleep 1
python manage.py db upgrade 
sleep 1
echo "[+] DB migrations complete"
if [ "$1" == "-t" ]; then
    echo "[+] Adding test data to the database"
    python manage.py create_test_data >logs/prettyunit.log 2>&1
fi
sleep 1
python manage.py set_default_settings >logs/prettyunit.log 2>&1
echo "[+] Setup completed"
echo "[+] Run 'python manage.py runserver' to start the PrettyUnit web server"

