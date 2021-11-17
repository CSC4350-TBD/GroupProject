# Group Project - Final
## Members: Alexander Ortiz, Lingyi Zheng, Yuliana Mircheva, SingYu Yu


## Heroku Link: https://recotbd.herokuapp.com/


## Requirements
npm install
pip install -r requirements.txt

## To Run Application
Run 'python3 app.py' in command terminal
To view on localhost, make sure certain lines in app.run function are commented out in the end of router.py

## To Deploy To Heroku
Create Heroku app
Push to Heroku with command terminal using: git push heroku main


# Important Information *Before* Running
## API 
The API has recently changed within the last two days.
Previous code that worked had to be edited and changed and our team is working on fixing API calls (though all should be working now)
The limit on API calls for IMDB API is 100 calls per day
Too many in one night will result in a ban as our team has experienced
While testing is encouraged, especially for John and the TAs, please note that there are some movies in certain genres that may result in nasty things due to the new API filters even if the genre itself is seemingly innocent, be wary of documenteries, im pretty sure the adult filter is broken, and for some reason some adult movies are listed in that catagory

## Testing
## Leo
Insert Leo's test problems here? Anything or issues you feel should be known, if not, just erase

## Yuliana
Insert Yuliana's test problems here? Anything or issues you feel should be known, if not, just erase

## Other Known Issues
We used some very unique ways to pass varriables between routes/html pages. The implementation of which scales very poorly with the ammount of varriables that need to be passed in the method we have set up. If we were to expand this project it would be likely that using a front end framework like react (or atleast using some javascript) would allow for a much easier passing of data.

## Things To Improve
For the HTML, there were some areas where code was being reused, such as the code to display flash messages, which probably could have been put into a php file and included in the HTML document since all the different divs and sections can it hard to realize where one has messed up when VS Code decides to take a nap and not autofill.

For the CSS, it's rather messy in general. It was not sorted, and there are probably many ids and/or classes that could easily be put together to avoid confusion when searching for a specific line of code. 

The api calls could be cleaned up, as there are some functions that might not be clear in their purpose due to similarities to other calls. One way to fix this is to change varriable names to be different, as a lot are similar enough to cause confusion 