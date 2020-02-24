Each .py file represents a AWS Lambda function, 1 for each venue as well as a Notify which is for email dispatch.

Each Function inherets the dependencies from Layer at runtime


Requests:
arn:aws:lambda:us-east-2:770693421928:layer:Klayers-python38-requests:3 


BS4:
arn:aws:lambda:us-east-2:770693421928:layer:Klayers-python38-beautifulsoup4:3


## TODO:
Unify Date format
Unify UID to artist_date_venue
add aditional field like ticket Url

Add notify function upon DB updates


Updateable Artist list
Warnings when low number of gigs
