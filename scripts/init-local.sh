pip install -r requirements.txt;
python manage.py wait_for_postgres;
python manage.py migrate;
python manage.py create_admin_user;
python manage.py seed_happiness;


echo 'alias pmp="python manage.py"' >> ~/.bashrc;
echo 'alias lint="flake8"' >> ~/.bashrc;
echo 'alias runserver="python manage.py runserver 0.0.0.0:8000"' >> ~/.bashrc;
echo 'alias covertest="coverage run manage.py test && coverage report"' >> ~/.bashrc;
echo 'alias kibosh="pmp reset_db --noinput && pmp migrate &&  pmp create_admin_user && pmp seed_happiness"' >> ~/.bashrc;
