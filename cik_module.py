# Name:Ernest Azukaeme
# Project CIK lookup

import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl     = fileurl
        self.name_dict   = {}
        self.ticker_dict = {}

        headers = {
            'user-agent': 'MLT CP tejiriaeducation@gmail.com'
        }
        r = requests.get(self.fileurl, headers=headers)

        self.filejson = r.json()


        print(r.text)
        self.filejson = r.json()
        print(self.filejson)

        # Building the lookup table
        self.cik_json_to_dict()

# Fills name_dict and tciket_dict dictinaniers using data from the json files
    def cik_json_to_dict(self):
        self.name_dict   = {}
        self.ticker_dict = {}
        for value in self.filejson.values():
            cik = value["cik_str"]
            name = value["title"]
            ticker = value["ticker"]
            self.name_dict[name] = cik
            self.ticker_dict[ticker] = cik

# Returns the CIK for a given name
    def name_to_cik(self, name: str):
        key = name.strip().upper()
        return self.name_dict.get(key, None)

# Returns the CIK for a given ticker
    def ticker_to_cik(self, ticker: str):
        key = ticker.strip().upper()
        return self.ticker_dict.get(key, None)

# instantiate and run
se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

print(se.ticker_to_cik('AAPL'))
