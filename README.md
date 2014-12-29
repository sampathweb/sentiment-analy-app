# Sentiment Analysis App
Developed by [Ramesh Sampath](http://sampathweb.com)

This application is built using Python / Flask for serving prediction API and as an Angular App for web interface.  Application has a tiny sqlite db to hold listing of datasets and the location of dataset files.

The webapp is hosted at [http://apps.sampathweb.com/sentiment-analysis/app/index.html#/](http://apps.sampathweb.com/sentiment-analysis/app/index.html#/)


## Deployment

* Flask API application is running via Gunicorn behind Ngnix.  My Gunicorn command is in api folder

* Webapp is running as Static page served by Nginx.

* Uploaded files are currently saved on the Server.  Plan to move it to S3 bucket via Boto library

* Database currently on the Server as a sqlite database.

## Future Development

* Add Unit Test

* Validate uploaded file for format

* Show probability for each categories

* Extend NaiveBayes model via Stemming to improve accuracy

## Credits

* Inspiration for NaiveBayes Model from Chapter 6 of the book - Programming Collective Intelligence by Toby Segaran
