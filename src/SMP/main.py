from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from requests import post, ConnectTimeout  # Importing necessary libraries for making HTTP requests and handling connection timeouts

class Home(MDScreen):
    def toggle_led(self, btn):  # Method to toggle the LED state
        ip = self.ids.ip.text  # Getting the IP address from the input field
        try:
            rout = btn.text.replace(" ", "").upper()  # Formatting the route (LED1 or LED2) to uppercase and removing spaces
            url = f"http://192.168.0.{ip if ip else 105}/{rout}"  # Constructing the URL for the HTTP request
            post(url)  # Sending an HTTP POST request to the specified URL
            #self.ids.resp.text = url  # Uncomment this line to display the URL in the response field
        except ConnectTimeout:
            self.ids.resp.text = "Connection Timeout"  # Displaying a connection timeout message in the response field

class main_app(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Setting the theme style to dark
        self.theme_cls.primary_palette = "Indigo"  # Setting the primary color palette to indigo
        return Builder.load_file("design.kv")  # Loading the Kivy design file

if __name__ == "__main__":
    main_app().run()  # Running the main application