##### Running locally:
Create and activate virtual environment: 

`virtualenv env`

`source env/bin/activate`

Install requirements:

`pip install -r requirements.txt` 

Obtain API KEY from : http://www.lyricsnmusic.com/api_keys/new

From terminal, input:
`echo "API_KEY=[youractualapikeygoeshere]" > .env`

Run server: 

`python app.py`

Navigate to localhost:5000 in browser to view app.