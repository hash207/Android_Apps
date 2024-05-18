from re import *
import sympy as sp
from math import *

__version__ = "1.0.0"

def Cons():
    pi: float = 3.141592653589793
    C: float = 299792458 #m/s
    G: float = 6.67428 * 10 ** -11 #m**3/kg.s**2
    lb: float = 2.20462 #kg
    Da: float = 1.660538921 * 10 ** -24 #kg
    crs = r"[-+]?(?:\d*\.\d+|\d+)"
    return pi, C, G, lb, Da, crs

def electrical_cons():
    vp = 1/(4*pi*10**-7*C**2) #Vacuum permeability
    v_p = 4*pi*10**-7
    k = 1/(4*pi*vp)
    return vp, v_p, k

def quantum_cons():
    H: float = (3*7*6310543)/(2**42*5**41) #j.s
    H_bar: float = H/(2*pi) #j.s
    PL: float = (H_bar*G/C**3)**0.5
    PT: float = (H_bar*G/C**5)**0.5
    PM: float = H_bar**0.5*C**0.5*G**-0.5
    P_CH: float = (4*pi*vp*H_bar*C)**0.5
    eV: float = 1.602176634 * 10 ** -18 #j
    WC: float = 2.897771955 * 10 ** -3 #m.kg
    return H, H_bar, PL, PT, PM, P_CH, eV, WC

pi, C, G, lb, Da, crs = Cons()

vp, v_p, k = electrical_cons()

H, H_bar, PL, PT, PM, P_CH, eV, WC = quantum_cons()

class ExtractError(Exception):...

class LorentzTrans:
    #Mass–Energy equivalence
    def MEE(x: str) -> str:
        """
        Calculate Mass–Energy equivalence:-
        For Mass:
            ****kg or ****lb or ****Da
        For Energy:
            ****j or ****eV
        NOTE: No Case sensitivity
        """
        x = x.lower()
        try:
            if str(''.join(findall('[a-zA-Z]',x))) == 'j':
                e = eval(x[:x.index('j')])
                m = e/C**2
                #print(f"Mass is: {m}kg\nWich is equal to: {m/Da}Da\nAnd {m/lb}lb")
                return(f"Mass is: {m}kg\nWich is equal to: {m/Da}Da\nAnd {m/lb}lb")
            elif str(''.join(findall('[a-zA-Z]',x))) == 'ev':
                e = eval(x[:x.index('ev')])
                m = e*eV/C**2
                #print(f"Mass is: {m}kg\nWich is equal to: {m/Da}Da\nAnd {m/lb}lb")
                return(f"Mass is: {m}kg\nWich is equal to: {m/Da}Da\nAnd {m/lb}lb")
            elif str(''.join(findall('[a-zA-Z]',x))) == 'kg':
                m = eval(x[:x.index('kg')])
                e = m*C**2
                #print(f"Energy is: {e}J\nWich is equal to: {e/eV}eV")
                return (f"Energy is: {e}J\nWich is equal to: {e/eV}eV")
            elif str(''.join(findall('[a-zA-Z]',x))) == 'da':
                m = eval(x[:x.index('da')])
                e = m*Da*C**2
                #print(f"Energy is: {e}J\nWich is equal to: {e/eV}eV")
                return (f"Energy is: {e}J\nWich is equal to: {e/eV}eV")
            elif str(''.join(findall('[a-zA-Z]',x))) == 'lb':
                m = eval(x[:x.index('lb')])
                e = m*lb*C**2
                #print(f"Energy is: {e}J\nWich is equal to: {e/eV}eV")
                return (f"Energy is: {e}J\nWich is equal to: {e/eV}eV")
            else:
                return 'error\nPlz Insert a Unit'
        except:
            raise ExtractError("Extraction could not be completed")

    #Lorentz Transformation
    def LF(x: str) -> str:
        try:
            V = eval(x[:x.lower().index('m')])
            LF = 1/(1-(V/C)**2)**0.5
            #print(f'Lorenz Factor is: {LF}')
            return (f'Lorenz Factor is: {LF}')
        except ZeroDivisionError:
            return "Speed of light, Lorenz Factor is infinity"

    @classmethod
    def TS(self,x: str) -> str:
        x = x.lower()
        try:
            if x.index('s') < x.index('m'):
                t = float(''.join(findall(crs,x[:x.index('s')])))
                V = x[x.index(',')+1:x.index('m')+3]
            elif x.index('s') > x.index('m'):
                t = float(''.join(findall(crs,x[x.index(','):[i.start() for i in finditer('s',x)][1]])))
                V = x[:x.index('m')+3]
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            T = t * float(''.join(findall(crs,self.LF(V))))
            #print(f"The Relativistic Time is: {T}S")
            return(f"The Relativistic Time is: {T}S")
        except ZeroDivisionError:
            #print('Speed of light\nThe Time freez')
            return 'Speed of light\nThe Time freez'

    @classmethod
    def LC(self,x: str) -> str:
        x = x.lower()
        try:
            if ''.join(findall('[a-z]',x)) == 'msm':
                l = eval(x[x.index(',')+1:[i.start() for i in finditer('m',x)][1]])
                V = x[:x.index('s')]
            elif ''.join(findall('[a-z]',x)) == 'mms':
                l = eval(x[:x.index('m')])
                V = x[x.index(',')+1:]
                pass
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            L = l / float(''.join(findall(crs,self.LF(V))))
            #print(f"The Relativistic Lingth is: {L}m")
            return(f"The Relativistic Lingth is: {L}m")
        except ZeroDivisionError:
            #print('Speed of light\nThe Lingth is Unlimited')
            return 'Speed of light\nThe Lingth is Unlimited'

    @classmethod
    def RsM(self,x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mskg' or ''.join(findall('[a-zA-Z]',x)) == 'kgms':
            if ''.join(findall('[a-zA-Z]',x)) == 'mskg':
                m = eval(x[x.index(',')+1:x.index('kg')])
                V = x[:x.index(',')]
            else:
                m = eval(x[:x.index('kg')])
                V = x[x.index(',')+1:]
        elif ''.join(findall('[a-zA-Z]',x)) == 'msda' or ''.join(findall('[a-zA-Z]',x)) == 'dams':
            if ''.join(findall('[a-zA-Z]',x)) == 'msda':
                m = eval(x[x.index(',')+1:x.index('da')])*Da
                V = x[:x.index(',')]
            else:
                m = eval(x[:x.index('da')])*Da
                V = x[x.index(',')+1:]
        elif ''.join(findall('[a-zA-Z]',x)) == 'mslb' or ''.join(findall('[a-zA-Z]',x)) == 'lbms':
            if ''.join(findall('[a-zA-Z]',x)) == 'mslb':
                m = eval(x[x.index(',')+1:x.index('lb')])*lb
                V = x[:x.index(',')]
            else:
                m = eval(x[:x.index('lb')])*lb
                V = x[x.index(',')+1:]
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        M = m / float(''.join(findall(crs,self.LF(V))))
        #print(f"The Rest Mass Is: {M}kg\nWich is equal to: {M/lb}lb\nand: {M/Da}Da")
        return(f"The Rest Mass is: {M}kg\nWich is equal to: {M/lb}lb\nand: {M/Da}Da")

    @classmethod
    def ReM(self,x: str) -> str:
        x = x.lower()
        try:
            if ''.join(findall('[a-zA-Z]',x)) == 'mskg' or ''.join(findall('[a-zA-Z]',x)) == 'kgms':
                if ''.join(findall('[a-zA-Z]',x)) == 'mskg':
                    m = eval(x[x.index(',')+1:x.index('kg')])
                    V = x[:x.index(',')]
                else:
                    m = eval(x[:x.index('kg')])
                    V = x[x.index(',')+1:]
            elif ''.join(findall('[a-zA-Z]',x)) == 'msda' or ''.join(findall('[a-zA-Z]',x)) == 'dams':
                if ''.join(findall('[a-zA-Z]',x)) == 'msda':
                    m = eval(x[x.index(',')+1:x.index('da')])*Da
                    V = x[:x.index(',')]
                else:
                    m = eval(x[:x.index('da')])*Da
                    V = x[x.index(',')+1:]
            elif ''.join(findall('[a-zA-Z]',x)) == 'mslb' or ''.join(findall('[a-zA-Z]',x)) == 'lbms':
                if ''.join(findall('[a-zA-Z]',x)) == 'mslb':
                    m = eval(x[x.index(',')+1:x.index('lb')])*lb
                    V = x[:x.index(',')]
                else:
                    m = eval(x[:x.index('lb')])*lb
                    V = x[x.index(',')+1:]
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            M = m * float(''.join(findall(crs,self.LF(V))))
            #print(f"The Relativistic Mass Is: {M}kg\nWich is equal to: {M/lb}lb\nand: {M/Da}Da")
            return(f"The Relativistic Mass is: {M}kg\nWich is equal to: {M/lb}lb\nand: {M/Da}Da")
        except ZeroDivisionError:
            #print('Speed of light\nThe Mass is Unlimited')
            return 'Speed of light\nThe Mass is Unlimited'

    #Relative Kinetic Energy
    @classmethod
    def RKE(self,x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mskg' or ''.join(findall('[a-zA-Z]',x)) == 'kgms':
            if ''.join(findall('[a-zA-Z]',x)) == 'mskg':
                m = eval(x[x.index(',')+1:x.index('kg')])
                V = x[:x.index(',')]
            else:
                m = eval(x[:x.index('kg')])
                V = x[x.index(',')+1:]
        elif ''.join(findall('[a-zA-Z]',x)) == 'msda' or ''.join(findall('[a-zA-Z]',x)) == 'dams':
            if ''.join(findall('[a-zA-Z]',x)) == 'msda':
                m = eval(x[x.index(',')+1:x.index('da')])*Da
                V = x[:x.index(',')]
            else:
                m = eval(x[:x.index('da')])*Da
                V = x[x.index(',')+1:]
        elif ''.join(findall('[a-zA-Z]',x)) == 'mslb' or ''.join(findall('[a-zA-Z]',x)) == 'lbms':
            if ''.join(findall('[a-zA-Z]',x)) == 'mslb':
                m = eval(x[x.index(',')+1:x.index('lb')])*lb
                V = x[:x.index(',')]
            else:
                m = eval(x[:x.index('lb')])*lb
                V = x[x.index(',')+1:]
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        KE = m*C**2 * (float(''.join(findall(crs,self.LF(V))))-1)
        #print(f"The Relative Kinetic Energy is: {KE}j\nWich is Equal to: {KE/eV}eV")
        return(f"The Relative Kinetic Energy is: {KE}j\nWich is Equal to: {KE/eV}eV")

    #Schwarzschild radius
    def Rs(x: str) -> str:
        x = x.lower()
        try:
            m = eval(x[:x.index('k')])
            r = 2*G*m/C**2
            #print(f"Schwarzschild Radius is: {r} m")
            return(f"Schwarzschild Radius is: {r} m")
        except ValueError:
            #print('error,Plz Insert a Unit')
            return 'error,Plz Insert a Unit'

    #Gravitational time dilation
    def GTDF(x: str) -> str:
        x = x.lower()
        m_index = x.index('m')
        kg_index = x.index('kg')

        if m_index < kg_index:
            m = float(findall(crs, x[m_index: x.index('*10')])[0]) if '**' in x else float(findall(crs, x[m_index:])[0])
            pow_1 = 10**int(findall(r'\d+', x[x.index('**'):])[0]) if '**' in x else 1
            d = float(findall(crs, x[: m_index])[0])
        else:
            m = float(findall(crs, x[:kg_index])[0]) if '**' in x else float(findall(crs, x[:kg_index])[0])
            pow_1 = 10**int(findall(r'\d+', x[x.index('**'):kg_index])[0]) if '**' in x else 1
            d = float(findall(crs, x[kg_index:])[0])
        f = (1-((2*G*(m*pow_1))/(d*C**2)))**0.5
        #print(f'Gravitational time dilation factor is: {f}N')
        return f'Gravitational time dilation factor is: {f}N'

    @classmethod
    def GTD(self,x: str) -> str:
        x = x.lower()
        for i in findall('[a-zA-Z]',x):
            if i == 's':
                if findall('[a-zA-Z]',x).index('s') == 0:
                    F = x[x.index(',')+1:]
                    t = float(''.join(findall(crs,x[:x.index(',')])))
                elif findall('[a-zA-Z]',x).index('s') == 2:
                    F = x[:x.index(',')]+x[[i.start() for i in finditer(',',x)][1]:]
                    t = float(''.join(findall(crs,x[x.index(','):x.index('s')])))
                elif findall('[a-zA-Z]',x).index('s') == 3:
                    F = x[:[i.start() for i in finditer(',',x)][1]]
                    t = float(''.join(findall(crs,x[[i.start() for i in finditer(',',x)][1]+1:])))
                else:
                    #print('error\nPlz Insert a Unit')
                    return 'error\nPlz Insert a Unit'
                T = t*float(''.join(findall(crs,str(self.GTDF(F)))))
                #print(f"Gravitational Time dilation is: {T}s")
                return(f"Gravitational Time dilation is: {T}s")

    def VAF(x: str) -> str:
        return 'Commning soon!'

class QubitWhiz:
    """Equation Mastery in the Quantum Universe with QubitWhiz!"""
    #Photon Energy
    def PhE(x: str) -> str:
        x = x.lower()
        if str(''.join(findall('[a-zA-Z]',x))) == 'j':
            e = eval(x[:x.index('j')])
            wl = H*C/e
            #print(f"The Wivelingth is: {wl} m")
            return(f"The Wivelingth is: {wl} m")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'ev':
            e = eval(x[:x.index('ev')])
            wl = H*C/(e*eV)
            #print(f"The Wivelingth is: {wl} m")
            return(f"The Wivelingth is: {wl} m")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'm':
            wl = eval(x[:x.index('m')])
            e = H*C/wl
            #print(f"The Energy is: {e} J\nWich is equal to: {e/eV} eV")
            return(f"The Energy is: {e} J\nWich is equal to: {e/eV} eV")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'hz':
            f = eval(x[:x.index('hz')])
            e = H*f
            #print(f"The Energy is: {e} J\nWich is equal to: {e/eV} eV")
            return(f"The Energy is: {e} J\nWich is equal to: {e/eV} eV")
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'

    #Photon Momentum
    def PhM(x: str) -> str:
        wl = eval(x[:x.lower().index('m')])
        m = H/wl
        #print(f"The Photon Momentum is: {m}kg.m/s")
        return f"The Photon Momentum is: {m}kg.m/s"

    #Uncertainty Principle
    def UCP(x: str) -> str:
        x = x.lower()
        if str(''.join(findall('[a-zA-Z]',x))) == 'kgms':
            M = eval(x[:x.index('kg')])
            m = H_bar/M
            #print(f"Mass is >= {m}kg\nWich is equal >= to: {m/Da}Da\nAnd >= {m/lb}lb")
            return(f"Mass is >= {m}kg\nWich is allmost equal to: >= {m/Da}Da\nAnd >= {m/lb}lb")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'kg':
            m = eval(x[:x.index('kg')])
            M = H_bar/m
            #print(f"The Momentum is >= {M} kg.m/s")
            return (f"The Momentum is >= {M} kg.m/s")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'da':
            m = eval(x[:x.index('da')])
            M = H_bar/m*Da
            #print(f"The Momentum is >= {M} kg.m/s")
            return (f"The Momentum is >= {M} kg.m/s")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'lb':
            m = eval(x[:x.index('lb')])
            M = H_bar/m*lb
            #print(f"The Momentum is >= {M} kg.m/s")
            return (f"The Momentum is >= {M} kg.m/s")
        else:
            return 'error\nPlz Insert a Unit'

    #Wien's Law
    def WI_LAW(x: str) -> str:
        x = x.lower()
        if str(''.join(findall('[a-zA-Z]',x))) == 'k':
            T = eval(x[:x.index('k')])
            WL = WC/T
            #print(f"The Wivelingth is: {WL}m")
            return(f"The Wivelingth is: {WL}m")
        elif str(''.join(findall('[a-zA-Z]',x))) == 'm':
            WL = eval(x[:x.index('m')])
            T = WC/WL
            #print(f"The Temp is: {T}k")
            return(f"The Temp is: {T}k")
        else:
            #print('error\nPlz Insert a Unit')
            return('error\nPlz Insert a Unit')

    #Temperature Conversion
    def Fah(x: str) -> str:
        x = x.lower()
        if ''.join(findall(r"°|[f]",x)) == '°f' or ''.join(findall("[a-zA-Z]",x)) == 'f':
            cel = (float(''.join(findall(crs,x)))-32)*(5/9)
            kel = ((float(''.join(findall(crs,x)))-32)*(5/9))+273.15
            #print(f'The Temperature in Kelvin is:{kel} K\nWich is equel to:{cel} °C')
            return f'The Temperature in Kelvin is:{kel} K\nWich is equel to:{cel} °C'
        else:
            return 'error\nPlz Insert a Unit'

    def Cel(x: str) -> str:
        x = x.lower()
        if ''.join(findall(r"°|[c]",x)) == '°c' or ''.join(findall("[a-zA-Z]",x)) == 'c':
            kel = float(''.join(findall(crs,x)))+273.15
            fah = (float(''.join(findall(crs,x)))*(9/5))+32
            #print(f'The Temperature in Kelvin is:{kel} K\nWich is equel to:{fah} °F')
            return f'The Temperature in Kelvin is:{kel} K\nWich is equel to:{fah} °F'
        else:
            return 'error\nPlz Insert a Unit'

    def Kel(x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'k':
            cel = eval(float(''.join(findall(crs,x))))-273.15
            fah = ((float(''.join(findall(crs,x)))-273.15) * (9/5))+32
            #print(f'The Temperature in Celsius is: {cel} °C\nWich is equel to:{fah} °F')
            return f'The Temperature in Celsius is: {cel} °C\nWich is equel to:{fah} °F'
        else:
            return 'error\nPlz Insert a Unit'

class Cl_Mec:
    #Free Fall Acceleration
    def FFA(x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mkg' or ''.join(findall('[a-zA-Z]',x)) == 'kgm':
            if x.index('kg') < x.index('m'):
                m = float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[:x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('kg') > x.index('m'):
                m = float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[x.index(','):x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mda' or ''.join(findall('[a-zA-Z]',x)) == 'dam':
            if x.index('da') < x.index('m'):
                m = Da*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[:x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('da') > x.index('m'):
                m = Da*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[x.index(','):x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mlb' or ''.join(findall('[a-zA-Z]',x)) == 'lbm':
            if x.index('lb') < x.index('m'):
                m = lb*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[:x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('lb') > x.index('m'):
                m = lb*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[x.index(','):x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[:x.index('m')])))
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        a = float(G*(m*pow_1)/d**2)
        #print(f"Free Fall Acceleration is: {a} m/s²")
        return(f"Free Fall Acceleration is: {a} m/s²")

    #Newton's Law of Unevirsal Gravitation
    @classmethod
    def grav(self,x: str) -> str:
        x = x.lower()
        for i in findall('[a-zA-Z]',x):
            if i == 'm':
                if (findall('[a-zA-Z]',x)).index(i) == 0:
                    a = x[:x.index('g')+2]
                    m = float(''.join(findall(crs,x[[i.start() for i in finditer(',',x)][1]+1:x.index('*10')]))) if (x[[i.start() for i in finditer(',',x)][1]+1:]).find('**') != -1 else float(''.join(findall(crs,x[[i.start() for i in finditer(',',x)][1]+1:])))
                    pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):])))) if (x[[i.start() for i in finditer(',',x)][1]+1:]).find('**') != -1 else 1
                    A = float(''.join(findall(r"\d+.[+-]?",str(self.FFA(a)))))
                    f = (m*pow_1)*A
                    #print(f"The Weight is: {f} N")
                    return(f"The Weight is: {f} N")
                elif (findall('[a-zA-Z]',x)).index(i) == 2:
                    a = x[:x.index(i)+1]
                    m = float(''.join(findall(crs,x[([i.start() for i in finditer(',',x)][1])+1:x.index('*10')]))) if x[([i.start() for i in finditer(',',x)][1])+1:].find('**') != -1 else float(''.join(findall(crs,x[([i.start() for i in finditer(',',x)][1])+1:])))
                    X = x[x.index(',')+1:]
                    pow_1 = 10**int(''.join(findall('\d',X[X.index('**'):X.index('kg')]))) if X.find('**') != -1 else 1
                    A = float(''.join(findall(r"\d+.[+-]?",str(self.FFA(a)))))
                    f = (m*pow_1)*A
                    #print(f"The Weight is: {f} N")
                    return(f"The Weight is: {f} N")
                elif (findall('[a-zA-Z]',x)).index(i) == 4:
                    a = x[x.index(',')+1:]
                    m = float(''.join(findall(crs,x[:x.index('*10')]))) if x[:x.index(',')].find('**') != -1 else float(''.join(findall(crs,x[:x.index(',')])))
                    pow_1 = 10**int(''.join(findall('\d',x[x.index('**'):x.index(',')]))) if x[:x.index(',')].find('**') != -1 else 1
                    A = float(''.join(findall(r"\d+.[+-]?",str(self.FFA(a)))))
                    f = (m*pow_1)*A
                    #print(f"The Weight is: {f}N")
                    return(f"The Weight is: {f}N")
                else:
                    #print('error\nPlz Insert a Unit')
                    return 'error\nPlz Insert a Unit'

    #Calculate Momentum
    def MNT(x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mskg' or ''.join(findall('[a-zA-Z]',x)) == 'kgms':
            if x.index('kg') < x.index('m'):
                m = float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[:x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('kg') > x.index('m'):
                m = float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[x.index(','):x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'msda' or ''.join(findall('[a-zA-Z]',x)) == 'dams':
            if x.index('da') < x.index('m'):
                m = Da*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[:x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('da') > x.index('m'):
                m = Da*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[x.index(','):x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mslb' or ''.join(findall('[a-zA-Z]',x)) == 'lbms':
            if x.index('lb') < x.index('m'):
                m = lb*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[:x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('lb') > x.index('m'):
                m = lb*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[x.index(','):x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[:x.index('m')])))
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        M = m*pow_1*V
        #print(f"The Momentum is: {M}kg.m/s")
        return f"The Momentum is: {M}kg.m/s"   

    #Calculate Work
    def Work(x: str) -> str:
        x = x.lower()
        units = ''.join(findall('[a-z]', x))
        if 'deg' in x:
            List = x.split(',')
            for i in List:
                if 'n' in i:
                    f = eval(i.replace('n', ''))
                elif 'm' in i:
                    d = eval(i.replace('m', ''))
                elif 'deg' in i:
                    th = eval(i.replace('deg', ''))
                else:
                    f = 0
                    d = 0
                    th = 0
        else:
            th = 0
            if units == 'nm':
                f = eval(x[:x.index('n')])
                d = eval(x[x.index(',')+1:x.index('m')])
            elif units == 'mn':
                f = eval(x[x.index(',')+1:x.index('n')])
                d = eval(x[:x.index('m')])
            else:
                return 'Error'
        work = f*d*cos(th/180*pi).__round__(5)
        #print(f"The work is: {work} J")
        return f"The work is: {work} J"

    #Calculate Velocity
    def VLCT(x: str) -> str:
        x = x.lower()
        if x.index('s') < x.index('m'):
            D = eval(x[x.index(',')+1:x.index('m')])
            t = eval(x[:x.index('s')])
        elif x.index('s') > x.index('m'):
            D = eval(x[:x.index('m')])
            t = eval(x[x.index(',')+1:x.index('s')])
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        V = D/t
        #print(f'Velocity is: {V} m/s')
        return f'Velocity is: {V} m/s'

    #Calculate Acceleration
    def Acc(x: str) -> str:
        x = x.lower()
        if len(findall('[a-z]',x[:x.index('s')])):
            V = eval(x[:x.index('m')])
            t = eval(x[x.index(',')+1:[i.start() for i in finditer('s',x)][1]])
        elif len(findall('[a-z]',x[:x.index('s')])) == 0:
            V = eval(x[x.index(',')+1:x.index('m')])
            t = eval(x[:x.index('s')])
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        Acc = V/t
        #print(f'The ascceleration is {Acc} m/s²')
        return f'The ascceleration is {Acc} m/s²'

    #Escape Velocity
    def EVC(x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mkg' or ''.join(findall('[a-zA-Z]',x)) == 'kgm':
            if x.index('kg') < x.index('m'):
                m = float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[:x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('kg') > x.index('m'):
                m = float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[x.index(','):x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mda' or ''.join(findall('[a-zA-Z]',x)) == 'dam':
            if x.index('da') < x.index('m'):
                m = Da*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[:x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('da') > x.index('m'):
                m = Da*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[x.index(','):x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mlb' or ''.join(findall('[a-zA-Z]',x)) == 'lbm':
            if x.index('lb') < x.index('m'):
                m = lb*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[:x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('lb') > x.index('m'):
                m = lb*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[x.index(','):x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                d = float(''.join(findall(crs,x[:x.index('m')])))
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        EV = ((2*m*pow_1*G)/d)**0.5
        #print(f"The Escape Velocity is: {EV}")
        return f"The Escape Velocity is: {EV}"

    #Kinatek Energy
    def KE(x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mskg' or ''.join(findall('[a-zA-Z]',x)) == 'kgms':
            if x.index('kg') < x.index('m'):
                m = float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[:x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('kg') > x.index('m'):
                m = float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[x.index(','):x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'msda' or ''.join(findall('[a-zA-Z]',x)) == 'dams':
            if x.index('da') < x.index('m'):
                m = Da*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[:x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('da') > x.index('m'):
                m = Da*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[x.index(','):x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mslb' or ''.join(findall('[a-zA-Z]',x)) == 'lbms':
            if x.index('lb') < x.index('m'):
                m = lb*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[:x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('lb') > x.index('m'):
                m = lb*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[x.index(','):x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                V = float(''.join(findall(crs,x[:x.index('m')])))
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        ke = ((m*pow_1)*V**2)/2
        #print(F"The Kinetic  Energy is: {ke} J\nWich is  equal to: {ke/eV} eV")
        return(F"The Kinetic  Energy is: {ke} J\nWich is  equal to: {ke/eV} eV")

    #Potential Energy
    @classmethod
    def PoE(self,x: str) -> str:
        x = x.lower()
        if ''.join(findall('[a-zA-Z]',x)) == 'mkg' or ''.join(findall('[a-zA-Z]',x)) == 'kgm':
            if x.index('kg') < x.index('m'):
                m = float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[:x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                H = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('kg') > x.index('m'):
                m = float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else float(''.join(findall(crs,x[x.index(','):x.index('kg')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('kg')])))) if x.find('**')!=-1 else 1
                H = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mda' or ''.join(findall('[a-zA-Z]',x)) == 'dam':
            if x.index('da') < x.index('m'):
                m = Da*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[:x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                H = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('da') > x.index('m'):
                m = Da*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else Da*float(''.join(findall(crs,x[x.index(','):x.index('da')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('da')])))) if x.find('**')!=-1 else 1
                H = float(''.join(findall(crs,x[:x.index('m')])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mlb' or ''.join(findall('[a-zA-Z]',x)) == 'lbm':
            if x.index('lb') < x.index('m'):
                m = lb*float(''.join(findall(crs,x[:x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[:x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                H = float(''.join(findall(crs,x[x.index(','):x.index('m')])))
            elif x.index('lb') > x.index('m'):
                m = lb*float(''.join(findall(crs,x[x.index(','):x.index('*10')]))) if x.find('**') != -1 else lb*float(''.join(findall(crs,x[x.index(','):x.index('lb')])))
                pow_1 = 10**(int(''.join(findall('\d',x[x.index('**'):x.index('lb')])))) if x.find('**')!=-1 else 1
                H = float(''.join(findall(crs,x[:x.index('m')])))
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        po = (m*pow_1)*float(''.join(findall(r"\d+.[+-]?",str(self.FFA('5.98*10**24kg,6371000m')))))*H
        #print(f"The Potential Energy is: {po} J\nWich is equal to: {po/eV} eV")
        return f"The Potential Energy is: {po} J\nWich is equal to: {po/eV} eV"

    #Pressure
    @classmethod
    def PUR(self,x: str) -> str:
        x = x.lower()
        _lis = x.split(',')
        if ''.join(findall(f'[a-zA-Z]',x)) == 'kgmm' or ''.join(findall(f'[a-zA-Z]',x)) == 'mkgm':
            for i in _lis:
                if i.find('kg') != -1:
                    d = eval(''.join(findall(crs, i)))
                else:
                    h = eval(''.join(findall(crs, i)))
            pur = d*h*float(''.join(findall(crs,self.FFA('5.98*10**24kg,6371000m'))))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mn' or ''.join(findall('[a-zA-Z]',x)) == 'nm':
            if x.index('n') < x.index('m'):
                p = eval(''.join(findall(crs,x[:x.index('n')])))
                A = eval(''.join(findall(crs,x[x.index(',')+1:x.index('m')])))
            elif x.index('n') > x.index('m'):
                p = eval(''.join(findall(crs,x[x.index(',')+1:x.index('n')])))
                A = eval(''.join(findall(crs,x[:x.index('m')])))
            #pur = p/A
        else:
            #print('error\nPlz Insert a Unit')
            return 'error\nPlz Insert a Unit'
        #print(f"Pressure is: {p,A} Pa")
        return f"Pressure is: {pur} Pa"

    #Buoyant Force
    @classmethod
    def BYF(self,x: str) -> str:
        x = x.lower()
        if  ''.join(findall('[a-zA-Z]',x)) == 'kgmm':
            D = float(''.join(findall(crs,x[:x.index('kg')])))
            V = float(''.join(findall(crs,x[x.index(','):])))
        elif ''.join(findall('[a-zA-Z]',x)) == 'mkgm':
            V = float(''.join(findall(crs,x[:x.index('m')])))
            D = float(''.join(findall(crs,x[x.index(','):])))
        BF = D*V*float(''.join(findall(r"\d+.[+-]?",str(self.FFA('5.98*10**24kg,6371000m')))))
        #print(f'The Buoyant Force is: {BF} N')
        return f'The Buoyant Force is: {BF} N'

class Elec_Equ:
    class Ohms_Law:
        def __init__(self, x: str) -> None:
            self.x = x

        def get_volt(self, x: str) -> str:
            x = x.lower()
            if x.index('o') < x.index('a'):
                I = eval(x[x.index(',')+1:x.index('a')])
                R = eval(x[:x.index('o')])
            elif x.index('o') > x.index('a'):
                I = eval(x[:x.index('a')])
                R = eval(x[x.index(',')+1:x.index('o')])
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            V = I*R
            #print(f'The Voltag in the circute is {V} V')
            return f'The Voltag in the circute is {V} V'

        def get_current(self, x: str) -> str:
            x = x.lower()
            if x.index('o') < x.index('v'):
                V = eval(x[x.index(',')+1:x.index('v')])
                R = eval(x[:x.index('o')])
            elif x.index('o') > x.index('v'):
                V = eval(x[:x.index('v')])
                R = eval(x[x.index(',')+1:x.index('o')])
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            I = V/R
            #print(f'The Current in  the circute is {I} A')
            return f'The Current in  the circute is {I} A'

        def get_resistance(self, x: str) -> str:
            x = x.lower()
            if x.index('a') < x.index('v'):
                V = eval(x[x.index(',')+1:x.index('v')])
                I = eval(x[:x.index('a')])
            elif x.index('a') > x.index('v'):
                V = eval(x[:x.index('v')])
                I = eval(x[x.index(',')+1:x.index('a')])
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            R = V/I
            #print(f'The Resistance in  the circute is {R} Ω')
            return f'The Resistance in  the circute is {R} Ω'

        def __str__(self):
                var = ''.join(findall('[a-zA-Z]', self.x.lower()))
                if var == 'ao' or var == 'oa':
                    return self.get_volt(self.x)
                elif var == 'vo' or var == 'ov':
                    return self.get_current(self.x)
                elif var == 'av' or var == 'va':
                    return self.get_resistance(self.x)
                else:
                    return 'Error\nPleas insert a right units'

    class coulombs_law:
        def __init__(self, x: str) -> str:
            self.x = x

        def EFS(self, x: str) -> str:
            x = x.lower()
            if ''.join(findall('[a-zA-Z]',x)) == 'mc' or ''.join(findall('[a-zA-Z]',x)) == 'cm':
                if x.index('c') < x.index('m'):
                    ch = eval(x[:x.index('c')])
                    d = eval(''.join(findall(crs,x[x.index(','):x.index('m')])))
                elif x.index('c') > x.index('m'):
                    ch = eval(x[x.index(',')+1:x.index('c')])
                    d = eval(x[:x.index('m')])
            else:
                #print('error\nPlz Insert a Unit')
                return 'error\nPlz Insert a Unit'
            efs = float(k*ch/d**2)
            #print(f"The Electric field strength is: {efs} N/C")
            return(f"The Electric field strength is: {efs} N/C")

        def main_law(self, x: str) -> str:
            x = x.lower()
            for i in findall('[a-zA-Z]',x):
                if i == 'm':
                    if (findall('[a-zA-Z]',x)).index(i) == 0:
                        a = x[:x.index('c')+2]
                        efs = float(''.join(findall(r"\d+.[+-]?",str(self.EFS(a)))))
                        ch = eval(''.join(findall(crs,x[[i.start() for i in finditer(',',x)][1]+1:])))
                    elif (findall('[a-zA-Z]',x)).index(i) == 1:
                        a = x[:x.index(i)+1]
                        efs = float(''.join(findall(r"\d+.[+-]?",str(self.EFS(a)))))
                        ch = float(''.join(findall(crs,x[([i.start() for i in finditer(',',x)][1])+1:x.index('*10')]))) if x[([i.start() for i in finditer(',',x)][1])+1:].find('**') != -1 else float(''.join(findall(crs,x[([i.start() for i in finditer(',',x)][1])+1:])))
                        X = x[x.index(',')+1:]
                        pow_1 = 10**int(''.join(findall('\d',X[X.index('**'):X.index('c')]))) if X.find('**') != -1 else 1
                    elif (findall('[a-zA-Z]',x)).index(i) == 2:
                        a = x[x.index(',')+1:]
                        efs = float(''.join(findall(r"\d+.[+-]?",str(self.EFS(a)))))
                        ch =  eval(x[:x.index(',')-1])
                    else:
                        #print('error\nPlz Insert a Unit')
                        return 'error\nPlz Insert a Unit'
                    F = efs*ch
                    #print(f"{F} N")
                    return(f"{F} N")

        def __str__(self):
            if len(findall('c',self.x.lower())) == 1:
                return self.EFS(self.x)
            else:
                return self.main_law(self.x)

    class Elec_Enrg:
        def __init__(self, x: str) -> None:
            self.x = x

        @staticmethod
        def El_PWR(x: str) -> str:
            x = x.lower()
            if ''.join(findall('[a-zA-Z]', x)) == 'oa' or ''.join(findall('[a-zA-Z]', x)) == 'ao':
                if x.index('o') < x.index('a'):
                    I = eval(x[x.index(',')+1:x.index('a')])
                    R = eval(x[:x.index('o')])
                elif x.index('o') > x.index('a'):
                    I = eval(x[:x.index('a')])
                    R = eval(x[x.index(',')+1:x.index('o')])
                EP = I**2*R
            elif ''.join(findall('[a-zA-Z]', x)) == 'ov' or ''.join(findall('[a-zA-Z]', x)) == 'vo':
                if x.index('o') < x.index('v'):
                    V = eval(x[x.index(',')+1:x.index('v')])
                    R = eval(x[:x.index('o')])
                elif x.index('o') > x.index('v'):
                    V = eval(x[:x.index('v')])
                    R = eval(x[x.index(',')+1:x.index('o')])
                EP = V**2/R
            elif ''.join(findall('[a-zA-Z]', x)) == 'va' or ''.join(findall('[a-zA-Z]', x)) == 'av':
                if x.index('a') < x.index('v'):
                    V = eval(x[x.index(',')+1:x.index('v')])
                    I = eval(x[:x.index('a')])
                elif x.index('a') > x.index('v'):
                    V = eval(x[:x.index('v')])
                    I = eval(x[x.index(',')+1:x.index('a')])
                EP = I*V
            return f'The Electrical Power is: {EP} W'

        @classmethod
        def main_law(self, x: str) -> str:
            x = x.lower()
            for i in x:
                if i == 'h':
                    if ''.join(findall('[a-z]', x)).index(i) == 0:
                        T = eval(x[:x.index(i)])
                        ep = x[x.index(',')+1:]
                        EP = float(''.join(findall(crs,self.El_PWR(ep))))
                        EE = EP * T*10**-3
                        return f'The Electrical Energy is: {EE} kWh'
                    if ''.join(findall('[a-z]', x)).index(i) == 1:
                        T = eval(x[x.index(',')+1:x.index(i)])
                        ep = x.replace(f",{x[x.index(',')+1:[i.start() for i in finditer(',',x)][1]]}", '')
                        EP = float(''.join(findall(crs,self.El_PWR(ep))))
                        EE = EP * T*10**-3
                        return f'The Electrical Energy is: {EE} kWh'
                    if ''.join(findall('[a-z]', x)).index(i) == 2:
                        T = eval(x[[i.start() for i in finditer(',',x)][1]+1:x.index('h')])
                        ep = x[:[i.start() for i in finditer(',',x)][1]]
                        EP = float(''.join(findall(crs,self.El_PWR(ep))))
                        EE = EP * T*10**-3
                        return f'The Electrical Energy is: {EE} kWh'

        def __str__(self):
            if self.x.find('h') == -1:
                return self.El_PWR(self.x)
            else:
                return self.main_law(self.x)

    def LPF(x: str) -> str:
        if ''.join(findall("[a-z]", x.lower())) == "of":
            R = eval(''.join( x[:x.index(',')-1]))
            C = eval(''.join( x[x.index(',')+1:-1]))
        elif ''.join(findall("[a-z]", x.lower())) == "fo":
            C = eval(''.join( x[:x.index(',')-1]))
            R = eval(''.join( x[x.index(',')+1:-1]))
        else :
            return "Error\n Pleas insert a right unit"
        lpf = (2*pi*R*C)**-1
        #print(f"The LPF frequency for this filter is: {lpf} Hz")
        return f"The LPF frequency for this filter is: {lpf} Hz"

    def HPF(x: str) -> str:
        if "f" in x.lower():
            if ''.join(findall("[a-z]", x.lower())) == "of":
                R = eval(''.join( x[:x.index(',')-1]))
                C = eval(''.join( x[x.index(',')+1:-1]))
            elif ''.join(findall("[a-z]", x.lower())) == "fo":
                C = eval(''.join( x[:x.index(',')-1]))
                R = eval(''.join( x[x.index(',')+1:-1]))
            else :
                return "Error\n Pleas insert a right unit"
            lpf = (2*pi*R*C)**-1
        elif "h" in x.lower():
            if ''.join(findall("[a-z]", x.lower())) == "oh":
                R = eval(''.join( x[:x.index(',')-1]))
                L = eval(''.join( x[x.index(',')+1:-1]))
            elif ''.join(findall("[a-z]", x.lower())) == "ho":
                L = eval(''.join( x[:x.index(',')-1]))
                R = eval(''.join( x[x.index(',')+1:-1]))
                lpf = R/(2*pi*L)
            else :
                return "Error\n Pleas insert a right unit"
        #print(f"The LPF frequency for this filter is: {lpf} Hz")
        return f"The HPF frequency for this filter is: {lpf} Hz"

    def Resis_collector(x: str, status: str = 'series') -> str:
        ans = 0
        status = status.lower()
        _lest = ''.join(x.split('o')).split(',')
        if status == 'series':
            for i in _lest:
                ans += float(i)
        elif status == 'parallel':
            for i in _lest:
                ans += 1/float(i)
            ans = 1/ans
        return f'The sumation of the resistors is {ans}'

    def Cap_Rea(x: str) -> str:
        x = x.lower()
        var = ''.join(findall('[a-z]',x))
        if var == 'hzf':
            C = eval(x[x.index(',')+1:x.index('f')])
            F = eval(x[:x.index('h')])
        elif var == 'fhz':
            F = eval(x[x.index(',')+1:x.index('h')])
            C = eval(x[:x.index('f')])
        Xc = 1/(2*pi*F*C)
        #print(f"The Capacitive Reactance is: {Xc} Ω")
        return f"The Capacitive Reactance is: {Xc} Ω"

    def Ind_Rea(x: str) -> str:
        x = x.lower()
        var = ''.join(findall('[a-z]',x))
        h = [i.start() for i in finditer('h', x)]
        if var == 'hzh':
            I = eval(x[x.index(',')+1:h[1]])
            F = eval(x[:x.index('h')])
        elif var == 'hhz':
            F = eval(x[x.index(',')+1:h[1]])
            I = eval(x[:x.index('h')])
        Xl = 2*pi*F*I
        #print(f"The Inductive Reactance is: {Xl} Ω")
        return f"The Inductive Reactance is: {Xl} Ω"

    def res_freq(x: str) -> str:
        x = x.lower()
        units = ''.join(findall('[a-z]', x))
        if units == 'fh':
            C = eval(x[:x.index('f')])
            I = eval(x[x.index(',')+1:x.index('h')])
        elif units == 'hf':
            C = eval(x[x.index(',')+1:x.index('f')])
            I = eval(x[:x.index('h')])
        F = (2*pi*(C*I)**0.5)**-1
        #print(f"The Resonant Frequency is: {F} Hz")
        return f"The Resonant Frequency is: {F} Hz"

    def inv_res_freq(x: str) -> str:
        x = x.lower()
        units = ''.join(findall('[a-z]', x))
        if units == 'hzx':
            F = eval(x[:x.index('hz')])
            Val = eval(x[x.index(',')+1:x.index('x')])
        elif units == 'xhz':
            F = eval(x[x.index(',')+1:x.index('hz')])
            Val = eval(x[:x.index('x')])
        ans = (4*pi**2*F**2*Val)**-1
        #print(f"the oposite of what you give is: {ans}")
        return f"the oposite of what you give is: {ans}"

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
            numbers = findall("\d",x)
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
            ans = str(eval(self.string.replace(num, f'radians({int(num)})')).__round__(3))
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

if __name__ == "__main__":
    x = ''

    print(CalcChamp(x))
