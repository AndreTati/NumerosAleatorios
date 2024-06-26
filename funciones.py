import decimal
import statistics
import math
import random

def generarRandom(cantidad):
  sucesion=[]
  for cuenta in range(cantidad):
      sucesion.append(round(random.random(),3))
  return sucesion

# GENERADORES DE NÚMEROS ALEATORIOS

def MetodoCongruencialLineal(x, a, b, mod, cantidad=0):
    print(cantidad)
    x=int(x)
    a=int(a)
    b=int(b)
    mod=int(mod)
    periodo = 0
    bandera = 0
    nrosAleatoriosGenerados=[]
    nros=[]
    resultado=''

    while(True):
        x = (((a * x) + b) % mod)
        if((periodo!=0 and x in nros) or (cantidad!=0 and len(nrosAleatoriosGenerados)==cantidad)):
          break
        nros.append(x)
        nroAleatorio=round(int(x)/mod,3)
        nrosAleatoriosGenerados.append(nroAleatorio)
        periodo += 1

    if(periodo == mod):
        resultado+="El generador es de ciclo completo\n"
    elif periodo < cantidad:
        resultado+="El generador es de ciclo incompleto\n"    
    resultado+="La longitud del período es: "+str(periodo)+"\n"
    resultado+="Los números aleatorios generados son: \n"+str(nrosAleatoriosGenerados)
    return resultado, nrosAleatoriosGenerados

def MetodoCongruencialMultiplicativo(x, a, mod):

    x=int(x)
    a=int(a)
    mod=int(mod)
    periodo = 0
    bandera = 0
    nrosAleatoriosGenerados=[]
    nros=[]
    resultado=''

    while(True):
        x = ((int(a) * int(x)) % int(mod))
        if(periodo!=0 and x in nros):
          break
        nros.append(x)
        nroAleatorio=round(int(x)/mod,3)
        nrosAleatoriosGenerados.append(nroAleatorio)
        periodo = periodo + 1

    if(periodo == mod):
        resultado+="El generador es de ciclo completo\n"
    else:
        resultado+="El generador es de ciclo incompleto\n"
    resultado+="La longitud del período es: {}\n".format(periodo)
    resultado+="Los números aleatorios generados son "+str(nrosAleatoriosGenerados)
    return resultado 

def MetodoCuadradosMedios(x, longitud, cantidad=0):

    longitud=int(longitud)
    x=int(x)
    nroAleatorio=0
    cuadradoSemilla=0
    nroMax=0
    longitudNro=0
    nroCompleto=0
    parteCentral=0
    valorParaNormalizar=10**longitud
    contador=0
    nrosAleatorios=[]
    nros=[]
    resultado=''

    while(True):
        cuadradoSemilla=int(x)**2
        nroMax=int('9'*longitud)**2
        longitudNroMax=int(len(str(nroMax)))
        nroCompleto=str(cuadradoSemilla).ljust(longitudNroMax,'0')
        indiceInicial=int((longitud/2))
        indiceFinal=int(indiceInicial+longitud)
        parteCentral=nroCompleto[indiceInicial:indiceFinal]
        x = parteCentral
        nroAleatorio=round(int(x)/valorParaNormalizar,3)

        if (x in nros or (cantidad!=0 and len(nrosAleatorios)==cantidad)):
          break
        nros.append(x)
        nrosAleatorios.append(nroAleatorio)
        contador=int(contador)+1

    print(contador)
    print(nros)
    print(nrosAleatorios)
    resultado+="Los números aleatorios generados son: {}\n La cantidad de números generados sin repetir son: {}".format(nrosAleatorios, len(nrosAleatorios))
   
    return resultado, nrosAleatorios

def MetodoProductosMedios(x, y, longitud, cantidadGenerar):
    longitud=int(longitud)
    x=int(x)
    y=int(y)
    cantidadGenerar=int(cantidadGenerar)
    nroAleatorio=0
    productoSemillas=0
    nroMax=0
    longitudNro=0
    nroCompleto=0
    parteCentral=0
    valorParaNormalizar=10**longitud
    contador=1
    nrosAleatorios=[]
    nros=[]
    resultado=''

    while(contador<=cantidadGenerar):
        productoSemillas=int(x*y)
        nroMax=int('9'*longitud)**2
        longitudNroMax=int(len(str(nroMax)))
        nroCompleto=str(productoSemillas).ljust(longitudNroMax,'0')
        indiceInicial=int((longitud/2))
        indiceFinal=int(indiceInicial+longitud)
        parteCentral=nroCompleto[indiceInicial:indiceFinal]
        x = y
        y=int(parteCentral)
        if(y in nros):
          break
        nros.append(y)
        nroAleatorio=round(y/valorParaNormalizar,3)
        nrosAleatorios.append(nroAleatorio)
        contador=int(contador)+1
    print(contador)
    print(nros)
    resultado+="Los números aleatorios generados son: {} \n La cantidad de números generados sin repetir son: {}".format(nrosAleatorios, len(nrosAleatorios))
   
    return resultado, nrosAleatorios

def MetodoCongruencialAditivo(secuencia, mod, cantidad):
    secuenciaCompleta=secuencia
    mod=int(mod)
    cantidad=int(cantidad)
    nrosAleatorios=[]
    iteraciones=cantidad
    resultado=''

    for i in range(iteraciones):
      longitud=len(secuenciaCompleta)
      x=int((int(secuenciaCompleta[longitud-1])+int(secuenciaCompleta[i]))%mod)
      if x in secuenciaCompleta:
        break
      secuenciaCompleta.append(x)
      nroAleatorio=round(x/(mod-1),3)
      nrosAleatorios.append(nroAleatorio)

    resultado+="Los números aleatorios generados son: {} \n La cantidad de números generados sin repetir son: {}".format(nrosAleatorios, len(nrosAleatorios))
    print(secuenciaCompleta)
    return resultado, nrosAleatorios


# PRUEBAS PARA REALIZAR A LOS GENERADORES

def prueba_chi2(sucesion, chi2):

    chi2_suma = 0
    chi2=float(chi2)
    sucesion2=[float(x) for x in sucesion]
    resultado=''

    # Calcula media esperada a partir de la sucesion de números observados
    frec_esperada= statistics.mean(sucesion2)
    resultado+="La frecuencia esperada es {}\n".format(frec_esperada) 

    # Determina el valor chi cuadrada a partir de cada elemento de la sucesión de números observados y la frecuencia esperada
    for elemento in sucesion2:

        chi2_suma = chi2_suma + (((elemento-frec_esperada)**2)/frec_esperada)

    # Criterio de aceptación
    if chi2_suma < chi2:
        resultado+="La hipotesis se acepta. El estadístico calculado a partir de la observación es {} < que el estadístico de la tabla: {}".format(chi2_suma, chi2)
    else:
        resultado+="La hipotesis se rechaza. El estadístico calculado a partir de la observación es {} > que el estadístico de la tabla: {}".format(chi2_suma, chi2)

    return resultado

def prueba_ks(sucesion, ks):
  #sucesion2=[float (x) for x in sucesion]
  sucesion_ordenada=sorted(sucesion)
  ks=float(ks)
  valor_absoluto=[]
  resultado=''
  j=1
  for numero in sucesion_ordenada:
    vabs=abs(numero-float(j/len(sucesion_ordenada)))
    valor_absoluto.append(vabs)
    j=j+1

  if(max(valor_absoluto)<ks):
    resultado+="Se acepta la prueba. El estadístico calculado a partir de la observación es {} < que el estadístico de la tabla: {}".format(max(valor_absoluto), ks)
  else:
    resultado+="No se acepta la prueba. El estadístico calculado a partir de la observación es {} > que el estadístico de la tabla: {}".format(max(valor_absoluto),ks)

  return resultado

def prueba_rachas(sucesion, z):
  z=float(z)
  n1=0
  n2=0
  sucesion_rachas=[]
  b=1
  N=len(sucesion)
  resultado=''

  for nro in sucesion:
    if(nro<0.5):
      n1=n1+1
      sucesion_rachas.append("-")
    else:
      n2=n2+1
      sucesion_rachas.append("+")

  for i in range(1,len(sucesion_rachas)):
    if(sucesion_rachas[i-1]==sucesion_rachas[i]):
      b=b+1

  media=(2*n1*n2/N)+1/2
  varianza=(2*n1*n2*(2*n1*n2-N))/((N**2)*(N-1))
  desviacion_estandar=math.sqrt(varianza)
  estadistico=(b-media)/desviacion_estandar

  if(z*(-1)<=estadistico<=z):
    resultado+="Se acepta la prueba. El valor estadístico observado {} se encuentra entre {} y {}".format(estadistico, z*(-1), z)
  else:
    resultado+="No se acepta la prueba. El valor estadístico observado {} no se encuentra entre {} y {}".format(estadistico, z*(-1), z)

  return resultado

def prueba_media(sucesion, z):
  z=float(z)
  resultado=''
  n=len(sucesion)
  promedio=sum(sucesion)/n
  lim_inferior=(1/2)-z*(1/math.sqrt(12*n))
  lim_superior=(1/2)+z*(1/math.sqrt(12*n))
  if(lim_inferior<promedio and promedio<lim_superior):
    resultado+="Se acepta la prueba. El valor de la media {} se encuentra entre {} y {}".format(promedio, lim_inferior, lim_superior)
  else:
    resultado+="No se acepta la prueba. El valor de la media {} no se encuentra entre {} y {}".format(promedio, lim_inferior, lim_superior)

  return resultado

def prueba_varianza(sucesion, chi1, chi2):
  chi1=float(chi1)
  chi2=float(chi2)
  resultado=''
  print(sucesion)
  #sucesion2=[float(x) for x in sucesion]
  n=len(sucesion)
  promedio=sum(sucesion)/n
  varianza=0
  sumatoria=0
  lim_inferior=chi1/(12*(n-1))
  lim_superior=chi2/(12*(n-1))
  for i in range(n):
    sumatoria+=(sucesion[i]-promedio)**2
  varianza=sumatoria/(n-1)
  if(lim_inferior<varianza and varianza<lim_superior):
    resultado+="Se acepta la prueba. El valor de la varianza {} se encuentra entre {} y {}".format(varianza, lim_inferior, lim_superior)
  else:
    resultado+="No se acepta la prueba. El valor de la varianza {} no se encuentra entre {} y {}".format(varianza, lim_inferior, lim_superior)

  return resultado


# GENERACIÓN DE VARIABLES ALEATORIAS

def genera_va(frecAbs, valorVA, sucesion):

  resultado=''
  distProb = []
  frecAbs=[int(x) for x in frecAbs]
  cantNA = sum(frecAbs,0) #total de observaciones

  #calcula f(x) distribución de probabilidad
  for i in frecAbs:
      p = round(i/cantNA,2)
      distProb.append(p)

  print(f"Distribución de Probabilidad: {distProb}")

  # Calcular la Distribución Acumulativa
  distAc = []
  sumaFrec = 0

  for f in distProb:
      sumaFrec = round(sumaFrec + f, 2)
      distAc.append(sumaFrec)

  print(f"Distribución Acumulativa: {distAc}\n")

  contInt = []  #n

  for i in range(len(frecAbs)):
      contInt.append(0)

  numAleatorios = sucesion  #u
  varAleatorias = []  #x

  for l in range(len(numAleatorios)):
      i = 0 # Contador de intervalos

      while i < len(frecAbs): # Qué hace la estructura repetitiva while: determina a qué valor de x corresponde el nro aleatorio generado
        if numAleatorios[l] <= distAc[i]:
            varA = valorVA[i]
            contInt[i] = contInt[i] + 1
            varAleatorias.append(varA) # Guardar variable aleatoria en una lista
            break
        i += 1

  resultado+=f"La frecuencia relativa de cada valor de variable aleatoria es : {distProb}\n"

  resultado+=f"La frecuencia acumulativa a partir de la frecuenca relativa de cada valor de variable aleatoria es : {distAc}\n"

  # Mostrar resultados finales

  resultado+=f"Los números aleatorios generados para producir las variables aleatorias son : {numAleatorios}\n"

  for i in range(len(frecAbs)):
     # Agregue el nombre de la variable correcta para que se muestre Intervalo   Nombre de la Variable Aleatoria   Total de valores de la variable aleatoria generada
      if(i==0):
        resultado+=f"Intervalo 0 <= u <={distAc[i]}  Nombre VA {valorVA[i]}  Total de valores {contInt[i]}\n"
      else:
        resultado+=f"Intervalo {distAc[i-1]} <= u <={distAc[i]}  Nombre VA {valorVA[i]}  Total de valores {contInt[i]}\n"

  return resultado
