import requests
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window 
from kivymd.uix.screen import MDScreen

class Gemini():
    headers = {'Content-Type': 'application/json'}
    data = lambda self,text: {"contents": [{"parts": [{"text": text}]}]}
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=you-api-key"

    def __init__(self, ans: str):
        self.response = requests.post(self.url, headers=self.headers, json= self.data(ans))
        self.response_data = self.response.json()

    def __str__(self):
        if self.response.status_code == 200:
            return self.response_data['candidates'][0]['content']['parts'][0]['text']
        else: return f"Error: API request failed with status code {self.response.status_code}"

class Home(MDScreen):
    def get_gem(self):
        x = self.ids.input.text
        self.ids.ans.text = str(Gemini(x))

class main_app(MDApp):
    def on_start(self):
        Window.set_title('Gemini')

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file('design.kv')


if __name__ == "__main__":
    main_app().run()