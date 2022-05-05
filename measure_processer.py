class error:
    def __init__(self, value, error):
        self.value = value
        self.error = error
        
    def p(self):
        return array([self.value,self.error])
    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return error(self.value + other, self.error)
        elif type(other) == error:
            return error(self.value + other.value, self.error+ other.error)
        else:
            print("input must be float int or error")
    def __radd__(self, other):
        return error(self.value + other, self.error)
    
    def __sub__(self, other):
        if type(self) == error and type(other) == error:
            return error(self.value - other.value, self.error + other.error)
        elif type(self) == error and type(other) != error:
            return error(self.value - other, self.error+ other)
        else:
            print("input must be float int or error")
    def __rsub__(self,other):
        return error(other-self.value, self.error)
    def __mul__(self,other):
        if type(self) == error and type(other) == error:
            return error(self.value * other.value, (self.error/self.value + other.error/other.value)*self.value*other.value)
        elif type(self) == error and type(other) != error:
            return error(self.value*other,self.error*abs(other))
        else:
            print("input must be float int or error")
    def __rmul__(self,other):
        return error(self.value*other,self.error*abs(other))
    def __truediv__(self,other):
        if type(self) == error and type(other) == error:
            return error(self.value / other.value, (self.error/self.value + other.error/other.value)*self.value/other.value)
        elif type(self) == error and type(other) != error:
            return error(self.value/other,self.error/abs(other))
        else:
            print("input must be float int or error")
    def __rtruediv__(self,other):
        return error(other/self.value,abs(other)/self.error)
def erfun(self,fun):
    h=1e-5
    if type(self) == error:
        return error(fun(self.value),abs((fun(self.value+h)-fun(self.value-h))/(2*h))*self.error)
    else:
        return error(fun(self),0)

def illesz(x,y):
    xatlag=average(x)
    yatlag=average(y)
    m=0
    mnev=0
    for i in range(len(x)):
        m+=(x[i]-xatlag)*(y[i]-yatlag)
        mnev+=(x[i]-xatlag)**2
    m/=mnev
    b=yatlag-m*xatlag
    s=sum((y-(x*m+b))**2)/(len(x)-2)
    sm=s/(sum(x**2)-len(x)*xatlag**2)
    sb=s*(1/len(x)+xatlag**2/(sum(x**2)-(len(x))*xatlag**2))
    plot(x,y,linestyle="",marker="o",label="mérés")
    t=linspace(min(x),max(x),2)
    plot(t,t*m+b,label="illesztés")
    legend()
    return array([hiba(m,sqrt(sm)),hiba(b,sqrt(sb))])
  
def strszam(szam,jegy):
    if type(szam)==float:
        strin=""
        mant=int(floor(log10(abs(szam))))
        if mant<-2 or mant+1>jegy: #lebegő pontos
            strin+=str(round(szam/10**floor(log10(abs(szam))),jegy-1))
            if len(strin)-1<jegy:
                strin+="0"*(jegy-len(strin)+1)
            strin="$"+strin+" \\cdot 10^{"+str(mant)+"}$"
        else:
            strin=str(szam)
        return strin
    elif type(szam)==int:
        return str(szam)
    elif type(szam)==error:
        strin=""
        mant=int(floor(log10(abs(szam.value))))
        if mant<-2 or mant+1>jegy: #lebegő pontos
            strin+=str(round(szam.value/10**floor(log10(abs(szam.value))),jegy-1))
            if len(strin)-1<jegy:
                strin+="0"*(jegy-len(strin)+1)
            strin="$("+strin+"\pm"+str(szam.error/10**mant)+") \\cdot 10^{"+str(mant)+"}$"
        else:
            strin="$"+str(szam.value)+"\pm"+str(szam.error)+"$"
        return strin
    else:
        print("input must be float int or error")

def tablazat(adat,cimsor,jegy):
    beg="\\begin{tabular}{|"+"c|"*len(cimsor)+"}"
    print(beg)
    print("\\hline")
    cim=""
    for i in range(len(cimsor)-1):
        cim+=cimsor[i]+" & "
    cim+=cimsor[-1] + " \\\\"
    print(cim)
    print("\\hline")
    for i in range(adat.shape[0]):
        adatsor=""
        for j in range(adat.shape[1]-1):
            adatsor+=strszam(adat[i,j],jegy)+" & "
        adatsor+=strszam(adat[i,-1],jegy)+ " \\\\"
        print(adatsor)
        print("\\hline")
    print("\\end{tabular}")
