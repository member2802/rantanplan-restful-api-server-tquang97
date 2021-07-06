# Rantanplan RESTful API Server

`Rantanplan` is a mobile application used to sniff Wi-Fi access points while the mobile device is in a stationary position. The list of these Wi-Fi access points, and their respective signal strength, constitute a unique signature of the place (restaurant, shop, etc.) where the mobile device is detected.

Rantanplan's server platform maintains a database of places. Each place is identified with a name, a postal address, and a list of Wi-Fi access points detectable at this location.

## Waypoint 1: Design Entity-Relationship Diagram (ERD)

A place is a location defined with a **name** and a **formatted address** (e.g., postal address).

_Note: The best would be that the formatted address of the place is available in different languages (or **locales**), where the default language is English. The current version of the RESTful API doesn't support this feature, but we might want to include this feature in a further version of our RESTful API._

The result of a scan operation performed by the Rantanplan mobile application and sent to the RESTful API server corresponds to the following information:

- Time when this scan operation has started.
- Time when this scan operation has completed.
- Number of rounds performed during this scan operation.
- An array of Wi-Fi access points that have been scanned:
  - Basic Service Set Identifier (BSSID) that uniquely identifies the Wi-Fi access point.
  - Service Set Identifier (SSID) of the Wi-Fi access point, a human-readable name.
  - Frequency in MHz of the channel over which the mobile device was communicating with the Wi-Fi access point.
  - The median value of the detected signal levels in dBm of the Wi-Fi access point.
  - Number of times the Wi-Fi access point has been detected during the scan operation.

A scan operation is associated with a place.

Download the last version of the application [`Navicat Data Modeler Essentials`](https://www.navicat.com/download/navicat-data-modeler-essentials) that supports basic features to easily create data model.

Design the logical data model that provides details of each data entity and the relationships between these data entities. This model is developed independently of the specific database management system into which it can be implemented.

## Waypoint 2: Store Wi-Fi Access Point Scan Result

The RESTful API supports the endpoint `/place/signal` and `/place/<place_id>/signal` that allows the Rantanplan mobile application to `POST` the result of a scan operation.

The endpoint `/place/signal` is used when place is not registered. The Rantanplan server platform will create a new place and return the identification to the mobile application. The mobile application MUST have passed the attributes `place_name` and `place_address` in the JSON expression.

The endpoint `/place/<place_id:string>/signal` is used when the place is identified with `place_id`.

Both these endpoints requires the Rantanplan mobile application to pass the following JSON expression in the body message of the HTTP request:

```json
{
  "start_time": timestamp,
  "end_time": timestanp,
  "round_count": integer,
  "signals": [
    {
      "bssid": string,
      "ssid": string,
      "frequency": integer,
      "signal_level": integer,
      "sample_count": integer
    },
    ...
  ]
}
```

where:

- `place_name` (optional): The name of the place. This attribute must be passed if the place is not identified.
- `place_address` (optional): The formatted address of the place. This attribute must be passed if the place is not identified.
- `start_time` (required): Time when this scan operation has started.
- `end_time` (required): Time when this scan operation has completed.
- `round_count` (required): Number of rounds performed during this scan operation.
- `signals` (required): An array of Wi-Fi access points that have been scanned.
  - `bssid` (required): Basic Service Set Identifier (BSSID) that uniquely identifies the Wi-Fi access point.
  - `ssid` (required): Service Set Identifier (SSID) of the Wi-Fi access point, a human-readable name.
  - `frequency` (required): Frequency in MHz of the channel over which the mobile device was communicating with the Wi-Fi access point.
  - `signal_level` (required): The median value of the detected signal levels in dBm of the Wi-Fi access point.
  - `sample_count` (required): Number of times the Wi-Fi access point has been detected during the scan operation.

For example:

```json
{
  "start_time": "2017-09-26T16:44:53.231+02",
  "end_time": "2017-09-26T16:45:05.191+02",
  "round_count": 5,
  "signals": [
    {
      "bssid": "c4:6e:1f:95:46:84",
      "ssid": "LongHang",
      "frequency": 2462,
      "signal_level": -90,
      "sample_count": 5
    },
    {
      "bssid": "88:d2:74:fa:a2:1b",
      "ssid": "Alex",
      "frequency": 2462,
      "signal_level": -81,
      "sample_count": 5
    },
    {
      "bssid": "10:fe:ed:0f:f8:49",
      "ssid": "N3T",
      "frequency": 2412,
      "signal_level": -52,
      "sample_count": 5
    },
    {
      "bssid": "c4:6e:1f:0d:41:50",
      "ssid": "AN PHU CORP",
      "frequency": 2462,
      "signal_level": -95,
      "sample_count": 2
    },
    {
      "bssid": "88:d2:74:e5:90:f9",
      "ssid": "Hawon",
      "frequency": 2447,
      "signal_level": -97,
      "sample_count": 3
    }
  ]
}
```

The RESTful API returns a JSON expression:

```json
{
  "place_id": string
}
```

where:

- `place_id`: Identification of the place that the mobile has scanned Wi-Fi access points nearby.

Implement these two endpoints with [`Flask`](https://flask.palletsprojects.com/), or the extension [`Flask-RESTX`](https://flask-restx.readthedocs.io/en/stable/) that [brings Swagger UI for all the API](https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f).

The RESTful API server stores the information in its database management system.

## Waypoint 3: Find Places with Wi-Fi Access Point Scan Result

Implement the HTTP method `POST` for the endpoint `/place/search`, which allows a client application to search for places that best match a Wi-Fi access point scan result passed in the body message of the request as a JSON expression:

```json
[
  {
    "bssid": string,
    "signal_level": integer
  },
  ...
]
```

For example:

```json
[
  {
    "bssid": "c4:6e:1f:95:46:84",
    "signal_level": -90
  },
  {
    "bssid": "88:d2:74:fa:a2:1b",
    "signal_level": -81
  },
  {
    "bssid": "10:fe:ed:0f:f8:49",
    "signal_level": -52
  },
  {
    "bssid": "c4:6e:1f:0d:41:50",
    "signal_level": -95
  },
  {
    "bssid": "88:d2:74:e5:90:f9",
    "signal_level": -97
  }
]
```

```bash
$ curl -X GET /place/search
     -H "Content-Type: application/json"
     -H "X-API-Key: f52ce42ac87f11e98e0d0008a20c190f" \
     -H "X-API-Sig: AIzaSyANQixZzt6a_p30YpJ9WY4rkg_svc3IbMU" \
     -d '[{"bssid":"c4:6e:1f:95:46:84","signal_level":-90},{"bssid":"88:d2:74:fa:a2:1b","signal_level":-81},{"bssid":"10:fe:ed:0f:f8:49","signal_level":-52},{"bssid":"c4:6e:1f:0d:41:50","signal_level":-95},{"bssid":"88:d2:74:e5:90:f9","signal_level":-97}]'
```

The RESTful API returns a list of places that best match the collected signals:

```json
[
  {
    "place_id": string,
    "place_name": string,
    "place_address": string,
    "score": decimal
  },
  ...
]
```

Where `score` is an estimation of the probability that the place is relevant to the search. A perfect precision score of `1.0` means that the place returned is totally relevant.

## Waypoint 4: Monitor the Performance of the Endpoints

In his book [Usability Engineering](https://www.nngroup.com/books/usability-engineering/) (1993), Jakob NIELSEN provided the following [basic advice regarding response times](https://www.youtube.com/watch?v=rDOVYO5aMSg&feature=emb_logo), which has been about the same for thirty years:

- **0.1 second** is about the limit for having the user feel that the system is reacting instantaneously, meaning that no special feedback is necessary except to display the result.
- **1.0 second** is about the limit for the user's flow of thought to stay uninterrupted, even though the user will notice the delay. Normally, no special feedback is necessary during delays of more than 0.1 but less than 1.0 second, but the user does lose the feeling of operating directly on the data.
- **10 seconds** is about the limit for keeping the user's attention focused on the dialogue. For longer delays, users will want to perform other tasks while waiting for the computer to finish, so they should be given feedback indicating when the computer expects to be done. Feedback during the delay is especially important if the response time is likely to be highly variable, since users will then not know what to expect.

These figures apply to Web or mobile applications that handle direct interactions with the user through a graphical interface, also known as the User Interface (UI). Because a Web service provides the data to be displayed by those applications, its response time has to be even faster. We define the following levels of performance:

| Response Time (ms) | Level of Performance |
| ------------------ | -------------------- |
| `]0, 50]`          | Excellent            |
| `]50, 100]`        | Good                 |
| `]100, 200]`       | Fair                 |
| `]200, 500]`       | Poor                 |
| `[500, ∞[`         | Bad                  |

The **Response Time** refers to the time delta between the instant the RESTful API server receives a request and the instant this RESTful API server returns the result of its computation (also known as **Processing Time**).

The **Latency** refers to the time delta between the instant the client application sends the request to the RESTful API server and the instant this client application receives the response. This duration includes the time the request and its response takes to travel back and forth over the network between the client application and the RESTful API server. The **Latency** corresponds to **Response Time** plus the **Network Time**.

Integrate [Flask Monitoring Dashboard](https://github.com/flask-dashboard/Flask-MonitoringDashboard) to monitor the performance of your RESTful API server.

Determine the **Performance Baseline**, that is the average response times for the 2 endpoints that your RESTful API server can consistently sustain at the maximum throughput (i.e., under expected/normal load). Technically speaking, this can be defined as pure performance testing. Baseline testing examines how a system performs and creates a baseline with which other types of tests can be compared.

## Waypoint 5: Load Test the RESTful API Server

Performance APi

[jMeter](https://www.youtube.com/watch?v=RrQx_tmUosY)
[Tsung]
