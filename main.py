import sys
import requests
from pytrends.request import TrendReq
import json
def main(list_key):
    keywords =list_key
    Time_Frame = 'today 1-m'
    geo = 'TW'
    cat = 0
    pytrend = TrendReq(hl='en-US', tz=360)

    pytrend.build_payload(
            kw_list=keywords,
            cat=cat,
            timeframe=Time_Frame,
            geo=geo,
            gprop='')
    interest_over_time_df = pytrend.interest_over_time()
    # print(interest_over_time_df)
    preload = json.loads(
            interest_over_time_df.to_json(orient='table'))['data']
    for i in range(len(preload)):
        del preload[i]['isPartial']
    # result = preload  # 一段時間內的趨勢
    json_list=[]
    my_dict = {"company":[],"count":[],"date":[]}
    
    result = preload[len(preload)-2]  # 最新的趨勢
    for i in result:
        if i !="date":
            my_dict["company"]=i
            my_dict["count"]=result[i]
            my_dict["date"]=result['date']
            json_list.append(my_dict)
            my_dict = {"company":[],"count":[],"date":[]};
    json_list=json.dumps(json_list)
    # print(json_list)

    headers={'content-type': 'application/json'}
    url = 'https://cloud-11-backend.herokuapp.com/api/trends/'
    r = requests.post(url, data = json_list, headers=headers)
    print(r)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    list_key=[]
    for i in range(1,len(sys.argv)):
        list_key.append(sys.argv[i])
    main(list_key)