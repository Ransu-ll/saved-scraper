# Saved Scraper - Scraping your saved posts on Reddit


## Introduction
A script designed to go through your saved posts and comments on Reddit, put them in an SQLite database and 
optionally export it to a `.csv` file for ease of access. 

If the saved content already exists in the database, then it will not be duplicated.

It can be also used as a module if desired.

Note: If you have more than 1000 comments and posts saved, this script will not be able to capture all of them due to
limitations in the API. See [Obfuscation and API limitations](https://praw.readthedocs.io/en/v3.6.2/pages/getting_started.html#obfuscation-and-api-limitations).

## Installation

### Part 1 - Creating a Reddit application
1. Go to your Reddit account's [authorised applications](https://www.reddit.com/prefs/apps/) page.
2. Find the button that allows you to create an app and click on it.
3. The `name` can be set to anything, I recommend "saved-scraper". The `description` and `about` can be left blank, 
however, the `uri` must be set to something. I recommend "http://www.example.com/unused/redirect/uri" as per the 
outdated but useful nonetheless 
[archived PRAW (Python Reddit API Wrapper) documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example).
It will not be all that relevant for this script anyway.
4. Press the "create app" button. Note the `client id`, located below the text that says "personal use script", and 
`client secret` as they will be used in the next section.

***WARNING: KEEP `client id` AND `client secret` PRIVATE - THIS SHOULD ONLY BE KNOWN BY YOU.***

### Part 2 - Installing the script
Note: You will need to have installed Python 3.10+ for this script to work. Compatibility with older versions not
guaranteed.

Note: You will need to install 3rd party modules `praw` and `dotenv`. If unsure how to install them, see  the official
document [Installing Python Modules](https://docs.python.org/3/installing/index.html). The former is used to access your
Reddit account, the latter is for isolating your login details, as well as `client id` and `client secret`.

1. Clone or download this repository.
2. [Pick branch of choice, see subheadings]

    #### 2a. Using a `.env` file (recommended)
    In the same folder which [the script](scrapesaved.py) is in, create a file called `.env`.
    
    The .env should look like the following:
    ```
    CLIENT_ID=[INSERT "client id"]
    CLIENT_SECRET=[INSERT "client secret"]
    USER_AGENT=desktop:saved_scraper:v0.0.1 (by u/[INSERT YOUR USERNAME])
    
    USER_NAME=[INSERT YOUR USERNAME]
    USER_PASS=[INSERT YOUR PASSWORD]
    ```
    Where there are brackets, do not include them when you insert values. For example, `CLIENT_ID=AbCDEF_G192V`.  
    `CLIENT_ID` is 22 characters long, `CLIENT_SECRET` is 30 characters long.
    
    #### 2b. Manually inputting the details
    In [the script](scrapesaved.py), where `main()` is called set `True` to `False` and it will prompt you to add the
    details via the `input()` function.


3. Run the file! By default, it will scrape all of your saved content, create a database and put the data there and then
export the contents of the database to a `.csv` file.

## Using the produced `.csv` file
- `Sub` - the Subreddit which the post/comment belongs to
- `Type` - if it is a comment or a post. `0` means post, `1` means comment
- `ID` - The ID of the content.
- `Title` - The title of the post. If it is a comment, it is the title of the post which it is under.
- `URL` - The link to it. Put `reddit.com` before the URL listed to access the link directly to it.
