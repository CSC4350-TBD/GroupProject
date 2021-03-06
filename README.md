# Group Project - TBD movie recommendation app

This is a school group project app. Movie TBD configures Search page which provides movies recommendation based on genre. Users can browse through the catalog and select any movie of interest. They can check the details of the movie including short description, rating, runtime, cast members, director, and genre. As well, the client can watch the trailers and leave a review for future clients. Prior to use the app users are required to login or sign up.

## Members: Alexander Ortiz, Lingyi Zheng, Yuliana Mircheva, SingYu Yu

## Heroku Link: http://recotbdtwo.herokuapp.com

## Requirements

pip install -r requirements.txt

## To Run Application

Run 'python3 app.py' in command terminal
To view on localhost, make sure certain lines in app.run function are commented out in the end of router.py

## To Deploy To Heroku

Create Heroku app
Push to Heroku with command terminal using: git push heroku main

# Important Information _Before_ Running

## API

The limit on API calls for IMDB API is 100 calls per day
Too many in one night will result in a ban as our team has experienced
While testing is encouraged, especially for John and the TAs, please note that there are some movies in certain genres that may result in nasty things due to the new API filters even if the genre itself is seemingly innocent, be wary of documenteries, im pretty sure the adult filter is broken, and for some reason some adult movies are listed in that catagory

## Testing

Mock test library in Python allows to replace part of our app system under test with mock objects and make assertions about how they have been used. unittest.mock provides a core Mock class removing the need to create a host of stubs throughout the test suite.

## Leo

Due to the recently changed of the API, the functionality of the API calls has some formate problems.

## Yuliana

Mocked server test tested if the database saves movie by ID from a hard coded username; then add the same ID to the DB. Next, adds a new ID to the DB and last pass in a list of valid IDs that doesn't include a prior one. The test pass ok.
Succesfully pass login route for user and password.

## Other Known Issues

We used some very unique ways to pass varriables between routes/html pages. The implementation of which scales very poorly with the ammount of varriables that need to be passed in the method we have set up. If we were to expand this project it would be likely that using a front end framework like react (or atleast using some javascript) would allow for a much easier passing of data.

## Things To Improve

For the HTML, there were some areas where code was being reused, such as the code to display flash messages, which probably could have been put into a php file and included in the HTML document since all the different divs and sections can it hard to realize where one has messed up when VS Code decides to take a nap and not autofill.

For the CSS, it's rather messy in general. It was not sorted, and there are probably many ids and/or classes that could easily be put together to avoid confusion when searching for a specific line of code.