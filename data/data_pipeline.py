import requests 
import re
import csv

class Prometheus:
    def __init__(self):
        self.PROMETHEUS = "http://localhost:8080"
        self.BASE_URL = "/prometheus/api/v1"
        self.name_filters = ["gpu"]
        self.container_filters = ["*"]

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
        filtered_names = set()
        for filter in self.name_filters:
            filtered = self.apply_filter(names, filter)

            for name in filtered:
                filtered_names.add(name)

        return list(filtered_names)
    
    def get_values(self, name, time, start):
        endpoint = "/query"
        params = { "query": "{}[{}]".format(name, time) }
        values = self.query(endpoint, params)['data']['result'][0]['values'] # container level filtering can be done here
        return values

    def get_all_values(self, names, time, start):
        values = []

        for name in names:
            values.append(self.get_values(name, time, start))

        # values looks like this
        # (time1, m1) (time2, m1) (time3, m3) ...
        # (time1, m2) (time2, m2) (tmie3, m3) ...
        # ...

        # and we want to convert it to a csv that looks like
        # time, l1, l2, l3 ...
        # time1, m1, m2, m3 ...
        # time2, m1, m2, m3 ...

        # essentially this operation is an augmented matrix transformation

        pretty_values = [] 
        pretty_values.append(['time'] + names)
        
        for i in range(len(values[0])):
            t = [values[0][i][0]]
            vs = [values[j][i][1] for j in range(len(names))]
            pretty_values.append(t + vs)     

        return pretty_values

    def construct_csv(self, names, time, start):
        values = self.get_all_values(names, time, start)
        with open('perf-data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(values)
        

if __name__ == "__main__":
    prom = Prometheus()
    names = prom.get_names()
    prom.construct_csv(names, '5m', 0)
