# TMF Sample Site -- With Extensions

This is a sample full stack web app written in Python, using the Django framework. This was mostly written in February 2020, with a few additional features or tweaks added on later.

I was given a basic overall template layout and the JSON data files, and wrote all the rest -- the back-end code, dynamic integration of the object-structure to the front-end, user comments, selecting relevant quotes and padding these out with random ones to a total of eight, reverse engineering API calls to the TMF image server, etc. This app features functional testing via Selenium. Django's logging feature is also implemented throughout.

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
