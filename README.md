# Mini Project

### Final Output
![Final Output](final-log.png?raw=true "Final Output")


TODO:
- Make the following utilities
    - a class having GET, POST, PUT, DELETE methods to make corresponding network requests to a given url
    - a decorator to do automatic retry with refreshed access token if current access token is expired

- Do the following with your implemented utilities
    - Log in by taking username and password input from user
    - get 5 most recent tweets, store them. Make sure you don't repeat these tweets in your posts
    - post 10 tweets with a new joke (you can use `pyjokes` package to get random jokes, instruction below) at 1 min interval. make sure all the 10 jokes are unique.
    - have a log of the execution time for each tweet posting 

Note: There are many third party libraries for making network requests in a much simpler way. However, for this project, we want to use the builtin libraries only, so don't install any additional packages. The only external library we will use is the `pyjokes` package.

I have created a mock twitter server [here](https://github.com/AhsanShihab/Intern-Test-Server). Run the server locally following the instructions there. Use the server to test your application.

### How to get random jokes

`pyjokes` is a python package that can give you random jokes. Follow the instructions below,
- in your project directory, create a python virtual environment first
```
cd <project folder>
python3 -m venv venv
```
- activate the environment
```
source venv/bin/activate
```
- install `pyjokes` package
```
pip3 install pyjokes
```
- use the following code to get a random joke
```python
from pyjokes import get_joke

get_joke() # returns a random joke
```

If you can, save the logs in a file and submit it with your project.

Here is a sample log,

![screenshot of a sample log](sample-log.png?raw=true "Title")

## If you are stuck
<details>
  <summary>Hints</summary>
  
  * write a base NetworkRequest class with static get, post, put, delete methods with generic parameters
  * write a class that can store the access_token and refresh_token, and update them
  * the decorator for updating the token will trigger token update if the network call response code in 401. It will re-run the function after updating the token (if retry also returns 401, no need to retry that request again)
  * the base NetworkRequest class doesn't need to have the auto retry mechanism. You can write another class specific to our need and use the NetworkRequest class's methods to make the network calls from there. This new class methods can be retried with the decorator.
  * use a decorator to log the execution time
  * you can maintain a `set` or `dict` object to keep track of the used jokes. for more fun, use a sql database, (for example, sqlite), to keep track of the used jokes. write a uniquness_checker context manager.
</details>
