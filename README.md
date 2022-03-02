# lunch-place-decider
This is the task assigned by Corner Case Technologies. Users can upload menu, vote for menu and see winner through 
implemented API endpoints. The list of api endpoints can be found in [this link](http://127.0.0.1:8000/api-docs/). 
**It is noteworthy that the API documentation page is using session authentication and hence we need to log in through 
django admin portal using superuser with proper group assigned in order to try out corresponding api endpoints from 
documentation page.**  
In order to fulfill the requirements users have been categorized in two groups: 
- **Restaurant owner**: Restaurant owners can create restaurants and restaurant menus. Each owner can create multiple 
restaurant instances and for each restaurant, owners can upload more than one menu for a specific day. Restaurant owners
are not allowed to upload  on the same day of the menu availability day. This is to ensure that the list of options 
available to the employees does not change in the middle of the voting period. As winners of last two days are not 
finalized while restaurant menus are being uploaded, the restaurant will be able to upload menu without any interruption.
However employees won't be able to vote for any menu on that restaurant. 
- **Office Employee**: Office employees can see menu options, cast vote and see winner for that day. If an employee
casts vote multiple times, it will simply overwrite his previous vote. Employees can only cast vote for that day. 
The voting deadline is 1PM. Employees will be able to see which restaurant and menu is leading before deadline and will
be presented with message that voting is still open.\
**Note**: As no tie-breaker logic was provided, if two menus have the same vote count, the first item of the queryset 
will be returned as winner.\

This application has been implemented using following technologies:
- Python 3.8
- Django 4.0.1
- Django rest framework 3.13.1
- Postgresql 14.0
- Unit tests have been implemented with Pytest and Pytest-django

##Launch Instructions
###Launch with Docker
The docker containers were created using Docker version 2.3.0.4. To launch the application 
using docker:
1. Clone the project code from the repository.
2. Change the value of **TIME_ZONE** in `settings.py` to your local time zone.
3. Make sure docker is running in the background.
4. Run ``docker-compose up --build`` in the project root directory.
5. Once the build is complete, run ``docker-compose exec web python manage.py migrate`` in
the project root directory.
6. In order to run Pytest unit test, run ``docker-compose exec web pytest``.

###Launching outside Docker
1. Make sure python 3.8 and postgresql 14.0 is installed.
2. Create a database role with ``lunch_place_decider`` and password ``lunch_place_decider``. 
Also create a database named `lunch_place_decider`.
3. Clone the project code from the repository.
4. Change the value of **TIME_ZONE** in `settings.py` to your local time zone.
5. In the project root directory, run the following commands:
    1. ``pip install -r requirements.txt``.
    2. ``python manage.py migrate``.
    3. ``python manage.py runserver``
6. In order to run unit tests, run ``pytest`` in project root directory.

##Future improvement scopes
1. Current implementation has static 1PM voting deadline. A settings item can be added to modify that as per necessity.
Similar settings can be provided for restaurant menu upload deadline also.
2. Provided unit tests do not provide 100% code coverage. More unit tests can be added to ensure coverage. Additionally
Coverage package can be used to generate coverage report which will help to improve test quality.
3. Current implementation does not count weekends and holidays while calculating last two day's winner restaurant. 
Additional functionality can be added to check for skip weekends and holidays while calculating winners.
4. Integrate jwt token for additional features like auto expiry of issued authentication tokens.
5. Add third party api documentation frameworks to allow api testing from documentation page using token authentication.

 