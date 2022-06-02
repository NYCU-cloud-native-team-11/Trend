import sys
import requests
from pytrends.request import TrendReq
import json
import datetime


def get_input(argv_lists):
    if len(argv_lists) < 2:
        print("please input at least one arguments")
        sys.exit(1)
    list_key = []
    for i in range(len(argv_lists)):
        if i != 0:
            list_key.append(argv_lists[i])
    return list_key


def upload_data(url, json_list):
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json_list, headers=headers)
    return r


def res_process(res):
    if res.status_code == 200:
        print("upload success")
        sys.exit(0)
    else:
        print("upload failed")
        sys.exit(1)


def get_trend(list_key):
    keywords = list_key
    Time_Frame = 'now 1-d'
    geo = ''
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
    json_list = []
    my_dict = {"company": [], "count": [], "date": []}

    result = preload[len(preload)-1]  # 最新的趨勢
    for i in result:
        if i != "date":
            my_dict["company"] = i
            my_dict["count"] = result[i]
            my_dict["date"] = result['date'].split('T')[0]
            json_list.append(my_dict)
            my_dict = {"company": [], "count": [], "date": []}
    json_list = json.dumps(json_list).replace("[", "").replace("]", "")
    # print(json_list)
    return json_list


def main(list_key):
    url = 'https://cloud-11-backend.herokuapp.com/api/trends/'
    json_list = get_trend(list_key)
    res = upload_data(url, json_list)
    res_process(res)


if __name__ == '__main__':
    list_key = get_input(sys.argv)
    main(list_key)
