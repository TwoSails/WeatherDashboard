import json


class FileExport:
    def __init__(self, data, post):
        self.filename = "weatherapp/data_files/export.json"
        self.data = data
        self.post = post
        self.post_items = (
        'export_name', 'span_int', 'wind_direction', 'avg_wind_speed', 'wind_gust', 'rainfall', 'humidity',
        'ambient_temp', 'ground_temp', 'pressure', 'timestamps')
        self.content_items = ['windDirection', 'avgWindSpeed', 'windGust', 'rainfall', 'humidity', 'ambientTemp',
                              'groundTemp', 'pressure', 'timestamps']
        self.content = {'windDirection': None,
                        'avgWindSpeed': None,
                        'windGust': None,
                        'rainfall': None,
                        'humidity': None,
                        'ambientTemp': None,
                        'groundTemp': None,
                        'pressure': None,
                        'timestamps': None}

    def content_data(self):
        self.content['windDirection'] = self.data.data['windDirection'][
                                        -(self.post.span_int * 48):] if self.post.wind_direction else None
        self.content['avgWindSpeed'] = self.data.data['avgWindSpeed'][
                                       -(self.post.span_int * 48):] if self.post.avg_wind_speed else None
        self.content['windGust'] = self.data.data['windGust'][
                                   -(self.post.span_int * 48):] if self.post.wind_gust else None
        self.content['rainfall'] = self.data.data['rainfall'][
                                   -(self.post.span_int * 48):] if self.post.rainfall else None
        self.content['humidity'] = self.data.data['humidity'][
                                   -(self.post.span_int * 48):] if self.post.humidity else None
        self.content['ambientTemp'] = self.data.data['ambientTemp'][
                                      -(self.post.span_int * 48):] if self.post.ambient_temp else None
        self.content['groundTemp'] = self.data.data['groundTemp'][
                                     -(self.post.span_int * 48):] if self.post.ground_temp else None
        self.content['pressure'] = self.data.data['pressure'][
                                   -(self.post.span_int * 48):] if self.post.pressure else None
        self.content['timestamps'] = self.data.data['TIMESTAMPS'][
                                     -(self.post.span_int * 48):] if self.post.timestamps else None

    def create_file(self):
        file = open(self.filename, 'w')
        json.dump(self.content, file, indent=4)
        file.close()

    def parse(self):
        for x in self.content_items:
            if self.content[x] is None:
                self.content = self.removeKey(self.content, x)
            else:
                pass

    def run(self):
        self.content_data()
        self.parse()
        self.create_file()

    @staticmethod
    def removeKey(d, key):
        r = dict(d)
        del r[key]
        return r
