Course project for https://cybersecuritybase.github.io/

The application is not 100% functional, but was created to demonstrate some of the top 10 OWASP vulnerabilities

You might find at least these if you look hard enough:
* XSS
* CSRF
* Weak authentication
* SQL injection
* Direct object reference

Installation (tested on a fresh Ubuntu 16.04):
* Clone the repo and `cd` to the folder
* Install pip: `sudo apt-get install python-pip`
* Install virtualenv `pip install virtualenv`
* Boot up the virtual environment `. venv/bin/activate` (this has to be repeated after closing the session)
* Install dependencies `pip install -r requirements.txt`
* Make a script for the following tasks or do them every time you boot up the development environment
* Set `export FLASK_APP=hello.py`
* and `export FLASK_DEBUG=1`
* Now try `flask run` it should work
