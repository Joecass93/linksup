import pandas as pd
import googlemaps
from gmplot import gmplot

class Main():

    def __init__(self):
        self.main()

    def main(self):
        df = pd.read_csv('courses.csv', sep=",")
        df = df[['course', 'url']]
        self.i = 0
        self.total = len(df)

        df['lat'] = df['course'].apply(self.get_lat)
        df['lon'] = df['course'].apply(self.get_lon)

        df.to_csv('course_w_locations', sep=',')

    def get_lat(self, course):
        try:
            self.i += 1
            print '{}/{}'.format(self.i, self.total)
            lat, lon = gmplot.GoogleMapPlotter.geocode(course, None)
            return lat
        except Exception as e:
            print e
            return None

    def get_lon(self, course):
        try:
            lat, lon = gmplot.GoogleMapPlotter.geocode(course, None)
            return lon
        except Exception as e:
            print e
            return None

if __name__ == "__main__":
    Main()
