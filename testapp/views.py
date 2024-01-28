from testapp import app
from flask import render_template, request
from random import randint

@app.route('/')
def index():
    my_dict = {
        "insert_something1":'views.pyのinsert_something1部分です',
        "insert_something2":'views.pyのinsert_something2部分です',
        'test_titles':['title1','title2','title3','title4','title5']}
    return render_template('testapp/index.html', my_dict=my_dict)

@app.route('/test')
def other1():
    return render_template('testapp/index2.html')

@app.get('sampleform')
@app.post('/sampleform')
def sampleform():
    if request.method == 'GET':
        return render_template('testapp/sampleform.html')
    if request.method == 'POST':
        hands={'0':'グー', '1':'チョキ', '2':'パー'}
        janken_mapping = {'draw':'引き分け', 'win':'勝ち', 'lose':'負け'}
        player_hand_ja = hands[request.form['janken']]
        player_hand = int(request.form['janken'])
        enemy_hand = int(randint(0, 2))
        enemy_hand_ja = hands[str(enemy_hand)]
        if player_hand == enemy_hand:
            judgement = 'draw'
        elif enemy_hand - player_hand == 1 or enemy_hand - player_hand == -2:
            judgement = 'win'
        else:
            judgement = 'lose'
        print(f'じゃんけん開始。enemy_hand:{enemy_hand}  player_hand:{player_hand} 結果:{judgement}')
        result = {
            'enemy_hand_ja':enemy_hand_ja,
            'player_hand_ja':player_hand_ja,
            'judgement':janken_mapping[judgement]
        }
        return render_template('testapp/janken_result.html', result=result)
