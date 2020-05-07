# -*- coding: utf-8 -*-
import twitter
from scrArrivals import getProd

# twitterAPI情報を記述
auth = twitter.OAuth(consumer_key="**********",
consumer_secret="**********",
token="**********",
token_secret="**********")
t = twitter.Twitter(auth=auth)

msg_arr = getProd()

for i in range(len(msg_arr)):    
    if len(msg_arr[i]) != 0:
        res = t.statuses.update(status = msg_arr[i]) # 取得した情報を投稿する
    
        if res.status_code == 200: #正常投稿出来た場合
            print("Success.")
        else: #正常投稿出来なかった場合
            print("Failed. : %d"% res.status_code)

print('Done')
# ------------------------------------------------------------------
# タイムライン取得
# timelines = t.statuses.home_timeline()
# for timeline in timelines:
#     tl = '({id}) [{username}]:{text}'.format(id=timeline['id'], username=timeline['user']['name'], text=timeline['text'])
#     print (tl)