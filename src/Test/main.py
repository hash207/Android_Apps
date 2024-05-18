from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from plyer import filechooser

class Home(MDScreen):
    def choose_dir(self):
        dir = filechooser.choose_dir()
        print(dir)

class main_app(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file("design.kv")

if __name__ == "__main__":
    main_app().run()

