
import string
from matplotlib.pyplot import pause
from numpy import not_equal
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
reports = f"/reports/"
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
        if args.output:    
            file = open('output.json', 'w')
            file.write(str(response))
            file.close()
            
        else:
            pass

        i = 0
        data_set = []
        base = len(data)
        while i is not base:
            try: 
                link = data[i]
            except IndexError:
                pass
            i = i + 1
            data_set.append(link)
            id = link['id']
            title = link['attributes']['title']
            try:
                state = link['attributes']['state']
            except KeyError:
                state = "No data found" 
            try:
                date_created = link['attributes']['created_at']
            except KeyError:
                date_created = "No data found"
            try:
                severity = link['relationships']['severity']['data']['attributes']['rating']
            except KeyError:
                severity = "No data found"
            try:
                reporter = link['relationships']['reporter']['data']['attributes']['username']
            except KeyError:
                reporter = "No data found"
            try:
                weakness = link['relationships']['weakness']['data']['attributes']['name']
            except KeyError:
                weakness = "No data found"
            try:
                payment = link['relationships']['bounties']['data']
            except KeyError:
                payment = "No data found"
        
            try:
                a_identifier = link['relationships']['structured_scope']['data']['attributes']['asset_identifier']
            except KeyError:
                a_identifier = "No data found"
            print("__________________________________\n")
            print(f"ID: {id}\t Severity:\t{severity} \nURL:\t{a_identifier}\nTitle: {title}\nReporter: {reporter}\nState: {state}\tDate Created: {date_created}\nWeakness: {weakness}\nPayout: {payment}\n")


if __name__ == '__main__':
    get_reports()
            


