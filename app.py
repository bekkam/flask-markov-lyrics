from flask import Flask, flash, render_template, url_for, redirect, request
import requests
from pymarkovchain import MarkovChain
# in terminal : echo "API_KEY=[youractualapikeygoeshere]" > .env
# Flask can read this special environment file if we add the following 2 lines:
import os

API_KEY = os.environ.get('API_KEY')

# Pass a port number on which to run the app, bc heroku assigns a random port number
PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
app.secret_key = 'development key'
# for heroku
app.config.from_object(__name__)


@app.route('/', methods=['GET'])
def cover():
    """Show the cover page"""

    return render_template('cover.html')


@app.route('/index', methods=['GET'])
def index():
    """Show the index page"""

    return render_template('index.html')


@app.route('/lyrics', methods=['POST'])
def lyrics():

    artist = request.form['artist']
    lines = int(request.form['lines'])

    if not artist:
        flash('All fields required')
        return redirect(url_for('index'))

    lyric_list = query_lyrics_api(artist)
    lyrics = format_as_string(lyric_list)
    result = generate_markov_model(lyrics, lines)

    return render_template('lyrics.html', result=result, artist=artist)


def query_lyrics_api(artist):
    """Return json of artist's lyrics from api"""

    # get response of artist's sample lyrics from api
    uri = "http://api.lyricsnmusic.com/songs"
    params = {
        'api_key': API_KEY,
        'artist': artist,
    }
    response = requests.get(uri, params=params)
    return response.json()


def format_as_string(lyric_list):
    """Given response.json(), formats as a string"""

    # Parse results into a long string of lyrics
    lyrics = ''
    for lyric_dict in lyric_list:
        # for each lyric dict, get value of the snippet key
        # remove trailing '...', and append to lyrics
        lyrics += lyric_dict['snippet'].replace('...', '') + ' '
    return lyrics


def generate_markov_model(lyrics, num_lines):
    """Generate markov chain's language model; return list of generated text"""

    # make markov chain from string of lyrics
    mc = MarkovChain()
    # generate the markov chain's language model, in case it's not present
    mc.generateDatabase(lyrics)
    # mc.generateString()) lets the markov chain generate some text -
    # let markov chain generate text for as many lines as user specifies
    result = []
    for line in range(0, num_lines):
        result.append(mc.generateString())

    return result

if __name__ == '__main__':

    # specify port for heroku
    app.run()
    # app.run(host='0.0.0.0', port=PORT)
