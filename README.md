# Group Project - Final
## Members: Alexander Ortiz, Lingyi Zheng, Yuliana Mircheva, SingYu Yu


## Heroku Link: https://recotbd.herokuapp.com/


## Requirements
npm install
pip install -r requirements.txt

## To Run Application
Run 'python3 app.py' in command terminal
To view on localhost, make sure lines "210-211" are commented out in router.py

## To Deploy To Heroku
Create Heroku app
Push to Heroku with command terminal using: git push heroku main


# Important Information *Before* Running
## API 
The API has recently changed within the last two days 
Previous code that worked had to be edited and changed and our team is working on fixing API calls
The limit on API calls for IMDB API is 100 calls per day
Too many in one night will result in a ban as our team has experienced
While testing is encouraged, especially for John and the TAs, please note that there are some movies in certain genres that may result in nasty things due to the new API filters even if the genre itself is seemingly innocent

Other members add more^

## Testing
## Leo
Insert Leo's test problems here? Anything or issues you feel should be known, if not, just erase

## Yuliana
Insert Yuliana's test problems here? Anything or issues you feel should be known, if not, just erase

## Other Known Issues
Insert something here, any trouble?

## Something To Improve
For the HTML, there were some areas where code was being reused, such as the code to display flash messages, which probably could have been put into a php file and included in the HTML document since all the different divs and sections can it hard to realize where one has messed up when VS Code decides to take a nap and not autofill.

For the CSS, it's rather messy in general. It was not sorted, and there are probably many ids and/or classes that could easily be put together to avoid confusion when searching for a specific line of code. 