
from matplotlib.pyplot import pause
import requests
import json
from requests.auth import  HTTPBasicAuth
import argparse

#build arguments menu
parser = argparse.ArgumentParser(description='Hackerone API connector.', fromfile_prefix_chars='@')
parser._optionals.title = "OPTIONS"
parser.add_argument('-a', '--api-key', type=str, help='API key for hackerone authentication.')
parser.add_argument('-u', '--user', help ='hackerone username for authentication')
parser.add_argument('-f', '--filter', help ='platform filter for hackerone api. usually company name.')
parser.add_argument('-o','--output', default='output', help='optional ouput name to prepend to scan outputs.')
args = parser.parse_args()


#build api auth
username = args.user
API_ENDPOINT = 'https://api.hackerone.com/v1'
reports = '/reports'
filter = f"?filter[program][]={args.filter}"

API_KEY = args.api_key

headers = {

           'Accept': "application/json",

}

class get_reports():
    '''class to query Hackerone API for reports'''
    def __init__(self):
        url = API_ENDPOINT + reports + filter
        r = requests.get(url, auth=HTTPBasicAuth(username, API_KEY), headers=headers)
        response = r.json()
        try:
            data = response['data']
        except KeyError:
            print("most likely auth error")
            pause
        file = open('output.json', 'w')
        file.write(str(data))
        file.close()
        base = data
        top = len(base)
        i = 0
        data_set = []
        while i is not top:
            link = data[i]
            i = i + 1
            data_set.append(link)
            id = link['id']
            title = link['attributes']['title']
            state = link['attributes']['state']
            date_created = link['attributes']['created_at']
            severity = link['relationships']['severity']['data']['attributes']['rating']
            try:
                a_identifier = link['relationships']['structured_scope']['data']['attributes']['asset_identifier']
            except KeyError:
                a_identifier = "NULL"
            print("__________________________________\n")
            print(f"ID: {id}\t Severity:\t{severity} \nURL:\t{a_identifier}\nTitle: {title}\nState: {state}\tDate Created: {date_created}\n\n\n")
           

if __name__ == '__main__':
    get_reports()
            


