from Every_Solver import *
from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
from kivy.core.window import Window
from webbrowser import open as _open
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screenmanager import MDScreenManager

class WindowManager(MDScreenManager):
    pass

st = lambda b, o, x: f"The number in binary is: {b}\nand in octal is: {o}\nand in hex: {x}"

class Home(MDScreen):
    def update_variable(self, new_value):
        solve_screen = self.manager.get_screen('Solve')
        solve_screen.FUN = new_value

    def get_data(self):
        x = self.ids.Equ.text
        self.ids.Eq_anser.text = str(CalcChamp(x))

    def get_ascii_data(self):
        x = str(self.ids.input.text)
        try:
            if x[0] == "0":
                self.ids.ans.text = str(eval(x))
            else: self.ids.ans.text = st(str(bin(int(x))), str(oct(int(x))), str(hex(int(x))))
        except:
                self.ids.ans.text = "Invaled value"

    def expand(self):
        x = self.ids.Equ.text
        self.ids.Eq_anser.text = Extract.expand_brackets(x)

    def calculas(self, none, calc):
        calc = calc._get_text()
        x = self.ids.Equ.text
        self.ids.Eq_anser.text = str(CalcChamp.Diff(x) if calc == "Diff" else CalcChamp.Int(x))

    # def get_dir(self):
    #     try:
    #         _dir = get_open_file()
    #         self.ids.dir_ans.text = _dir
    #     except Exception as e:
    #         self.ids.dir_ans.text = str(e)

    def open_web(self):
        _open('https://sites.google.com/view/every-solver')

class Solve(MDScreen):
    FUN = ''

    def on_enter(self):
        self.ids.Solve.text = ""
        self.ids.anser.text = ""

    def Sol(self):
        self.ids.anser.text = str(eval(self.FUN + "('" + str(self.ids.Solve.text) + "')" ))

class Heugebra(MDScreen):...

class TETab(MDFloatLayout, MDTabsBase):...

class PETab(MDFloatLayout, MDTabsBase):...

class EETab(MDFloatLayout, MDTabsBase):...

class ASTab(MDFloatLayout, MDTabsBase):...

class QUTab(MDFloatLayout, MDTabsBase):...

class HeuTab(MDFloatLayout, MDTabsBase):...

class EncTab(MDFloatLayout, MDTabsBase):...

class MAIN(MDApp):
    def on_start(self):
        Window.set_title('Every Solver')

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file('design.kv')

if __name__ == '__main__':
    MAIN().run()
