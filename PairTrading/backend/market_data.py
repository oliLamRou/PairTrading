import requests
import warnings

class MarketData:
    def __init__(self, base_url):
        self.base_url = base_url

    def requests_results(self, url: str) -> dict:
        #400 bad requests
        #404 wrong
        #429 too many requests
        #200 good

        r = requests.get(self.base_url + url)

        status_code = r.status_code
        if not status_code == 200:
            warnings.warn(message=f'Requests code: {status_code}', category=Warning, stacklevel=2)

        #NOTE: .get will probaly not work with other API
        results = r.json().get('results')

        return results, status_code

    def format_results(self,
            row: dict, 
            columns_type: dict
        ) -> dict:

        results_ = {}
        for k, v in row.items():
            column = columns_type.get(k)
            if not column:
                print(f'Column: {k} does exist. It will be skipped.\n')
                continue

            column_name = column[0]
            column_type = column[1]
            if column_type == 'INTERGER':
                results_[column_name] = int(v)
            elif column_type == 'REAL':
                results_[column_name] = float(v)
            else:
                results_[column_name] = str(v)

        return results_

    def requests_and_format(self, url, columns):
        results, status_code = self.requests_results(url)
        if not status_code == 200:
            return

        if type(results) == list:
            return [self.format_results(result, columns) for result in results]
        else:
            return self.format_results(results, columns)

if __name__ == '__main__':
    m = MarketData('')