Herana
======

This is the University-Community Engagement Assessment Instrument built for Herana by Code for South Africa.

Local Development
-----------------

1. Clone the repo
2. Setup a virtualenv: `virtualenv --no-site-packages env; source env/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Setup the database:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```
Three types of users with different permissions exist in the application.
* Global Admin
* Institute Admin
* Project Leader

As the superuser:
Add an Institute with labels for the organisation levels e.g. Faculty, department, school
Add the organisational units to the levels e.g Department of Science.

Add an Institute admin user.
Add a Project Leader user.

The InstituteAdmin and ProjectLeader groups are created in the background if they don't exist upon user creation.

As the InstituteAdmin user, create a reporting period.
Only one reporting period can be active for an institute.
Engagement projects can only be captured if a reporting period is active.

Institute admin users can create Project leaders for the Institute they belong to.
Project leaders capture Engagement projects.
Institute admin and Global admin users can reject, flag and delete projects.

Engagement Projects can be in Draft or Final state.
Look [here](https://github.com/Code4SA/herana/blob/master/herana/admin.py#L698) to see how Engagement Projects are saved, deleted and carried over from one period to the next.


Production deployment
---------------------

Production deployment assumes you're running on Heroku.

You will need:

* a django secret key
* a New Relic license key
* An AWS S3 access & secret access key
* A django email host password
* The Google Analytics key

```bash
dokku config:set municipal-finance DJANGO_DEBUG=False \
                                   AWS_ACCESS_KEY_ID=... \
                                   AWS_SECRET_ACCESS_KEY=... \
                                   NEW_RELIC_APP_NAME=Herana \
                                   NEW_RELIC_LICENSE_KEY=... \
                                   DJANGO_EMAIL_HOST_PASSWORD=...\
                                   GOOGLE_ANALYTICS_ID=...\
                                   DJANGO_SECRET_KEY=...\
                                   DATABASE_URL=postgres://herana_questionnaire:...@postgresq....amazonaws.com/herana_questionnaire

git push dokku
```
License
-------

MIT License
