# TMF Sample Site -- With Extensions

Hello! Thanks for reading my README!

# Pre-Requisites
Python 3 and pip

# Clone
Clone the github repo and navigate to the root directory of the repo.

Then, follow the instructions, below.

# Running the project

## 1. Install and activate the virtual environment
Be sure you are in the same directory as this README, then,
```
$ python3 -m venv ./tmf_venv/
$ source tmf_venv/bin/activate
```

## 2. Install requirements
Be sure you're in the same directory as this README and thus, `requirements.txt`, then,
```
$ pip install -r requirements.txt
```

## 3. Navigate to the project directory
```
$ cd TMF_project/
```
Once you do this, double-check to make sure you are in the same directory as the `manage.py` file

## 4. Set up the database and collect the static files
```
$ python3 manage.py migrate
$ python3 manage.py collectstatic
```
It's fine to overwrite any existing static files, if asked: by following these instructions you are starting fresh!

## 5. Start the server
```
$ python3 manage.py runserver
```

## 6. Go interact with the app!
Point your web browser at '127.0.0.1:8000/' or 'localhost:8000'.

## 7. Exit
To exit the virtual environment when you're done, simply type `deactivate` all by itself

# Additional options, and some details on the project
- When you run the project, none of the Articles will have any attached comments yet. Please add some as you browse the app!
- I did not implement the "relevant" quotes per article, but simply load three random quotes. To have a better feel for the shuffling functionality, please feel free to uncomment the relevant code block in views.py's article_detail method.
```
    # # uncomment this code block to get a larger sampling of quotes for the article
    # # get a larger number of random quotes for testing the shuffle:
    # quotes = get_random_quotes(10)
```
You could also comment out the code block just above, but it's not strictly necessary.

Enjoy! and thanks for reading.
