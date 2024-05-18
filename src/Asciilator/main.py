from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

st = lambda b, o, x: f"The number in binary is: {b}\nand in octal is: {o}\nand in hex: {x}"

class Home(MDScreen):
    def get_data(self):
        x = str(self.ids.input.text)
        try:
            if x[0] == "0":
                self.ids.ans.text = str(eval(x))
            else: self.ids.ans.text = st(str(bin(int(x))), str(oct(int(x))), str(hex(int(x))))
        except:
                self.ids.ans.text = "Invaled value"

class Asciilator(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file('design.kv')

if __name__ == "__main__":
    Asciilator().run()
