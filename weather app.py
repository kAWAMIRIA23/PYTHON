import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.City_label = QLabel("ENTER CITY", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("GET WEATHER", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
            
    def initUI(self):
        self.setWindowTitle("Weather")
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.City_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        self.City_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.City_label.setObjectName("City_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
           QLabel, QPushButton {
               font-family: Calibri;
               font-size: 30px;
               font-style: bold;
           }
           QLineEdit#city_input {
               font-size: 60px;
           }
           QPushButton#get_weather_button {
               font-size: 50px;
               font-weight: italic;
           }
           QLabel#temperature_label {
               font-size: 60px;
           }
           QLabel#emoji_label {
               font-size: 100px;
               font-family: Segoe UI Emoji;
           }
           QLabel#description_label {
               font-size: 50px;
               font-weight: bold;
           }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
  
    def get_weather(self):
        api_key = "61270d485f7a31a18993384b2d84f02a"
        city = self.city_input.text()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
       
        try:
            response = requests.get(url)
            data = response.json()
       
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_err:       
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease enter a valid city")
                case 401:
                    self.display_error("Bad request\nInvalid API key")
                case 403:
                    self.display_error("Bad request\nAccess denied")
                case 404:
                    self.display_error("Bad request\nCity not found")
                case 500:
                    self.display_error("Bad request\nPlease enter a valid city")
                case 502:
                    self.display_error("Bad request\nInvalid response from server")
                case 503:
                    self.display_error("Bad request\nService unavailable")
                case 504:
                    self.display_error("Bad request\nGateway timeout")
                case _:
                    self.display_error(f"An error occurred\n{http_err}")
                      
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Connection error\nRequest timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("An error occurred\nPlease try again later")
        except requests.exceptions.RequestException as e:
            self.display_error(f"An error occurred\n{e}")
              
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 20px; color: red;")
        self.temperature_label.setText(message)
    
    def display_weather(self, data):
        temperature = data["main"]["temp"]
        temperature = temperature - 273.15
        temperature = round(temperature, 2)
        
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"] 
        
        self.temperature_label.setText(f"{temperature}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌧️"
        elif 500 <= weather_id <= 531:  
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🤷"
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
