import sympy as sp
from math import factorial
from kivymd.app import MDApp
from kivy.lang import Builder
from re import findall, finditer
from kivy.core.window import Window
from webbrowser import open as _open
from kivymd.uix.screen import MDScreen
from kivy.properties import DictProperty
from kivymd.uix.screenmanager import MDScreenManager

__version__ = "1.0.0"
crs = r"[-+]?(?:\d*\.\d+|\d+)"

class ExtractError(Exception):...

class Extract:
    pow = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}

    def __init__(self, x):
        self.string = x

    #Linear Equation
    @classmethod
    def EX_LIN(self, x: str) -> list:
        x = x.lower()
        if x[0] == '+':
            x = x.replace('+','',1)
        if ''.join(findall('[a-z]',x)) == '':
            a = 0
            b = float(x)
        else:
            if len(findall('[-+]',x)) == 1:
                if x[0] != '-':
                    if x.index(''.join(findall('[a-z]',x))) < x.index(''.join(findall('[-+]',x))):
                        a = float(''.join(findall('\d|[.]',x[:x.index(''.join(findall('[-+]',x)))]))) if x[0] != ''.join(findall('[a-zA-Z]',x)) else 1.0
                        b = float(''.join(findall(crs,x[x.index(''.join(findall('[-+]',x))):])))
                    else:
                        a = float(''.join(findall(crs,x[x.index(''.join(findall('[-+]',x))):]))) if x[x.index(''.join(findall('[-+]',x)))+1] != ''.join(findall('[a-zA-Z]',x)) else float(''.join(findall('[-+]',x))+'1')
                        b = float(''.join(findall('\d|[.]',x[:x.index(''.join(findall('[-+]',x)))])))
                else:
                    if ''.join(findall('[a-zA-Z]',x)) == '':
                        a = 0.0
                        b = float(x)
                    if ''.join(findall('[a-zA-Z]',x)) != '':
                        a = float(''.join(findall(crs,x))) if x != '-'+''.join(findall('[a-zA-Z]',x)[0]) else -1.0
                        b = 0.0
            elif len(findall('[-+]',x)) == 0:
                    if ''.join(findall('[a-zA-Z]',x)) == '':
                        a = 0.0
                        b = float(x)
                    if ''.join(findall('[a-zA-Z]',x)) != '':
                        a = float(''.join(findall(crs,x))) if x != ''.join(findall('[a-zA-Z]',x)[0]) else 1.0
                        b = 0.0                    
            else:
                if ''.join(findall('[-+]',x)[1]) == '-':
                    if x.index(''.join(findall('[a-zA-Z]',x))) < [i.start() for i in finditer('[-+]',x)][1]:
                        a = float(''.join(findall(crs,x[:x.index(''.join(findall('[a-zA-Z]',x)))]))) if x[1] != ''.join(findall('[a-zA-Z]',x)) else -1.0
                        b = float(''.join(findall(crs,x[[i.start() for i in finditer('[-+]',x)][1]:])))
                    else:
                        a = float(''.join(findall(crs,x[[i.start() for i in finditer('[-+]',x)][1]:]))) if x[[i.start() for i in finditer('[-+]',x)][1]+1:] != ''.join(findall('[a-zA-Z]',x)[0]) else 1.0 if ''.join(findall('[-+]',x)[1]) != '-' else -1.0
                        b = float(''.join(findall(crs,x[:[i.start() for i in finditer('[-+]',x)][1]])))
                else:
                    if x.index(''.join(findall('[a-zA-Z]',x))) < x.index(''.join(findall('[-+]',x)[1])):
                        a = float(''.join(findall(crs,x[:x.index(''.join(findall('[a-zA-Z]',x)))]))) if x[1] != ''.join(findall('[a-zA-Z]',x)) else -1.0
                        b = float(''.join(findall(crs,x[x.index('+'):])))
                    else:
                        a = float(''.join(findall(crs,x[x.index(''.join(findall('[-+]',x)[1])):])))
                        b = float(''.join(findall(crs,x[:[i.start() for i in finditer('[-+]',x)][1]])))
        return [a,b]

    #Quadratic Equation
    @classmethod
    def EX_QUD(self, x: str) -> list:
        if x[0] == '-' or x[0] == '+':
            a = float(''.join(findall('\d|[+-]|.',x[:x.index('^2')-1]))) if x[1] != ''.join(findall('[a-zA-Z]',x)[0]) else float(x[0] + '1')
        else:
            a = float(''.join(findall('\d|[+-]|.',x[:x.index('^2')-1]))) if x[0] != ''.join(findall('[a-zA-Z]',x)[0]) else 1.0
        if len(x[x.index('^2')+2:]) != 0:
            b = self.EX_LIN(x[x.index('^2')+2:])[0]
            c = self.EX_LIN(x[x.index('^2')+2:])[1]
        else:
            b=c=0
        return [a,b,c]
    
    #Cubic Equation
    @classmethod
    def EX_CUB(self, x: str) -> list:
        a = float(''.join(findall(crs,x[:x.index('^3')]))) if len(findall(crs,x[:[i.start() for i in finditer('[a-zA-Z]',x)][0]])) != 0 else 1.0 if x[0] != '-' else -1.0
        if len(x[x.index('^3')+1:]) != 0:
            if x.find('^2') != -1:
                b = self.EX_QUD(x[x.index('^3')+2:])[0]
                c = self.EX_QUD(x[x.index('^3')+2:])[1]
                d = self.EX_QUD(x[x.index('^3')+2:])[2]
            else:
                b = 0
                c = self.EX_LIN(x[x.index('^3')+2:])[0]
                d = self.EX_LIN(x[x.index('^3')+2:])[1]
        else:
            b=c=d=0
        return [a,b,c,d]

    @classmethod
    def EX_FRTH(self, x: str) -> list:
        a=b=c=d=e= 0
        var = findall('[a-z]',x.lower())[0]
        a = float(x[:x.index(var)]) if x[0] != var else 1.0
        if len(x[x.index('^4')+1:]) != 0:
            if x.find('^3') != -1:
                b = self.EX_CUB(x[x.index('^4')+2:])[0]
                c = self.EX_CUB(x[x.index('^4')+2:])[1]
                d = self.EX_CUB(x[x.index('^4')+2:])[2]
                e = self.EX_CUB(x[x.index('^4')+2:])[3]
            elif x.find('^2') != -1:
                b = 0
                c = self.EX_QUD(x[x.index('^4')+2:])[0]
                d = self.EX_QUD(x[x.index('^4')+2:])[1]
                e = self.EX_QUD(x[x.index('^4')+2:])[2]
            else:
                b=c=0
                d = self.EX_LIN(x[x.index('^4')+2:])[0]
                e = self.EX_LIN(x[x.index('^4')+2:])[1]
        else:
            b=c=d=e=0
        return [a,b,c,d,e]

    def EX_CIR(self, x: str) -> list:
        x = x.lower()
        try:
            var = findall('[a-z]', x)
            d = float(x[x.index('=')+1:]) ** 0.5
            for i in x:
                if i == var[0]:
                    x_brak = x[x.index(i):x.index(')')]
                    X = float(x_brak.replace(var[0],'')) * -1 if findall('\d',x_brak) != [] else 0
                    y_brak = x[x.index(var[1]):[j.start() for j in finditer('²',x)][1]-1]
                    Y = float(y_brak.replace(var[1],'')) if findall('\d',y_brak) != [] else 0
                    return [X,Y,d]
        except:
            raise ExtractError("Extraction could not be completed")
        return

    def pascal_triangle(rows) :
        factor = lambda n,k: factorial(n)/(factorial(k)*factorial(n-k))
        ans = [factor(rows,i) for i in range(0, rows+1)]
        return ans

    #Expand Brackets
    @classmethod
    def expand_brackets(self, string):
        if string != '':
            string = string.lower()
            power = int(string[-1])
            nums = int(findall(crs, string)[0])
            var = str(findall('[a-z]', string)[0])
            sign = str(findall('[+-]', string)[0])
            
            factors = [self.pascal_triangle(power)[i]*(nums**i) for i in range(power+1)]

            ans = [(str(int(factors[i]))+var+f"{self.pow[str(j+1)]}"+(sign if sign == '+' else ('' if i%2 == 0 else '+'))).replace('¹', '') for i, j in zip(range(power), reversed(range(power)))]

            return ''.join(ans)+str(int(factors[-1]))
        else:
            return ''

    def __str__(self):
        if self.string.find('(') == -1:
            if self.string.find('^4') != -1:
                a,b,c,d,e = self.EX_FRTH(self.string)[0],self.EX_FRTH(self.string)[1],self.EX_FRTH(self.string)[2],self.EX_FRTH(self.string)[3],self.EX_FRTH(self.string)[4]
                return f"{a},{b},{c},{d},{e}"
            if self.string.find('^3') != -1:
                return f"{self.EX_CUB(self.string)[0]},{self.EX_CUB(self.string)[1]},{self.EX_CUB(self.string)[2]},{self.EX_CUB(self.string)[3]}"
            elif self.string.find('^2') != -1:
                if len(findall(r"\^2",self.string)) == 2:
                    return f"{self.EX_CIR(self.string)[0]},{self.EX_CIR(self.string)[1]},{self.EX_CIR(self.string)[2]}"
                else:
                    return f"{self.EX_QUD(self.string)[0]},{self.EX_QUD(self.string)[1]},{self.EX_QUD(self.string)[2]}"
            else:
                return f"{self.EX_LIN(self.string)[0]},{self.EX_LIN(self.string)[1]}"
        else:
            self.string = self.expand_brackets(self.string)
            if self.string.find('^4') != -1:
                a,b,c,d,e = self.EX_FRTH(self.string)[0],self.EX_FRTH(self.string)[1],self.EX_FRTH(self.string)[2],self.EX_FRTH(self.string)[3],self.EX_FRTH(self.string)[4]
                return f"{a},{b},{c},{d},{e}"
            if self.string.find('^3') != -1:
                return f"{self.EX_CUB(self.string)[0]},{self.EX_CUB(self.string)[1]},{self.EX_CUB(self.string)[2]},{self.EX_CUB(self.string)[3]}"
            elif self.string.find('^2') != -1:
                if len(findall(r"\^2",self.string)) == 2:
                    return f"{self.EX_CIR(self.string)[0]},{self.EX_CIR(self.string)[1]},{self.EX_CIR(self.string)[2]}"
                else:
                    return f"{self.EX_QUD(self.string)[0]},{self.EX_QUD(self.string)[1]},{self.EX_QUD(self.string)[2]}"
            else:
                return f"{self.EX_LIN(self.string)[0]},{self.EX_LIN(self.string)[1]}"

class CalcChamp:
    def __init__(self,string: str = None) -> None:
        self.string = string

    #problem in this function
    @classmethod
    def Eq_Trns(self,x: str, calculas: bool = False) -> str:
        if x.replace('.', '').isnumeric():
            return x
        else:
            var = ''.join(findall('[a-zA-Z]',x)[0])
            numbers = findall('\d',x)
            if x.find('*') == -1:
                x = (x if x[0].isnumeric() else '1'+x).replace(var, '*'+var).replace('^', '**')
                return x
            else:
                if calculas:
                    for i in numbers:
                        i = eval(i)
                        x = x.replace('**'+str(i), Extract.pow[str(i)]) if x.find('**'+str(i)) != -1 else x
                
                    x = x.replace('*','')
                    x = x.replace(' ','')
                    return x
                else:
                    x = x.replace('**', '^').replace('*', '').replace(' ', '')
                    return x

    @classmethod
    def SOL_LIN(self,x: str) -> str:
        _lis = [eval(i) for i in str(Extract(x)).split(',')]
        a = _lis[0]
        b = _lis[1]
        if a == 0:
            if b == 0:
                return "Infinite solutions"
            else:
                return "No solution"
        else:
            x = -1*b/a
            #print(f"The value of {sym} is: {x}")
            return x

    @classmethod
    def SOL_QUD(self,x: str) -> str:
        _lis = [eval(i) for i in str(Extract(x)).split(',')]
        a,b,c = _lis[0],_lis[1],_lis[2]
        D = b**2-4*a*c
        if (D > 0):
            x1 = ((b*-1)+eval(''.join(findall(crs,str(D**0.5).replace('0','')))))/(2*a)
            x2 = ((b*-1)-eval(''.join(findall(crs,str(D**0.5).replace('0','')))))/(2*a)
            if x1 == x2 * -1:
                #print([f"±{x1}\nThe Discriminant is:{D}",x1,x2])
                return [f"±{x1}",x1,x2]
            else:
                #print([f"{x1},{x2}\nThe Discriminant is:{D}",x1,x2])
                return [f"{x1},{x2}",x1,x2]
        elif (D == 0):
            x = (-1*b)/(2*a)
            #print([f"{x}\nThe Discriminant is:{D}"])
            return [f"{x}",x,x]
        elif (D < 0):
            D = D*-1
            x1 = ((b*-1)+eval(''.join(findall(crs,str(D**0.5).replace('0','')))))/(2*a)
            x2 = ((b*-1)-eval(''.join(findall(crs,str(D**0.5).replace('0','')))))/(2*a)
            if x1 == x2 * -1:
                #print([f"±{x1}i\nThe Discriminant is:{D}"])
                return [f"±{x1}i"]
            else:
                #print([f"{x1}i,{x2}i\nThe Discriminant is:{D}"])
                return [f"{x1}i,{x2}i"]

    @classmethod
    def SOL_CUB(self,string: str) -> str:
        Factors = [eval(i) for i in str(Extract(string)).split(',')]
        a,b,c,d = Factors[0],Factors[1],Factors[2],Factors[3]
        f = lambda x: a*x**3+b*x**2+c*x+d
        x = sp.symbols('x')
        string = f"{a}{x}^3{'' if b==0 else (f'{b}{x}^2' if b<0 else f'+{b}{x}^2')}{'' if c==0 else (f'{c}{x}' if c<0 else f'+{c}{x}')}{'' if d==0 else (d if d<0 else f'+{d}')}"
        divisors = []

        for i in sp.divisors(int(a)):
            for j in sp.divisors(int(d)):
                divisors.append(j/i)

        result = []

        for i in divisors:
            result.append(i)
            result.append(i*-1)

        #print(result)

        for i in result:
            if f(float(i)) == 0:
                divisor = 'x'+str(i*-1) if (i*-1)<0 else 'x+'+str(i*-1)
                quotient = sp.simplify(eval(self.Eq_Trns(string)) / eval(divisor))
                LIN = self.SOL_LIN(divisor)
                try:
                    QUD1, QUD2 = self.SOL_QUD(self.Eq_Trns(str(quotient)))[1], self.SOL_QUD(self.Eq_Trns(str(quotient)))[2]
                    Result = set([LIN, QUD1, QUD2])
                except IndexError:
                    Result = [LIN]
                return str(Result)[1:-1]
        else:
            return "This equation has no solutions"

    @classmethod
    def SOL_FRTH(self,string: str) -> str:
        Factors = [eval(i) for i in str(Extract(string)).split(',')]
        a,b,c,d,e = Factors[0],Factors[1],Factors[2],Factors[3],Factors[4]
        f = lambda x: a*x**4+b*x**3+c*x**2+d*x+e
        x = sp.symbols('x')
        string = f"{a}{x}^4{'' if b==0 else (f'{b}{x}^3' if b<0 else f'+{b}{x}^3')}{'' if c==0 else (f'{c}{x}^2' if c<0 else f'+{c}{x}^2')}{'' if d==0 else (f'{d}{x}' if d<0 else f'+{d}{x}')}{'' if e==0 else (e if e<0 else f'+{e}')}"
        divisors = []

        for i in sp.divisors(int(a)):
            for j in sp.divisors(int(d)):
                divisors.append(j/i)

        result = []

        for i in divisors:
            result.append(i)
            result.append(i*-1)
        
        #print(result)

        for i in result:
            if f(i) == 0:
                divisor = 'x'+str(i*-1) if (i*-1)<0 else 'x+'+str(i*-1)
                quotient = str(sp.simplify(eval(self.Eq_Trns(string)) / eval(divisor)))
                if quotient.find('**3') != -1:
                    sol = self.SOL_CUB(self.Eq_Trns(quotient))
                elif quotient.find('**2') != -1:
                    sol = self.SOL_QUD(self.Eq_Trns(quotient))
                return sol
        else:
            return "This equation has no solutions"

    #Derivation
    @classmethod
    def Diff(self,x: str) -> str:
        try:
            if x.find('(') == -1:
                x = x.lower()
                if ''.join(findall('[a-z]',x)) == '':
                    #print("The Diffrntation is: 0")
                    return "The Diffrntation is: 0" if len(x) != 0 else ''
                elif x.find('*') == -1:
                    x = self.Eq_Trns(x)

                    symb = sp.symbols(''.join(findall('[a-zA-Z]',x)[0]))

                    DIFF = str(sp.diff(x, symb))

                    DIFF = self.Eq_Trns(DIFF, calculas= True)

                    #print(f"The Diffrntation is: {DIFF}")
                    return f"The Diffrntation is: {DIFF}"
        except:
            return 'Error'

    #Integral
    @classmethod
    def Int(self,x: str) -> str:
        try:
            if x.find('(') == -1:
                x = x.lower()
                if ''.join(findall('[a-z]',x)) == '':
                    try:
                        INT = f"{eval(''.join(findall(crs, x)))}x+c"
                        return f"The Integral is: {INT}"
                    except:
                        return ''
                    #print("The Integral is: 0")
                elif x.find('*') == -1:
                    x = self.Eq_Trns(x)

                    symb = sp.symbols(''.join(findall('[a-zA-Z]',x)[0]))

                    try:
                        INT = str(sp.integrate(x, symb))
                    except SyntaxError:
                        INT = str('1'+sp.integrate(x, symb))

                    INT = self.Eq_Trns(INT, calculas =True) + '+c'

                    #print(f"The Integral is: {INT}")
                    return f"The Integral is: {INT}"
        except:
            return 'Error'

    def __str__(self) -> str:
        if self.string.replace(' ','') == '':
            return ''
        elif self.string == f"sin({''.join(findall(crs,self.string))})" or self.string == f"cos({''.join(findall(crs,self.string))})" or self.string == f"tan({''.join(findall(crs,self.string))})":
            num = ''.join(findall(crs, self.string))
            ans = str(eval(self.string.replace(num, f'radians({int(num)})')))
            return ans
        elif 'log' in self.string:
            return str(eval(self.string))
        elif 'ln' in self.string:
            return str(eval((self.string).replace('ln', 'log1p')))
        else:
            if findall('[a-z]',self.string.lower()) != []:
                if self.string.find('^4') != -1:
                    return str(self.SOL_FRTH(self.string))
                elif self.string.find('^3') != -1:
                    return str(self.SOL_CUB(self.string))
                elif self.string.find('^2') != -1:
                    if len(findall(r"\^2",self.string)) == 2:
                        List = [eval(i) for i in str(Extract(self.string)).split(',')]
                        return f"The Circle Cinter's points is: ({List[0]},{List[1]}),\nand The Diameter is: {List[2]}"
                    else:
                        return str(self.SOL_QUD(self.string)[0])
                else:
                    return str(self.SOL_LIN(self.string))
            else:
                return str(eval(self.string))

class WindowManager(MDScreenManager):
    pass

class Home(MDScreen):
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

class Heugebra(MDScreen):
    def open_web(self):
        _open('https://sites.google.com/view/every-solver')

class MAIN(MDApp):
    data = DictProperty()

    def on_start(self):
        Window.set_title('Every Solver')

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file('testing.kv')

if __name__ == '__main__':
    MAIN().run()
