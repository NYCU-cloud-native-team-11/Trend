from asyncio import protocols
import sys
import requests
from pytrends.request import TrendReq
import json
from datetime import datetime
# import pprint
import calendar
import os
import setting


def get_input(argv_lists):
    if len(argv_lists) < 2:
        print("please input at least one arguments")
        sys.exit(1)
    list_key = []
    for i in range(len(argv_lists)):
        if i != 0:
            list_key.append(argv_lists[i].replace("-", " "))
    # print(list_key)
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
    Time_Frame = 'now 1-H'
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

    preload = json.loads(
        interest_over_time_df.to_json(orient='table'))['data']

    for i in range(len(preload)):
        del preload[i]['isPartial']
    # pprint.pprint(preload)  # for debug
    json_list = []
    for j in range(len(keywords)):
        total_count = 0
        my_dict = {"company": [], "count": [], "date": []}
        company = keywords[j]
        for i in range(len(preload)):
            total_count += preload[i][company]

        my_dict["company"] = company
        my_dict["count"] = total_count
        try:
            time = preload[len(
                preload)-1]['date'].replace("T", " ").replace("Z", "").split(".")[0]
            d = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            ts = calendar.timegm(d.utctimetuple())
            my_dict["date"] = str(datetime.fromtimestamp(ts))
        except:
            time = str(datetime.now())
            d = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            ts = calendar.timegm(d.utctimetuple())
            my_dict["date"] = str(datetime.fromtimestamp(ts))
        json_list.append(my_dict)
    return json.dumps(json_list)


def main(list_key):

    protocol = os.getenv('PROTOCOL')
    host = os.getenv('HOST')
    api = os.getenv('API')
    if protocol == None:
        print("please set PROTOCAL environment variable")
        sys.exit(1)
    if host == None:
        print("please set HOST environment variable")
        sys.exit(1)
    if api == None:
        print("please set API environment variable")
        sys.exit(1)
    url = protocol+"://" + host + api
    json_list = get_trend(list_key)
    # print(json_list)
    res = upload_data(url, json_list)
    res_process(res)


if __name__ == '__main__':
    list_key = get_input(sys.argv)
    main(list_key)
