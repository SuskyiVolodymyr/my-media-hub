# MyMediaHub
MyMediaHub is a web application that allows users to create and manage lists of their favorite movies, anime, series, and cartoons. Users can rate, comment, and set statuses (watching, finished, planning to watch, dropped) for each item.

## Check it out
[My Media Hub project deployed to Render](https://my-media-hub.onrender.com)

Test user:
- login : TestUser
- password: Test_password_1234

## Features
- User Authentication: Secure user login and registration.
- Media Management: Users can add, update, and remove items from their lists.
- Search and Filter: Search for media by title and filter by genre.
- Rating System: Rate media items on a scale of 0 to 5.
- Comments: Add and view comments for each media item.
- Responsive Design: The application is optimized for both desktop and mobile devices.
## Technologies Used
- Backend: Django
- Frontend: Bootstrap 4
- Database: SQLite (development), PostgreSQL (production)
- Authentication: Django's built-in authentication system
## Setup and Installation

Clone the repository:
```
git clone https://github.com/SuskyiVolodymyr/my-media-hub.git
cd mymediahub
```
Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```
Install the dependencies:
```
pip install -r requirements.txt
```
Apply migrations:
```
python manage.py migrate
```
Create a superuser:
```
python manage.py createsuperuser
```
Run the development server:
```
python manage.py runserver
```
You also need some environment variables (example in .env.template): 
```
DATABASE_URL="..."  # if you want to use another database
DJANGO_DEBUG=False  # to disable djungo debug
DJANGO_SECRET_KEY=... 
```
Load the initial data:
```
python manage.py loaddata initial_data.json
```
Access the application:
Open your browser and go to http://localhost:8000.

## Usage
- Login: Use the login page to authenticate.
- Dashboard: After logging in, you will see the dashboard where you can manage your media lists.
- Add Media: Use the forms to add new movies, anime, series, and cartoons.
- Search and Filter: Use the search bar and genre filters to find specific media.
- Rate and Comment: Click on a media item to rate and comment on it.
- Update and Remove: Use the update and remove links to manage your media items.
## Customization
### Styling
- CSS: Custom styles are defined in static/css/styles.css.
- Fonts: The application uses the 'Roboto Slab' font.
- Colors: The main color scheme is a dark theme with purple accents.
### Forms
- Bootstrap is used for styling forms.
- Forms are customized to include specific classes and styles.
