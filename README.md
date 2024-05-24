# Purpose
Port of my original traderJS module from 2 years ago to Python. Python is a more utilitarian language when it comes to automation of trading, so this module will allow for users to utilize this language with their Tradovate accounts.
# Setup
1) Create a Tradovate account and register an app
2) Create accessToken.json (leave blank or if there's an error, setup as {"accessToken":""})
3) Create a .env (fill it in with all your account details)
4) Run the file calling the refresh access token function in order to obtain an access token. This is how you will authenticate sending orders and performing core account actions.
5) Place orders and call the refres access token function in a loop in order to ensure that it never expires
6) Get rich? I don't know - up to you.
