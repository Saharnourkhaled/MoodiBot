from urllib.request import urlopen
import requests
import json
import random
import secretToken

def get_mood_quote(mood):
    request_url = 'https://favqs.com/api/quotes/'
    params = dict(
        filter = mood,
        type = 'tag'
    )

    pullme = requests.get(url=request_url, headers={'Authorization': 'Token token={secretToken}'}.format(secretToken), params=params)
    length_of_results = len(pullme.json()['quotes']) - 1
    random_index = random.randint(0, length_of_results)
    quote = pullme.json()['quotes'][random_index]['body']
    author = pullme.json()['quotes'][random_index]['author']
    quote_output = '"{}" ~ {}'.format(quote, author)
    return quote_output


def rps(user_input):
    message = 'I play {}, '
    result = ''
    ai_num = random.randint(0,2)
    rps_dict = {0:'rock', 1:'paper', 2:'scissors'}
    for i in rps_dict:
        if user_input == rps_dict[i]:
            user_num = i
    if user_num == ai_num:
        return message.format(rps_dict[ai_num]) + 'it\'s a tie!'
    elif ((user_num - ai_num + 3) % 3) == 1:
        return message.format(rps_dict[ai_num]) + 'you win!'
    else:
        return message.format(rps_dict[ai_num]) + 'I win! :D'

def youtube_list(user_mood):
    moto_list = ['https://www.youtube.com/watch?v=8aRor905cCw&index=2&list=PLkBnz4liFlLLSa3fj01dLF0OfWwEBqsU4', 'https://www.youtube.com/watch?v=A66_4_4eyVg', 'https://www.youtube.com/watch?v=Sv6dMFF_yts&list=PLvPjBbFpr-O1azdoLQpxSt9nX5twB3kky']
    calm_list = ['https://www.youtube.com/watch?v=hHW1oY26kxQ', 'https://www.youtube.com/watch?v=aJOTlE1K90k&list=PL4QNnZJr8sRPmuz_d87ygGR6YAYEF-fmw', 'https://www.youtube.com/watch?v=jO2viLEW-1A&list=PLMmqTuUsDkRICG_7HkmgGV081DGDjEFxe']
    rand_pick = random.randint(0,2)
    
    if user_mood == 'happy' or 'sad' or 'motivation':
        return moto_list[rand_pick]
    if user_mood == 'anger' or 'neutral':
        return calm_list[rand_pick]

def lambda_handler(event, context):
    content_output: ""
    user_intent = event['currentIntent']['name']
    
    if user_intent == 'GetMood':
        user_mood = event['currentIntent']['slots']['Emotion']
        content_output = get_mood_quote(user_mood)
        
        
    if user_intent == 'RockPaperScissors':
        player_hand = event['currentIntent']['slots']['PlayerHand']
        content_output = rps(player_hand)

    if user_intent == 'YouTubePlaylist':
        youtube_mood = event['currentIntent']['slots']['Youtube']
        content_output = youtube_list(youtube_mood)

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": content_output
            },
        }
    }

    return response
    
