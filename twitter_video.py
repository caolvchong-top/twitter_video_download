import re
import os
import requests
import json
from fake_useragent import UserAgent


def video_download(video_id:str):
    url='https://twitter.com/i/api/graphql/BoHLKeBvibdYDiJON1oqTg/TweetDetail?variables={"focalTweetId":"'+video_id+'","with_rux_injections":false,"includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true}&features={"responsive_web_twitter_blue_verified_badge_is_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_uc_gql_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":true}'
    ua=UserAgent()

    #读取cookies
    if not os.path.exists('cookies.txt') or os.path.getsize('cookies.txt')==0:
        print('\n==>请检查程序目录下cookies.txt文件是否存在，并将cookie粘贴在文件内...<==')
        return
    else:
        with open('cookies.txt','r') as f:
            cookies=f.readlines()[0]
            f.close()
    re_token='ct0=(.*?);'
    ct0=re.findall(re_token,cookies)[0]

    headers={
        'user-agent':ua.random,
        'authorization':'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'cookie':cookies,
        'x-csrf-token':ct0,
        }

    #开始获取该视频推文信息
    try:
        response=requests.get(url,headers=headers)
    except Exception as e:
        print('\n==>大概是网络有问题，请检查一下...<==')
        return
    if response.status_code==403:
        print('\n==>大概是cookie过期了，请在cookies.txt文件中更新一下cookie...<==')
        return
    raw_data=json.loads(response.text)
    #print(raw_data)
    #提取视频真实地址
    try:
        video_url_lst=raw_data['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]['video_info']['variants']
    except Exception as e:
        print('\n==>未提取到视频链接，请检查这篇推文内是否 真的 包含有视频内容//或是推特的格式变了...<==')
        return
    bitrate_lst=[x['bitrate'] if 'bitrate' in x else 0 for x in video_url_lst]    #有时候列表中会有个content_type的玩意儿,要排除
    video_url=video_url_lst[bitrate_lst.index(max(bitrate_lst))]['url']        #默认下载最大（清晰度最高）的视频，如有其他需要请自行修改这一行
    
    #开始下载视频
    file_name=video_id+'.mp4'
    print('\n开始下载视频...')
    response=requests.get(video_url,headers=headers).content
    with open(file_name,'wb') as f:
        f.write(response)
        f.close()
    print('\n下载完成,请在程序目录下查看...')
    return

#Test
print('运行前请确认网络可用，以及cookies.txt文件的存在...\n')
video_id=input('视频推文的ID(https://.../status/后面跟的那一串数字):')
video_download(video_id)


