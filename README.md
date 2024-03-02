# No Fuss IT Assets App

The No Fuss IT Assets Application serves to allow users to maintain an asset register by enabling the ability to create, update, and delete assets, customers, and manufacturers. Only users with admin privileges are able to delete records, which is based on the role assigned to an account in the database. A pre-existing admin user has been set up which testing the deletion functionality can be done through. The login details for this user are as follows:

Username: Scott

Password: AdminUser123!

The live hosted application for production can be found here:

https://www.nofussit.app/

And the live hosted application for development can be found here:

https://assetsapp.onrender.com/

## Dependencies

Please find the list of dependencies for this application below (this can also be found in requirements.txt):

```bash
alembic==1.11.2
blinker==1.6.2
click==8.1.6
colorama==0.4.6
coverage==7.3.0
Flask==2.3.2
Flask-Limiter==3.5.1
Flask-Login==0.6.2
Flask-Migrate==4.0.4
Flask-SQLAlchemy==3.0.5
Flask-Testing==0.8.1
Flask-WTF==1.1.1
greenlet==2.0.2
gunicorn==21.2.0
iniconfig==2.0.0
itsdangerous==2.1.2
Jinja2==3.1.2
Mako==1.2.4
MarkupSafe==2.1.3
packaging==23.1
pluggy==1.3.0
pytest==7.4.0
pytest-cov==4.1.0
python-dotenv==1.0.0
SQLAlchemy==2.0.19
typing_extensions==4.7.1
Werkzeug==2.3.6
WTForms==3.0.1

```
