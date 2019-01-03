

def user_to_channelid(user_name, api_key="AIzaSyCzerFuw3AJr6o29InSBHBW9Rfy5xzIyTY"):
    '''
    유튜브 채널 도메인이 'youtube.com/user/xxxx' 일 경우,
    'xxxx' 부분을 user_name에 넣어주면 고유 채널 ID값을 반환해줍니다.
    return => 채널 고유 ID
    '''
    import requests
    from bs4 import BeautifulSoup 

    target_url = '''https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={}&key={}'''.format(user_name, api_key) 

    html = requests.get (target_url)
    soup = BeautifulSoup (html.text, "html.parser" )
    api_dict = eval(soup.text.replace("false","False").replace("true","True"))
    channel_id = api_dict['items'][0]["id"]
    
    return channel_id