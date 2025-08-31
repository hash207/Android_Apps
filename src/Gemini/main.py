import os
from google import genai
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window 
from kivymd.uix.screen import MDScreen

api_key = os.environ["GEMINI_API_KEY"]

class Gemini():
    def __init__(self, content: str, image: str=None):

        client = genai.Client(api_key=api_key)

        if not image:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=content,
            )
            
            self.answer = response.text
        else:
            with open(image, 'rb') as f:
                image_bytes = f.read()

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    genai.types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
                    content
                ]
            )
            
            self.answer = response.text
    def __str__(self):
        return self.answer

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