import requests

def get_last_heart_rate_value(api_url, headers):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        dataset = data.get("activities-heart-intraday", {}).get("dataset", [])
        if dataset:
            last_value = dataset[-1]
            return last_value
        else:
            return None
    else:
        response.raise_for_status()

api_url = "https://api.fitbit.com/1/user/-/activities/heart/date/2024-06-24/1d/1min.json"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BLNFEiLCJzdWIiOiJDNFIzNkwiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNzE5MjkzODkyLCJpYXQiOjE3MTkyNjUwOTJ9.ZkBBNIBIXIy_Rp1m03g0faLDN3aO078l9uz_N263GGc"
}

last_heart_rate_value = get_last_heart_rate_value(api_url, headers)
print(last_heart_rate_value)
