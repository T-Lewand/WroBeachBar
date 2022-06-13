import numpy as np
import requests
import json

class Point():
    def __init__(self, lat, lon):
        self.api_key = 'd01071244629a2b658132aa14e3d64d2'
        self.lat = lat
        self.lon = lon
        self.location = (lat, lon)

    def _get_weather_data(self, url):
        response = requests.get(url)
        data = response.json()
        return data

    def current_weather(self):
        """
        Retrieves current weather condition of Point instance location as instance attributes
        :return: None
        """

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}' \
              f'&units=metric'
        data = self._get_weather_data(url)
        main = data['main']
        self.temp = main['temp']
        self.temp_feeled = main['feels_like']
        self.temp_min = main['temp_min']
        self.temp_max = main['temp_max']
        self.pressure = main['pressure']
        self.humidity = main['humidity']

    def forecast(self, interval='daily'):

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={self.lat}&lon={self.lon}&exclude={interval}' \
              f'&appid={self.api_key}&units=metric'
        data = self._get_weather_data(url)
        self.current = data['current']
        self.minutely = data['minutely']
        if interval == 'hourly':
            pass
        else:
            self.hourly = data['hourly']


class Area(Point):
    def __init__(self, center_lat, center_lon, grid_shape=(3, 3), cell_size=0.5):
        """
        Creates Area instance with given parameters
        :param center_lat: Latitude coordinate of central point
        :param center_lon: Longitude coordinate of central point
        :param grid_shape: shape of grid, only odd numbers
        :param cell_size: length between two closest points in grid given in degrees

        Attributes
        center: coordinates of center point, tuple with two elements (lat, lon)
        grid_shape: shape of grid, tuple with two elements
        cell_size: length between two closest points in grid given in degrees
        size: size of area in degrees
        border: values of top, bottom latitudes, and left, right longitudes, tuple with four elements (left_lon,
            top_lat, right_lon, bottom_lat)
        """
        super().__init__(center_lat, center_lon)
        self.center = self.location
        self.grid_shape = grid_shape
        self.cell_size = cell_size
        self.size = ((grid_shape[0]-1)*cell_size, (grid_shape[1]-1)*cell_size)
        self.border = (center_lon - self.size[1]/2, center_lat + self.size[0]/2,
                       center_lon + self.size[1]/2, center_lat - self.size[0]/2)
        self.left_border = self.border[0]
        self.top_border = self.border[1]
        self.right_border = self.border[2]
        self.bottom_border = self.border[3]

    def grid_coordinates(self):
        """
        Calculates coordinates of every point in grid
        :return: Numpy array of coordinates, 3 dimension, (row, column, (lat,lon))
        """
        vector_lat = np.zeros((self.grid_shape[0], 1))
        vector_lon = np.zeros((self.grid_shape[1], 1))
        k = 0
        for lat, lon in zip(vector_lat, vector_lon):
            lat = self.top_border - self.cell_size * k
            lon = self.left_border + self.cell_size * k

            vector_lat[k], vector_lon[k] = lat, lon
            k += 1

        vector_lat = vector_lat.T
        vector_lon = vector_lon.T
        matrix_lat = vector_lat
        matrix_lon = vector_lon
        for i in range(self.grid_shape[0]-1):
            matrix_lat = np.vstack([matrix_lat, vector_lat])
            matrix_lon = np.vstack([matrix_lon, vector_lon])


        self.grid_coord_ = np.dstack((matrix_lat.T, matrix_lon))
        return self.grid_coord_

    def current_weather(self, as_list=False):
        """
        Gets current weather for all points in grid
        :param as_list:
        :return:
        """
        self.temp = []
        self.temp_feeled = []
        self.temp_min = []
        self.temp_max = []
        self.pressure = []
        self.humidity = []

        for i in self.grid_coord_:
            for j in i:

                url = f'https://api.openweathermap.org/data/2.5/weather?lat={j[0]}&lon={j[1]}&' \
                      f'appid={self.api_key}&units=metric'
                response = requests.get(url)
                data = response.json()
                main = data['main']
                self.temp.append(main['temp'])
                self.temp_feeled.append(main['feels_like'])
                self.temp_min.append(main['temp_min'])
                self.temp_max.append(main['temp_max'])
                self.pressure.append(main['pressure'])
                self.humidity.append(main['humidity'])

        if as_list is False:
            self.temp = np.array(self.temp).reshape(self.grid_shape)
            self.temp_feeled = np.array(self.temp_feeled).reshape(self.grid_shape)
            self.temp_min = np.array(self.temp_min).reshape(self.grid_shape)
            self.temp_max = np.array(self.temp_max).reshape(self.grid_shape)
            self.pressure = np.array(self.pressure).reshape(self.grid_shape)
            self.humidity = np.array(self.humidity).reshape(self.grid_shape)
