from Every_Solver import *
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screenmanager import MDScreenManager

class WindowManager(MDScreenManager):
    pass

class Home(MDScreen):
    def update_variable(self, new_value):
        solve_screen = self.manager.get_screen('Solve')
        solve_screen.FUN = new_value

    def get_data(self):
        x = self.ids.Equ.text
        self.ids.Eq_anser.text = str(CalcChamp(x))

    def expand(self):
        x = self.ids.Equ.text
        self.ids.Eq_anser.text = Extract.expand_brackets(x)

    def calculas(self, none, calc):
        calc = calc._get_text()
        x = self.ids.Equ.text
        self.ids.Eq_anser.text = str(CalcChamp.Diff(x) if calc == "Diff" else CalcChamp.Int(x))

class Solve(MDScreen):
    FUN = ''

    def on_enter(self):
        self.ids.Solve.text = ""
        self.ids.anser.text = ""

    def Sol(self):
        self.ids.anser.text = str(eval(self.FUN + "('" + str(self.ids.Solve.text) + "')" ))

class Heugebra(MDScreen):
    def open_web(self):
        _open('https://sites.google.com/view/every-solver')

class CMTab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class MPTab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class EETab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class RETab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class QUTab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class HeuTab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class EncTab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class MAIN(MDApp):
    def on_start(self):
        Window.set_title('Every Solver')

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file('design.kv')

if __name__ == '__main__':
    MAIN().run()
