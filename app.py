from boggle import Boggle
from flask import Flask, session, request, render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "nice_try"

boggle_game = Boggle()

@app.route('/')
def gen_board():
    """Generates game board."""

    game_board = boggle_game.make_board()
    session['game_board'] = game_board
    h_score = session.get('h_score', 0)
    play_count = session.get('play_count', 0)
    
    return render_template('index.html', game_board = game_board, h_score = h_score, play_count = play_count)

@app.route('/validate-word')
def validate_word():
    """Confirm that word is in words dict"""
    
    word = request.args['word']
    game_board = session['game_board']
    res = boggle_game.check_valid_word(game_board, word)
    
    return jsonify({'result': res})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Gets current score and updates play_count and h_score if a new h_score is reached"""
    
    h_score = session.get('h_score', 0)
    play_count = session.get('play_count', 0)
    score = request.json['score']
    
    session['h_score'] = max(score, h_score)
    session['play_count'] = play_count + 1
    
    return jsonify(newHScore = score > h_score)