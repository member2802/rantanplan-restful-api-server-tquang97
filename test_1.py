import requests
import json
import random

i=1

while i < 1000000:

    url = "http://127.0.0.1:5000/place/signal"
    # url1 = "http://127.0.0.1:5000/place/{}/signal".format(i)
    url2 = "http://127.0.0.1:5000/place/search"

    data = json.dumps(
                    {
                    "place_name":"NAME{}".format(i), 
                    "place_address":"ADDRESS", 
                    "start_time":"2020-07-30T04:49:00.287Z",
                    "end_time":"2020-07-30T04:49:26.076Z",
                
                    "round_count":5, 
                    "signals":[ 
                        {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                        "frequency":2462,
                        "sample_count":4,
                        "signal_level":-65,
                        "ssid":"Internet-VP2"}, 
                        {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                        "frequency":2452,
                        "sample_count":5,
                        "signal_level":-75,
                        "ssid":"Pharmacity-Office"}, 
                        {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                        "frequency":2452,
                        "sample_count":5,
                        "signal_level":-75,
                        "ssid":"Pharmacity-Office"}, 
                        {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                        "frequency":2452,
                        "sample_count":5,
                        "signal_level":-75,
                        "ssid":"Pharmacity-Office"}, 
                        {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                        "frequency":2452,
                        "sample_count":5,
                        "signal_level":-75,
                        "ssid":"Pharmacity-Office"}
                        ], 
                    })
    data_id = json.dumps(
                    {   
                        "place_name":"NAME{}".format(i),
                        "place_address":"place123",
                        "start_time": "2017-09-26T16:44:53.231+02",
                        "end_time": "2017-09-26T16:45:05.191+02",
                        "round_count": 5,
                        "signals": [
                            {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                            "frequency":2462,
                            "sample_count":4,
                            "signal_level":random.randrange(-100, -1),
                            "ssid":"Internet-VP2"
                            }, 
                            {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                            "frequency":2452,
                            "sample_count":5,
                            "signal_level":random.randrange(-100, -1),
                            "ssid":"Pharmacity-Office"
                            }, 
                            {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                            "frequency":2452,
                            "sample_count":5,
                            "signal_level":random.randrange(-100, -1),
                            "ssid":"Pharmacity-Office"
                            }, 
                            {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                            "frequency":2452,
                            "sample_count":5,
                            "signal_level":random.randrange(-100, -1),
                            "ssid":"Pharmacity-Office"
                            }, 
                            {"bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                            "frequency":2452,
                            "sample_count":5,
                            "signal_level":random.randrange(-100, -1),
                            "ssid":"Pharmacity-Office"
                            }
                        ]
                    })    
    data_search = json.dumps(
        {"signals":[
                {
                    "bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                    "signal_level": -65
                },
                {
                    "bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                    "signal_level": -75
                },
                {
                    "bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                    "signal_level": -65
                },
                {
                    "bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                    "signal_level": -75
                },
                {
                    "bssid":"02:e0:4c:d2:91:3{}".format(random.randrange(1, 10)),
                    "signal_level": -65
                }
            ]
        }
    ) 

    headers = {
      'Content-Type': 'application/json'
    }

    # response = requests.request("POST", url, headers=headers, data = data)

    # response1 =  requests.request("POST", url1, headers=headers, data = data_id)
          
    response2 = requests.request("POST", url2, headers=headers, data = data_search)
    
    i+=1
    print(i)