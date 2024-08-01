import requests 
import re
import csv
import argparse
import json

class Prometheus:
    def __init__(self, args):
        self.PROMETHEUS = args.prometheus_url
        self.BASE_URL = "/prometheus/api/v1"
        with open(args.filter_file, "r") as file:
            self.filters = json.load(file)

    def query(self, endpoint, params):
        response = requests.get(
            self.PROMETHEUS + self.BASE_URL + endpoint,
            params=params
        )

        return response.json()

    def apply_filter(self, names, f):
        r = re.escape(f)
        return filter(lambda n: re.search(r, n) != None, names)

    def get_names(self):
        endpoint = "/label/__name__/values"
        names = self.query(endpoint, {})['data']

        # union over all filters
        filtered_names = list()
        for (name_filter, filter) in self.filters:
            filtered = self.apply_filter(names, name_filter)

            for name in filtered:
                filtered_names.append((name, filter))

        return filtered_names
    
    def get_values(self, name, filters, time):
        endpoint = "/query"
        params = { "query": "{}[{}]".format(name, time) }

        for metric in self.query(endpoint, params)['data']['result']:
            match = True
            for key in filters.keys():
                if key not in metric['metric']:
                    print(f'Query failed: {key} not exist in {metric['metric']}')
                    match = False
                else:
                    if not filters[key] in metric['metric'][key]:
                        match = False
            
            if match:
                return metric['values']

    def get_all_values(self, names, time):
        values = []
        pretty_values = [] 
        pretty_values.append(['time'])

        for (name, filters) in names:
            v = self.get_values(name, filters, time)
            if v is None or len(v) < 1:
                print(f'no data found {name}, {filters}')
                continue
            values.append(v)
            pretty_values[0].append(name)

        # values looks like this
        # (time1, m1) (time2, m1) (time3, m3) ...
        # (time1, m2) (time2, m2) (tmie3, m3) ...
        # ...

        # and we want to convert it to a csv that looks like
        # time, l1, l2, l3 ...
        # time1, m1, m2, m3 ...
        # time2, m1, m2, m3 ...

        # essentially this operation is an augmented matrix transpose        
        if len(values) < 1:
            print("no data found")
        else:
            for i in range(len(values[0])):
                t = [values[0][i][0]]
                vs = [values[j][i][1] for j in range(len(values))]
                pretty_values.append(t + vs)     

        return pretty_values

    def construct_csv(self, names, time):
        values = self.get_all_values(names, time)
        with open('perf-data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(values)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prometheus-url",
                        type=str,
                        required=True,
                        help="Sets the prometheus url to use")
    parser.add_argument("--filter-file",
                        type=str,
                        required=True,
                        help="The path of the filter file to use")
    parser.add_argument("-t",
                        type=str,
                        default="1h",
                        help="The time duration to get")
    
    args = parser.parse_args()
    prom = Prometheus(args)
    names = prom.get_names()
    prom.construct_csv(names, args.t)
