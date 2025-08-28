import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl     = fileurl
        self.name_dict   = {}
        self.ticker_dict = {}

        headers = {
            'user-agent': 'YourCompany your_email@domain.com'
        }
        r = requests.get(self.fileurl, headers=headers)

        self.filejson = r.json()


        print(r.text)
        self.filejson = r.json()
        print(self.filejson)

        # build our lookup tables
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

print(se.ticker_to_cik('NVDA'))

import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.name_dict = {}
        self.ticker_dict = {}
        self.headers = {"User-Agent": "MyApp/1.0 (me@example.com)"}

        r = requests.get(self.fileurl, headers=self.headers)
        r.raise_for_status()
        self.filejson = r.json()
        self.cik_json_to_dict()

    def cik_json_to_dict(self):
        """Fill name_dict and ticker_dict from SEC company_tickers.json"""
        for value in self.filejson.values():
            cik = str(value["cik_str"]).zfill(10)
            name = value["title"].upper()
            ticker = value["ticker"].upper()
            self.name_dict[name] = cik
            self.ticker_dict[ticker] = cik

    def name_to_cik(self, name: str):
        return self.name_dict.get(name.upper().strip())

    def ticker_to_cik(self, ticker: str):
        return self.ticker_dict.get(ticker.upper().strip())

    def _get_filings(self, cik):
        """Fetch a company's recent filings JSON by CIK."""
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()["filings"]["recent"]

    def annual_filing(self, cik, year):
        """Get 10-K filing URL for given year."""
        filings = self._get_filings(cik)
        for form, date, acc, doc in zip(
            filings["form"], filings["filingDate"],
            filings["accessionNumber"], filings["primaryDocument"]
        ):
            if form == "10-K" and date.startswith(str(year)):
                return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}"
        return None

    def quarterly_filing(self, cik, year, quarter):
        """Get 10-Q filing URL for given year and quarter (Q4 → 10-K)."""
        if quarter == 4:
            return self.annual_filing(cik, year)
        filings = self._get_filings(cik)
        for form, date, acc, doc in zip(
            filings["form"], filings["filingDate"],
            filings["accessionNumber"], filings["primaryDocument"]
        ):
            if form == "10-Q" and date.startswith(str(year)):
                month = int(date.split("-")[1])
                if (month - 1)//3 + 1 == quarter:
                    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}"
        return None


# Example usage
if __name__ == "__main__":
    se = SecEdgar("https://www.sec.gov/files/company_tickers.json")
    cik = se.ticker_to_cik("NVDA")
    print("CIK for NVDA:", cik)
    print("NVDA 2024 10-K:", se.annual_filing(cik, 2024))
    print("NVDA 2023 Q2 10-Q:", se.quarterly_filing(cik, 2023, 2))
