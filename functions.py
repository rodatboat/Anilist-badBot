import requests
import json
import random
import os
import time

info = json.loads(open("config.json").read())
SESSION_KEY = info['token']
SELF_ID = info['id']

clear = lambda: os.system('cls')

def getFollowerCount():
    cont = True
    count = 1
    totalF = 0
    while(cont):
        url = "https://graphql.anilist.co"
        cookies = {'laravel_session': SESSION_KEY}
        params = {"query":"query($id:Int!,$page:Int){Page(page:$page){pageInfo{total perPage currentPage lastPage hasNextPage}followers(userId:$id,sort:USERNAME){id name avatar{large}}}}","variables":{"id":SELF_ID,"type":"followers","page":count}}


        r = requests.post(url, cookies=cookies, json=params)
        raw = r.json()
        followers = raw['data']['Page']['followers']

        if len(followers) == 0:
            cont = False
        else:
            totalF+=len(followers)
        count+=1

    print(f"\nUser {SELF_ID} currently has {totalF} followers.\n")

def getFollowingCount():
    cont = True
    count = 1
    totalF = 0
    while(cont):
        url = "https://graphql.anilist.co"
        cookies = {'laravel_session': SESSION_KEY}
        params = {
            "query": "query($id:Int!,$page:Int){Page(page:$page,perPage:100){pageInfo{total perPage currentPage lastPage hasNextPage}following(userId:$id,sort:USERNAME){id name avatar{large}}}}",
            "variables": {"id": SELF_ID, "type": "following", "page": count}}

        r = requests.post(url, cookies=cookies, json=params)
        raw = r.json()
        following = raw['data']['Page']['following']

        if len(following) == 0:
            cont = False
        else:
            totalF+=len(following)
        count+=1

    print(f"\nUser {SELF_ID} currently follows {totalF}.\n")

def toggleFollow(id, count):
    url = "https://graphql.anilist.co"
    cookies = {'laravel_session':SESSION_KEY}
    params = {"query":"mutation($id:Int){ToggleFollow(userId:$id){id name isFollowing}}","variables":{"id":id}}

    r = requests.post(url, cookies=cookies, json=params)

    if r.status_code == 200:
        print(f"Toggled Follow on user {id}  \t\t#{count+1}")
    else:
        print(f"FAILED ON USER {id} ERROR: {r.status_code}")
        time.sleep(30)

def getIds(numpp):
    count = 0
    if round(int(numpp)/50) > int(numpp)/50:
        count = round(int(numpp))
    else:
        count = round(int(numpp)/50)+1
    cont = True

    while cont:
        url = "https://graphql.anilist.co"
        cookies = {'laravel_session': SESSION_KEY}
        params = {"query":"query($isFollowing:Boolean = true,$activityType:ActivityType,$page:Int){Page(page:$page,perPage:50){pageInfo{total perPage currentPage lastPage hasNextPage}activities(isFollowing:$isFollowing type:$activityType type_in:[TEXT,ANIME_LIST,MANGA_LIST]sort:ID_DESC){... on TextActivity{id userId type replyCount text isLocked isSubscribed isLiked likeCount createdAt user{id name donatorTier donatorBadge avatar{large}}}... on ListActivity{id userId type status progress replyCount isLocked isSubscribed isLiked likeCount createdAt user{id name donatorTier donatorBadge avatar{large}}media{id type status isAdult title{userPreferred}bannerImage coverImage{large}}}}}}","variables":{"page":count,"type":"global","filter":"all","isFollowing":False}}
        #params = {"query":"query($isFollowing:Boolean = true,$hasReplies:Boolean = false,$activityType:ActivityType,$page:Int){Page(page:$page,perPage:"+ str(numpp) +"){pageInfo{total perPage currentPage lastPage hasNextPage}activities(isFollowing:$isFollowing type:$activityType hasRepliesOrTypeText:$hasReplies type_in:[TEXT,ANIME_LIST,MANGA_LIST]sort:ID_DESC){... on TextActivity{id userId type replyCount text isLocked isSubscribed isLiked likeCount createdAt user{id name donatorTier donatorBadge avatar{large}}}... on ListActivity{id userId type status progress replyCount isLocked isSubscribed isLiked likeCount createdAt user{id name donatorTier donatorBadge avatar{large}}media{id type status isAdult title{userPreferred}bannerImage coverImage{large}}}}}}","variables":{"page":1,"type":"global","filter":"all","isFollowing":False,"hasReplies":True}}
        r = requests.post(url, cookies=cookies, json=params)
        raw = r.json()
        userList = raw['data']['Page']['activities']

        userInfo = {}
        userInfo['allUsers']=[]

        #print(r.status_code)
        #print(len(raw['data']['Page']['activities']))

        for user in userList:
            userInfo['allUsers'].append({'name': user['user']['name'],
                             'userId':user['userId']})
        if count == 1:
            cont = False
        count-=1
    file = open("userList.json", "w")
    json.dump(userInfo, file)

def getFollowing():
    url = "https://graphql.anilist.co"
    cookies = {'laravel_session': SESSION_KEY}
    userInfo = {}
    userInfo['allUsers'] = []
    count = 1
    cont = True
    while cont:
        params = {
            "query": "query($id:Int!,$page:Int){Page(page:$page,perPage:100){pageInfo{total perPage currentPage lastPage hasNextPage}following(userId:$id,sort:USERNAME){id name avatar{large}}}}",
            "variables": {"id": SELF_ID, "type": "following", "page": count}}
        r = requests.post(url, cookies=cookies, json=params)
        raw = r.json()
        following = raw['data']['Page']['following']

        if len(following) == 0:
            cont = False

        file = open("currentlyFollowing.json", "w")
        for user in following:
            userInfo['allUsers'].append({'name':user['name'],
                                         'userId':user['id']})
        count+=1
    json.dump(userInfo, file)

def getFollowers():
    url = "https://graphql.anilist.co"
    cookies = {'laravel_session': SESSION_KEY}
    userInfo = {}
    userInfo['allUsers'] = []
    count = 1
    cont = True
    while cont:
        params = params = {"query":"query($id:Int!,$page:Int){Page(page:$page){pageInfo{total perPage currentPage lastPage hasNextPage}followers(userId:$id,sort:USERNAME){id name avatar{large}}}}","variables":{"id":SELF_ID,"type":"followers","page":count}}
        r = requests.post(url, cookies=cookies, json=params)
        raw = r.json()
        followers = raw['data']['Page']['followers']

        if len(followers) == 0:
            cont = False

        file = open("currentFollowers.json", "w")
        for user in followers:
            userInfo['allUsers'].append({'name':user['name'],
                                         'userId':user['id']})
        count+=1
    json.dump(userInfo, file)

def unfollowRandoms(choice):
    getFollowing()
    usersF = json.loads(open("currentlyFollowing.json").read())
    usersF = usersF['allUsers']

    usersE = json.loads(open("exceptions.json").read())
    usersE = usersE['allUsers']

    if choice == 0:
        for user in usersF:
            if user not in usersE:
                toggleFollow(user['userId'])
    if choice > 0:
        count = choice
        while count > 0:
            user = random.randint(0, len(usersF)-1)
            if usersF[user] not in usersE:
                toggleFollow(usersF[user]['userId'], count-1)
                count-=1

def unfollowTraitors():
    getFollowing()
    usersF = json.loads(open("currentlyFollowing.json").read())
    usersF = usersF['allUsers']

    getFollowers()
    usersCF = json.loads(open("currentFollowers.json").read())
    usersCF = usersCF['allUsers']

    usersE = json.loads(open("exceptions.json").read())
    usersE = usersE['allUsers']

    for user in usersF:
        if user in usersE:
            del user
    for user in usersF:
        if user not in usersCF:
            print(f"Unfollowing {user['name']}")
            toggleFollow(user['userId'], 0)

def followGlobal():
    numpp = input("\nHow many users would you like to follow?")
    getIds(numpp)

    users = json.loads(open("userList.json").read())
    users = users['allUsers']

    getFollowing()
    usersF = json.loads(open("currentlyFollowing.json").read())
    usersF = usersF['allUsers']

    count = 0
    for user in users:
        if not user in usersF:
            if count > int(numpp):
                break
            else:
                toggleFollow(int(user['userId']), count)
                count+=1

def followAllFollowers():
    getFollowers()
    usersCF = json.loads(open("currentFollowers.json").read())
    usersCF = usersCF['allUsers']

    for user in usersCF:
        toggleFollow(user['userId'], 0)
