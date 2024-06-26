import tkinter as tk
from tkinter import messagebox
import funciones
import re

class PaginaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        #Variables generales a todos los frames
        self.semilla = tk.StringVar()
        self.semilla2 = tk.StringVar()
        self.multiplicador = tk.StringVar()
        self.incremento = tk.StringVar()
        self.modulo = tk.StringVar()
        self.cantidadGenerar = tk.StringVar()
        self.cantidadGenerarPruebas = tk.IntVar()
        self.longitud = tk.StringVar()
        self.secuencia = tk.StringVar()
        self.secuenciaVA = tk.StringVar()
        self.chi = tk.StringVar()
        self.chi2 = tk.StringVar()
        self.ks = tk.StringVar()
        self.z = tk.StringVar()
        self.intervaloSelect = tk.StringVar(value="5")
        self.intervaloSelectGenerador = tk.StringVar(value="1")
        self.variablesAleatorias = tk.StringVar()
        self.nrosAleatoriosGenerados=tk.StringVar()

        self.title("Simulador")
        #self.geometry("450x300")
        #self.resizable(False, False)

        # Contenedor principal donde se colocarán los frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Añadir los frames a la ventana principal
        for F in (FrameMenuPrincipal, FrameMenuNrosAleatorios, FrameMenuPruebas, FrameMenuVariablesAleatorias, 
            FrameCongruencialLinealMixto, FrameCongruencialLinealMultiplicativo, FrameCongruencialLinealAditivo,
            FrameCuadradosMedios, FrameProductosMedios, FrameChiCuadrada, FrameKolmogorovSmirnov, FrameRachas,
            FrameMedia, FrameVarianza, FrameTransformadaInversa):
            page_name = F.__name__
            if F in (FrameCongruencialLinealMixto, FrameCongruencialLinealAditivo, FrameCuadradosMedios, FrameProductosMedios):
                frame = F(parent=self.container, controller=self, mostrar_botones=True)
            else:
                frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar el frame inicial
        self.show_frame("FrameMenuPrincipal")

        self.configurar_ventana()

    def configurar_ventana(self):
        # Tamaño de la ventana
        width = 550
        height = 550

        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular posición para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Establecer tamaño y posición de la ventana
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_frame(self, page_name):
        self.limpiarCampos() #limpia los campos cada vez que cambia de frame
        '''Mostrar un frame determinado'''
        frame = self.frames[page_name]
        frame.tkraise()

    def aceptar(self, opcion, guardaGenerados=False, opcionSiguiente=None):
        if opcion=="1":
            print(self.cantidadGenerarPruebas)
            resultados, nrosAleatorios=funciones.MetodoCongruencialLineal(self.semilla.get(), self.multiplicador.get(), self.incremento.get(), self.modulo.get(), self.cantidadGenerarPruebas)
            if guardaGenerados:
                pregunta=messagebox.askquestion("", resultados+"\nDesea utilizar los números generados??")
                if pregunta=="yes":
                    self.nrosAleatoriosGenerados=nrosAleatorios
                    self.aceptar(opcionSiguiente)
            else:
                messagebox.showinfo("Resultado", resultados)
        elif opcion=="2":
            resultados=funciones.MetodoCongruencialMultiplicativo(self.semilla.get(), self.multiplicador.get(), self.modulo.get())
            messagebox.showinfo("Resultado", resultados)
        elif opcion=="3":
            #splitear la secuencia para que sea una lista y pasar esa por parámetro
            #secuencia=self.secuencia.get().split()
            cantidad=int(self.cantidadGenerar.get()) if self.cantidadGenerar.get() else self.cantidadGenerarPruebas
            resultados, nrosAleatorios=funciones.MetodoCongruencialAditivo(self.secuencia.get().split(","), self.modulo.get(), cantidad)
            if guardaGenerados:
                pregunta=messagebox.askquestion("", resultados+"\nDesea utilizar los números generados??")
                if pregunta=="yes":
                    self.nrosAleatoriosGenerados=nrosAleatorios
                    self.aceptar(opcionSiguiente)
            else:
                messagebox.showinfo("Resultado", resultados)
        elif opcion=="4":
            resultados, nrosAleatorios=funciones.MetodoCuadradosMedios(self.semilla.get(), self.longitud.get(), self.cantidadGenerarPruebas)
            if guardaGenerados:
                pregunta=messagebox.askquestion("", resultados+"\nDesea utilizar los números generados??")
                if pregunta=="yes":
                    self.nrosAleatoriosGenerados=nrosAleatorios
                    self.aceptar(opcionSiguiente)
            else:
                messagebox.showinfo("Resultado", resultados) 
        elif opcion=="5":
            cantidad=int(self.cantidadGenerar.get()) if self.cantidadGenerar.get() else self.cantidadGenerarPruebas
            resultados, nrosAleatorios=funciones.MetodoProductosMedios(self.semilla.get(), self.semilla2.get(), self.longitud.get(), cantidad)
            if guardaGenerados:
                pregunta=messagebox.askquestion("", resultados+"\nDesea utilizar los números generados??")
                if pregunta=="yes":
                    self.nrosAleatoriosGenerados=nrosAleatorios
                    self.aceptar(opcionSiguiente)
            else:
                messagebox.showinfo("Resultado", resultados)
        elif opcion=="6":
            resultados=funciones.prueba_chi2(self.secuencia.get().split(","), self.chi.get().replace(",", "."))
            messagebox.showinfo("Resultado", resultados)
        elif opcion=="7":
            resultados=funciones.prueba_ks(self.nrosAleatoriosGenerados, self.ks.get().replace(",", "."))
            messagebox.showinfo("Resultado", resultados)
        elif opcion=="8":
            resultados=funciones.prueba_rachas(self.nrosAleatoriosGenerados, self.z.get().replace(",", "."))
            messagebox.showinfo("Resultado", resultados)
        elif opcion=="9":
            resultados=funciones.prueba_media(self.nrosAleatoriosGenerados, self.z.get().replace(",", "."))
            messagebox.showinfo("Resultado", resultados)
        elif opcion=="10":
            resultados=funciones.prueba_varianza(self.nrosAleatoriosGenerados, self.chi.get().replace(",", "."), self.chi2.get().replace(",", "."))
            messagebox.showinfo("Resultado", resultados)
        elif opcion=="11":
            valoresObservados=self.secuenciaVA.get().split(",")
            variablesAleatorias=self.variablesAleatorias.get().split(",")
            resultados=funciones.genera_va(valoresObservados, variablesAleatorias, self.nrosAleatoriosGenerados)
            messagebox.showinfo("Resultado", resultados)

    def limpiarCampos(self):
        self.semilla.set('')
        self.multiplicador.set('')
        self.incremento.set('')
        self.modulo.set('')
        self.cantidadGenerar.set('')
        self.longitud.set('')
        self.secuencia.set('')
        self.semilla2.set('')
        self.chi.set('')
        self.chi2.set('')
        self.ks.set('')
        self.z.set('')
        self.intervaloSelect.set('5')
        self.intervaloSelectGenerador.set('1')
        self.variablesAleatorias.set('')

    def limpiarFramesHijos(self):
        self.semilla.set('')
        self.multiplicador.set('')
        self.incremento.set('')
        self.modulo.set('')
        self.longitud.set('')
        self.secuencia.set('')
        self.semilla2.set('')
        self.intervaloSelect.set('5')

class FrameMenuPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #label = tk.Label(self, text="Start Page")
        #label.pack(side="top", fill="x", pady=10)

        buttonNA = tk.Button(self, text="GENERAR NÚMEROS ALEATORIOS",
                            command=lambda: controller.show_frame("FrameMenuNrosAleatorios"))
        buttonNA.grid(row=0, column=1,padx=180, pady=20)

        buttonTest = tk.Button(self, text="TESTS DE ALEATORIEDAD",
                            command=lambda: controller.show_frame("FrameMenuPruebas"))
        buttonTest.grid(row=1, column=1,padx=180, pady=20)

        buttonVA = tk.Button(self, text="GENERAR VARIABLES ALEATORIAS",
                            command=lambda: controller.show_frame("FrameMenuVariablesAleatorias"))
        buttonVA.grid(row=2, column=1,padx=180, pady=20)

class FrameMenuNrosAleatorios(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        buttonCL = tk.Button(self, text="MÉTODO CONGRUENCIAL LINEAL MIXTO",
                            command=lambda: controller.show_frame("FrameCongruencialLinealMixto"))
        buttonCL.grid(row=0, column=1,padx=140, pady=20)

        buttonCA = tk.Button(self, text="MÉTODO CONGRUENCIAL LINEAL MULTIPLICATIVO",
                            command=lambda: controller.show_frame("FrameCongruencialLinealMultiplicativo"))
        buttonCA.grid(row=1, column=1,padx=140, pady=20)

        buttonCM = tk.Button(self, text="MÉTODO CONGRUENCIAL LINEAL ADITIVO",
                            command=lambda: controller.show_frame("FrameCongruencialLinealAditivo"))
        buttonCM.grid(row=2, column=1,padx=140, pady=20)

        buttonCuadMed = tk.Button(self, text="MÉTODO CUADRADOS MEDIOS",
                            command=lambda: controller.show_frame("FrameCuadradosMedios"))
        buttonCuadMed.grid(row=3, column=1,padx=140, pady=20)

        buttonProdMed = tk.Button(self, text="MÉTODO PRODUCTOS MEDIOS",
                            command=lambda: controller.show_frame("FrameProductosMedios"))
        buttonProdMed.grid(row=4, column=1,padx=140, pady=20)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPrincipal"))
        buttonVolver.grid(row=5, column=1,padx=180, pady=20)

class FrameMenuPruebas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        buttonChi = tk.Button(self, text="PRUEBA DE LA CHI CUADRADA",
                            command=lambda: controller.show_frame("FrameChiCuadrada"))
        buttonChi.grid(row=0, column=1,padx=180, pady=20)

        buttonKS = tk.Button(self, text="PRUEBA DE KOLMOGOROV SMIRNOV",
                            command=lambda: controller.show_frame("FrameKolmogorovSmirnov"))
        buttonKS.grid(row=1, column=1,padx=180, pady=20)

        buttonRachas = tk.Button(self, text="TEST DE RACHAS",
                            command=lambda: controller.show_frame("FrameRachas"))
        buttonRachas.grid(row=2, column=1,padx=180, pady=20)

        buttonMedia = tk.Button(self, text="PRUEBA DE MEDIAS",
                            command=lambda: controller.show_frame("FrameMedia"))
        buttonMedia.grid(row=3, column=1,padx=180, pady=20)

        buttonVarianza = tk.Button(self, text="PRUEBA DE VARIANZA",
                            command=lambda: controller.show_frame("FrameVarianza"))
        buttonVarianza.grid(row=4, column=1,padx=180, pady=20)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPrincipal"))
        buttonVolver.grid(row=5, column=1,padx=200, pady=20)

class FrameMenuVariablesAleatorias(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        buttonTransfInv = tk.Button(self, text="MÉTODO DE LA TRANSFORMADA INVERSA PARA DISCRETAS",
                            command=lambda: controller.show_frame("FrameTransformadaInversa"))
        buttonTransfInv.grid(row=0, column=1,padx=110, pady=20)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPrincipal"))
        buttonVolver.grid(row=1, column=1,padx=130, pady=20)

class FrameCongruencialLinealMixto(tk.Frame):
    def __init__(self, parent, controller, mostrar_botones=True, framePadre=None):
        super().__init__(parent)
        self.controller = controller
        self.mostrar_botones=mostrar_botones
        self.padre=framePadre

        # Determinar la fuente de las variables
        
        self.variable_source = self.controller

        labelSemilla = tk.Label(self, text="Semilla")
        labelSemilla.grid(row=0, column=0,padx=90, pady=10)

        entrySemilla = tk.Entry(self, textvariable=self.variable_source.semilla)
        entrySemilla.grid(row=0, column=1,padx=90, pady=10)

        labelMultiplicador = tk.Label(self, text="Multiplicador")
        labelMultiplicador.grid(row=1, column=0,padx=90, pady=10)

        entryMultiplicador = tk.Entry(self, textvariable=self.variable_source.multiplicador)
        entryMultiplicador.grid(row=1, column=1,padx=90, pady=10)

        labelIncremento = tk.Label(self, text="Incremento")
        labelIncremento.grid(row=2, column=0,padx=90, pady=10)

        entryIncremento = tk.Entry(self, textvariable=self.variable_source.incremento)
        entryIncremento.grid(row=2, column=1,padx=90, pady=10)

        labelModulo = tk.Label(self, text="Módulo")
        labelModulo.grid(row=3, column=0,padx=90, pady=10)

        entryModulo = tk.Entry(self, textvariable=self.variable_source.modulo)
        entryModulo.grid(row=3, column=1,padx=90, pady=10)

        if mostrar_botones:
            buttonAceptar = tk.Button(self, text="Aceptar",
                                command= self.validaciones)
            buttonAceptar.grid(row=4, column=0,padx=90, pady=50)

            buttonVolver = tk.Button(self, text="Volver",
                               command=lambda: controller.show_frame("FrameMenuNrosAleatorios"))
            buttonVolver.grid(row=4, column=1,padx=90, pady=50)

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        semilla=int(self.variable_source.semilla.get()) if self.variable_source.semilla.get() else 0
        multiplicador=int(self.variable_source.multiplicador.get()) if self.variable_source.multiplicador.get() else 0
        modulo=int(self.variable_source.modulo.get()) if self.variable_source.modulo.get() else 0
        incremento=int(self.variable_source.incremento.get()) if self.variable_source.incremento.get() else 1
        if(semilla<=0):
            mensaje+="La semilla debe ser mayor a 0\n"
            mostrarMensaje=True
        if(multiplicador<=0 or multiplicador>modulo):
            mensaje+="El multiplicador debe ser >0 y < al módulo\n"
            mostrarMensaje=True
        if(incremento>modulo):
            mensaje+="El incremento debe ser < al módulo\n"
            mostrarMensaje=True
        if(modulo==0):
            mensaje+="El módulo no puede ser 0\n"
            mostrarMensaje=True
        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
        elif not self.mostrar_botones:
            opcionSiguiente=''
            if(self.padre=="KS"):
                opcionSiguiente="7"
            elif self.padre=="Rachas":
                opcionSiguiente="8"
            elif self.padre=="media":
                opcionSiguiente="9"
            elif self.padre=="varianza": 
                opcionSiguiente="10"
            else:
                opcionSiguiente="11"
            self.variable_source.aceptar("1", True, opcionSiguiente)
        else:
            self.variable_source.aceptar("1")

class FrameCongruencialLinealMultiplicativo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelSemilla = tk.Label(self, text="Semilla")
        labelSemilla.grid(row=0, column=0,padx=90, pady=10)

        entrySemilla = tk.Entry(self, textvariable=self.controller.semilla)
        entrySemilla.grid(row=0, column=1,padx=90, pady=10)

        labelMultiplicador = tk.Label(self, text="Multiplicador")
        labelMultiplicador.grid(row=1, column=0,padx=90, pady=10)

        entryMultiplicador = tk.Entry(self, textvariable=self.controller.multiplicador)
        entryMultiplicador.grid(row=1, column=1,padx=90, pady=10)

        labelModulo = tk.Label(self, text="Módulo")
        labelModulo.grid(row=2, column=0,padx=90, pady=10)

        entryModulo = tk.Entry(self, textvariable=self.controller.modulo)
        entryModulo.grid(row=2, column=1,padx=90, pady=10)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.validaciones)
        buttonAceptar.grid(row=3, column=0,padx=90, pady=50)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuNrosAleatorios"))
        buttonVolver.grid(row=3, column=1,padx=90, pady=50)

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        semilla=int(self.controller.semilla.get()) if self.controller.semilla.get() else 0
        multiplicador=int(self.controller.multiplicador.get()) if self.controller.multiplicador.get() else 0
        modulo=int(self.controller.modulo.get()) if self.controller.modulo.get() else 0
        if(semilla<=0):
            mensaje+="La semilla debe ser mayor a 0\n"
            mostrarMensaje=True
        if(multiplicador<=0 or multiplicador>modulo):
            mensaje+="El multiplicador debe ser >0 y < al módulo\n"
            mostrarMensaje=True
        if(modulo==0):
            mensaje+="El módulo no puede ser 0\n"
            mostrarMensaje=True
        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
        else:
            self.controller.aceptar("2")

class FrameCongruencialLinealAditivo(tk.Frame):
    def __init__(self, parent, controller, mostrar_botones=True, framePadre=None):
        super().__init__(parent)
        self.controller = controller
        self.mostrar_botones=mostrar_botones
        self.padre=framePadre

        # Determinar la fuente de las variables
        
        self.variable_source = self.controller

        labelSecuencia = tk.Label(self, text="Secuencia inicial")
        labelSecuencia.grid(row=0, column=0,padx=80, pady=10)

        entrySecuencia = tk.Entry(self, textvariable=self.variable_source.secuencia)
        entrySecuencia.grid(row=0, column=1,padx=80, pady=10)

        labelAdvSec = tk.Label(self, text="Ingrese los números separados por una coma sin espacios", fg="red",wraplength=400, justify="center")
        labelAdvSec.grid(row=1, column=0,columnspan=3, padx=0, pady=10)
       
        labelModulo = tk.Label(self, text="Módulo")
        labelModulo.grid(row=3, column=0,padx=80, pady=10)

        entryModulo = tk.Entry(self, textvariable=self.variable_source.modulo)
        entryModulo.grid(row=3, column=1,padx=80, pady=10)

        if mostrar_botones:
            labelCantidadGenerar = tk.Label(self, text="Cantidad a generar")
            labelCantidadGenerar.grid(row=2, column=0,padx=80, pady=10)

            entryCantidadGenerar = tk.Entry(self, textvariable=self.variable_source.cantidadGenerar)
            entryCantidadGenerar.grid(row=2, column=1,padx=80, pady=10)

            buttonAceptar = tk.Button(self, text="Aceptar",
                                command=self.validaciones)
            buttonAceptar.grid(row=4, column=0,padx=80, pady=50)

            buttonVolver = tk.Button(self, text="Volver",
                               command=lambda: controller.show_frame("FrameMenuNrosAleatorios"))
            buttonVolver.grid(row=4, column=1,padx=80, pady=50)

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        secuenciaInicial=self.variable_source.secuencia.get().replace(" ", "")
        cantidad=int(self.variable_source.cantidadGenerar.get()) if self.variable_source.cantidadGenerar.get() else 0
        modulo=int(self.variable_source.modulo.get()) if self.variable_source.modulo.get() else 0
        patron=re.compile(r'[^\w\s,]')
        if(not secuenciaInicial or ',' not in secuenciaInicial or patron.search(secuenciaInicial)):
            mensaje+="La secuencia deben ser números separados por comas sin espacios\n"
            mostrarMensaje=True
        if(cantidad<=0 or cantidad>modulo):
            mensaje+="La cantidad a generar debe ser >0 y < al módulo\n"
            mostrarMensaje=True
        if(modulo==0):
            mensaje+="El módulo no puede ser 0\n"
            mostrarMensaje=True
        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
        elif not self.mostrar_botones:
            if(self.padre=="KS"):
                opcionSiguiente="7"
            elif self.padre=="Rachas":
                opcionSiguiente="8"
            elif self.padre=="media":
                opcionSiguiente="9"
            else: 
                opcionSiguiente="10"
            self.variable_source.aceptar("3", True, opcionSiguiente)
        else:
            self.variable_source.aceptar("3")

class FrameCuadradosMedios(tk.Frame):
    def __init__(self, parent, controller, mostrar_botones=True, framePadre=None):
        super().__init__(parent)
        self.controller = controller
        self.mostrar_botones=mostrar_botones
        self.padre=framePadre

        # Determinar la fuente de las variables
        
        self.variable_source = self.controller

        labelSemilla = tk.Label(self, text="Semilla")
        labelSemilla.grid(row=0, column=0,padx=70, pady=10)

        entrySemilla = tk.Entry(self, textvariable=self.variable_source.semilla)
        entrySemilla.grid(row=0, column=1,padx=70, pady=10)

        labelCantidadGenerar = tk.Label(self, text="Longitud del nro aleatorio")
        labelCantidadGenerar.grid(row=1, column=0,padx=70, pady=10)

        entryCantidadGenerar = tk.Entry(self, textvariable=self.variable_source.longitud)
        entryCantidadGenerar.grid(row=1, column=1,padx=70, pady=10)

        if mostrar_botones:
            buttonAceptar = tk.Button(self, text="Aceptar",
                                command=self.validaciones)
            buttonAceptar.grid(row=2, column=0,padx=70, pady=50)

            buttonVolver = tk.Button(self, text="Volver",
                               command=lambda: controller.show_frame("FrameMenuNrosAleatorios"))
            buttonVolver.grid(row=2, column=1,padx=70, pady=50)

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        semilla=int(self.variable_source.semilla.get()) if self.variable_source.semilla.get() else 0
        longitud=int(self.variable_source.longitud.get()) if self.variable_source.longitud.get() else 0
        if(semilla<=0):
            mensaje+="La semilla debe ser > 0\n"
            mostrarMensaje=True
        if(longitud<=0):
            mensaje+="La longitud del número aleatorio debe ser > 0\n"
            mostrarMensaje=True
        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
        elif not self.mostrar_botones:
            if(self.padre=="KS"):
                opcionSiguiente="7"
            elif self.padre=="Rachas":
                opcionSiguiente="8"
            elif self.padre=="media":
                opcionSiguiente="9"
            else: 
                opcionSiguiente="10"
            self.variable_source.aceptar("4", True, opcionSiguiente)
        else:
            self.variable_source.aceptar("4")

class FrameProductosMedios(tk.Frame):
    def __init__(self, parent, controller, mostrar_botones=True, framePadre=None):
        super().__init__(parent)
        self.controller = controller
        self.mostrar_botones=mostrar_botones
        self.padre=framePadre

        # Determinar la fuente de las variables
        
        self.variable_source = self.controller

        labelSemilla = tk.Label(self, text="Semilla")
        labelSemilla.grid(row=0, column=0,padx=70, pady=10)

        entrySemilla = tk.Entry(self, textvariable=self.variable_source.semilla)
        entrySemilla.grid(row=0, column=1,padx=70, pady=10)

        labelSemilla2 = tk.Label(self, text="Semilla2")
        labelSemilla2.grid(row=1, column=0,padx=70, pady=10)

        entrySemilla2 = tk.Entry(self, textvariable=self.variable_source.semilla2)
        entrySemilla2.grid(row=1, column=1,padx=70, pady=10)

        labelLongitud = tk.Label(self, text="Longitud del nro aleatorio")
        labelLongitud.grid(row=2, column=0,padx=70, pady=10)

        entryLongitud = tk.Entry(self, textvariable=self.variable_source.longitud)
        entryLongitud.grid(row=2, column=1,padx=70, pady=10)

        if mostrar_botones:
            labelCantidadGenerar = tk.Label(self, text="Cantidad a generar")
            labelCantidadGenerar.grid(row=3, column=0,padx=70, pady=10)

            entryCantidadGenerar = tk.Entry(self, textvariable=self.variable_source.cantidadGenerar)
            entryCantidadGenerar.grid(row=3, column=1,padx=70, pady=10)
            buttonAceptar = tk.Button(self, text="Aceptar",
                                command=self.validaciones)
            buttonAceptar.grid(row=4, column=0,padx=70, pady=50)

            buttonVolver = tk.Button(self, text="Volver",
                               command=lambda: controller.show_frame("FrameMenuNrosAleatorios"))
            buttonVolver.grid(row=4, column=1,padx=70, pady=50)

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        semilla=int(self.variable_source.semilla.get()) if self.variable_source.semilla.get() else 0
        semilla2=int(self.variable_source.semilla2.get()) if self.variable_source.semilla2.get() else 0
        cantidad=int(self.variable_source.cantidadGenerar.get()) if self.variable_source.cantidadGenerar.get() else 0
        longitud=int(self.variable_source.longitud.get()) if self.variable_source.longitud.get() else 0
        if(semilla <=0 or semilla2<=0):
            mensaje+="Las semillas deben ser > 0\n"
            mostrarMensaje=True
        if(cantidad<=0):
            mensaje+="La cantidad a generar debe ser > 0\n"
            mostrarMensaje=True
        if(longitud<=0):
            mensaje+="La longitud del número aleatorio debe ser > 0\n"
            mostrarMensaje=True
        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
        elif not self.mostrar_botones:
            if(self.padre=="KS"):
                opcionSiguiente="7"
            elif self.padre=="Rachas":
                opcionSiguiente="8"
            elif self.padre=="media":
                opcionSiguiente="9"
            else: 
                opcionSiguiente="10"
            self.variable_source.aceptar("5", True, opcionSiguiente)
        else:
            self.variable_source.aceptar("5")

class FrameChiCuadrada(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelChi = tk.Label(self, text="Chi cuadrada (tabla)")
        labelChi.grid(row=0, column=0,padx=80, pady=5)

        entryChi = tk.Entry(self, textvariable=self.controller.chi)
        entryChi.grid(row=0, column=1,padx=80, pady=5)

        labelIntervalos = tk.Label(self, text="Intervalos")
        labelIntervalos.grid(row=1, column=0, rowspan=4,padx=80, pady=2)

        radioIntervalo1 = tk.Radiobutton(self, text="5", variable=self.controller.intervaloSelect, value="5")
        radioIntervalo1.grid(row=1, column=1,padx=80, pady=2)

        radioIntervalo2 = tk.Radiobutton(self, text="10", variable=self.controller.intervaloSelect, value="10")
        radioIntervalo2.grid(row=2, column=1,padx=80, pady=2)

        radioIntervalo3 = tk.Radiobutton(self, text="15", variable=self.controller.intervaloSelect, value="15")
        radioIntervalo3.grid(row=3, column=1,padx=80, pady=2)

        radioIntervalo4 = tk.Radiobutton(self, text="20", variable=self.controller.intervaloSelect, value="20")
        radioIntervalo4.grid(row=4, column=1,padx=80, pady=2)

        labelFA = tk.Label(self, text="Valores observados")
        labelFA.grid(row=5, column=0,padx=80, pady=2)

        entryFA = tk.Entry(self, textvariable=self.controller.secuencia)
        entryFA.grid(row=5, column=1,padx=80, pady=2)

        labelAdvSec = tk.Label(self, text="Recuerde ingresar la cantidad de valores acorde a la cantidad de intervalos seleccionados\nIngrese los números separados por una coma sin espacios", fg="red",wraplength=420, justify="center")
        labelAdvSec.grid(row=6, column=0,columnspan=3, padx=0, pady=5)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.validaciones)
        buttonAceptar.grid(row=7, column=0,padx=80, pady=50)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPruebas"))
        buttonVolver.grid(row=7, column=1,padx=80, pady=50)

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        chi=self.controller.chi.get().replace(",", ".")
        valoresObservados=self.controller.secuencia.get()
        intervalo=self.controller.intervaloSelect.get()
        patron=re.compile(r'[^\w\s,]')
        if(not chi):
            mensaje+="Debe ingresar el valor de tabla para chi cuadrada\n"
            mostrarMensaje=True
        if(not valoresObservados or ',' not in valoresObservados or patron.search(valoresObservados)):
            mensaje+="Los valores observados deben ser números separados por coma sin espacios\n"
            mostrarMensaje=True
        elif ',' in valoresObservados:
            valoresObservados=valoresObservados.split(",")
            if(len(valoresObservados)!=int(intervalo)):
                mensaje+="No coincide la cantidad de valores observados con el intervalo seleccionado\n"
                mostrarMensaje=True
        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
        else:
            self.controller.aceptar("6")

class FrameKolmogorovSmirnov(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelKS = tk.Label(self, text="KS (tabla)")
        labelKS.grid(row=0, column=0,padx=50, pady=10)

        entryKS = tk.Entry(self, textvariable=self.controller.ks)
        entryKS.grid(row=0, column=1,padx=50, pady=10)

        labelCantidadGenerar = tk.Label(self, text="Cantidad de números aleatorios")
        labelCantidadGenerar.grid(row=1, column=0,padx=50, pady=10)

        entryCantidadGenerar = tk.Entry(self, textvariable=self.controller.cantidadGenerar)
        entryCantidadGenerar.grid(row=1, column=1,padx=50, pady=10)

        labelIntervalos = tk.Label(self, text="Generación de números aleatorios")
        labelIntervalos.grid(row=2, column=0, rowspan=3,padx=50, pady=2)

        radioIntervalo1 = tk.Radiobutton(self, text="Función random", variable=self.controller.intervaloSelectGenerador, value="1", command=self.show_selected_frame)
        radioIntervalo1.grid(row=3, column=1,padx=50, pady=2)

        radioIntervalo2 = tk.Radiobutton(self, text="Congruencial mixto", variable=self.controller.intervaloSelectGenerador, value="FrameCongruencialLinealMixto", command=self.show_selected_frame)
        radioIntervalo2.grid(row=4, column=1,padx=50, pady=2)

        radioIntervalo4 = tk.Radiobutton(self, text="Cuadrados medios", variable=self.controller.intervaloSelectGenerador, value="FrameCuadradosMedios", command=self.show_selected_frame)
        radioIntervalo4.grid(row=5, column=1,padx=50, pady=2)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.aceptar)
        buttonAceptar.grid(row=7, column=0,padx=50, pady=50)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPruebas"))
        buttonVolver.grid(row=7, column=1,padx=50, pady=50)

        # Contenedor para los frames
        self.frame_container = tk.Frame(self)
        self.frame_container.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # Frames a ser mostrados
        self.frames = {}
        
        for F in (FrameCongruencialLinealMixto, FrameCuadradosMedios):
            #mostrar_botones = False if F == FrameCongruencialLinealMixto else True
            #caller = "KS" if F == FrameCongruencialLinealMixto else None
            frame = F(parent=self.frame_container, controller=self.controller, mostrar_botones=False, framePadre="KS")
            
            self.frames[F.__name__] = frame
            frame.grid(row=6, column=0, sticky="nsew")

        self.show_selected_frame()

    def show_selected_frame(self):
        self.controller.limpiarFramesHijos()
        selected = self.controller.intervaloSelectGenerador.get()

        # Ocultar todos los frames primero
        for frame in self.frames.values():
            frame.grid_remove()

        if selected == "1":
            # No mostrar ningún frame, ya que "Función random" no tiene uno asociado
            pass
        elif selected in self.frames:
            frame = self.frames[selected]
            frame.grid(row=6, column=0, sticky="nsew")
            frame.tkraise()

    def validaciones(self):
        mensaje=''
        mostrarMensaje=False
        cantidad = int(self.controller.cantidadGenerar.get()) if self.controller.cantidadGenerar.get() else 0
        ks = self.controller.ks.get().replace(",", ".")
        if(not ks):
            mensaje+="Debe ingresar el valor de tabla ks\n"
            mostrarMensaje=True
        if(not cantidad or cantidad<=0):
            mensaje+="Debe ingresar la cantidad a generar"
            mostrarMensaje=True

        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
            return None, None
        else:
            return cantidad, ks

    def aceptar(self):
        selected = self.controller.intervaloSelectGenerador.get()
        cantidad, ks=self.validaciones()
        if selected=="1":
            sucesion=funciones.generarRandom(cantidad)
            self.controller.nrosAleatoriosGenerados=sucesion
            self.controller.aceptar("7")
        else:
            self.controller.cantidadGenerarPruebas=cantidad
            frameHijo = self.frames[selected]
            frameHijo.validaciones()
            
class FrameRachas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelZ = tk.Label(self, text="Z (tabla)")
        labelZ.grid(row=0, column=0,padx=50, pady=10)

        entryZ = tk.Entry(self, textvariable=self.controller.z)
        entryZ.grid(row=0, column=1,padx=50, pady=10)

        labelCantidadGenerar = tk.Label(self, text="Cantidad de números aleatorios")
        labelCantidadGenerar.grid(row=2, column=0,padx=50, pady=10)

        entryCantidadGenerar = tk.Entry(self, textvariable=self.controller.cantidadGenerar)
        entryCantidadGenerar.grid(row=2, column=1,padx=50, pady=10)

        labelIntervalos = tk.Label(self, text="Generación de números aleatorios")
        labelIntervalos.grid(row=3, column=0, rowspan=3,padx=50, pady=2)

        radioIntervalo1 = tk.Radiobutton(self, text="Función random", variable=self.controller.intervaloSelectGenerador, value="1", command=self.show_selected_frame)
        radioIntervalo1.grid(row=3, column=1,padx=50, pady=2)

        radioIntervalo3 = tk.Radiobutton(self, text="Congruencial aditivo", variable=self.controller.intervaloSelectGenerador, value="FrameCongruencialLinealAditivo", command=self.show_selected_frame)
        radioIntervalo3.grid(row=4, column=1,padx=50, pady=2)

        radioIntervalo5 = tk.Radiobutton(self, text="Productos medios", variable=self.controller.intervaloSelectGenerador, value="FrameProductosMedios", command=self.show_selected_frame)
        radioIntervalo5.grid(row=5, column=1,padx=50, pady=2)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.aceptar)
        buttonAceptar.grid(row=7, column=0,padx=50, pady=50)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPruebas"))
        buttonVolver.grid(row=7, column=1,padx=50, pady=50)

        # Contenedor para los frames
        self.frame_container = tk.Frame(self)
        self.frame_container.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # Frames a ser mostrados
        self.frames = {}
        
        for F in (FrameCongruencialLinealAditivo, FrameProductosMedios):
            #mostrar_botones = False if F == FrameCongruencialLinealMixto else True
            #caller = "KS" if F == FrameCongruencialLinealMixto else None
            frame = F(parent=self.frame_container, controller=self.controller, mostrar_botones=False, framePadre="Rachas")
            
            self.frames[F.__name__] = frame
            frame.grid(row=6, column=0, sticky="nsew")


        self.show_selected_frame()

    def show_selected_frame(self):
        self.controller.limpiarFramesHijos()
        '''Mostrar el frame seleccionado por el radio button'''
        selected = self.controller.intervaloSelectGenerador.get()

        # Ocultar todos los frames primero
        for frame in self.frames.values():
            frame.grid_remove()

        if selected == "1":
            # Mostrar el frame correspondiente a "Función random"
            # No hay necesidad de mostrar ningún frame, ya que "Función random" no tiene un frame asociado
            pass
        elif selected in self.frames:
            frame = self.frames[selected]
            frame.grid(row=6, column=0, sticky="nsew")
            frame.tkraise()

    def validaciones(self):
        mensaje=''
        mostrarMensaje=False
        z = self.controller.z.get().replace(",", ".")
        cantidad = int(self.controller.cantidadGenerar.get()) if self.controller.cantidadGenerar.get() else 0
        if(not z):
            mensaje+="Debe ingresar el valor de tabla z\n"
            mostrarMensaje=True

        if(not cantidad or cantidad<=0):
            mensaje+="Debe ingresar la cantidad a generar"
            mostrarMensaje=True

        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
            return None, None
        else:
            return cantidad, z

    def aceptar(self):
        selected = self.controller.intervaloSelectGenerador.get()
        cantidad, z=self.validaciones()
        if z:
            if selected=="1":
                sucesion=funciones.generarRandom(cantidad)
                self.controller.nrosAleatoriosGenerados=sucesion
                self.controller.aceptar("8")
            else:
                self.controller.cantidadGenerarPruebas=cantidad
                frameHijo = self.frames[selected]
                frameHijo.validaciones()
            
class FrameMedia(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelZ = tk.Label(self, text="Z (tabla)")
        labelZ.grid(row=0, column=0,padx=60, pady=10)

        entryZ = tk.Entry(self, textvariable=self.controller.z)
        entryZ.grid(row=0, column=1,padx=60, pady=10)

        labelCantidadGenerar = tk.Label(self, text="Cantidad de números aleatorios")
        labelCantidadGenerar.grid(row=2, column=0,padx=60, pady=10)

        entryCantidadGenerar = tk.Entry(self, textvariable=self.controller.cantidadGenerar)
        entryCantidadGenerar.grid(row=2, column=1,padx=60, pady=10)

        labelIntervalos = tk.Label(self, text="Generación de números aleatorios")
        labelIntervalos.grid(row=3, column=0, rowspan=3,padx=60, pady=2)

        radioIntervalo1 = tk.Radiobutton(self, text="Función random", variable=self.controller.intervaloSelectGenerador, value="1", command=self.show_selected_frame)
        radioIntervalo1.grid(row=3, column=1,padx=60, pady=2)

        radioIntervalo3 = tk.Radiobutton(self, text="Congruencial mixto", variable=self.controller.intervaloSelectGenerador, value="FrameCongruencialLinealMixto", command=self.show_selected_frame)
        radioIntervalo3.grid(row=4, column=1,padx=60, pady=2)

        radioIntervalo5 = tk.Radiobutton(self, text="Productos medios", variable=self.controller.intervaloSelectGenerador, value="FrameProductosMedios", command=self.show_selected_frame)
        radioIntervalo5.grid(row=5, column=1,padx=60, pady=2)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.aceptar)
        buttonAceptar.grid(row=7, column=0,padx=60, pady=50)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPruebas"))
        buttonVolver.grid(row=7, column=1,padx=60, pady=50)

        # Contenedor para los frames
        self.frame_container = tk.Frame(self)
        self.frame_container.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # Frames a ser mostrados
        self.frames = {}
        
        for F in (FrameCongruencialLinealMixto, FrameProductosMedios):
            #mostrar_botones = False if F == FrameCongruencialLinealMixto else True
            #caller = "KS" if F == FrameCongruencialLinealMixto else None
            frame = F(parent=self.frame_container, controller=self.controller, mostrar_botones=False, framePadre="media")
            
            self.frames[F.__name__] = frame
            frame.grid(row=6, column=0, sticky="nsew")


        self.show_selected_frame()

    def show_selected_frame(self):
        self.controller.limpiarFramesHijos()
        '''Mostrar el frame seleccionado por el radio button'''
        selected = self.controller.intervaloSelectGenerador.get()

        # Ocultar todos los frames primero
        for frame in self.frames.values():
            frame.grid_remove()

        if selected == "1":
            # Mostrar el frame correspondiente a "Función random"
            # No hay necesidad de mostrar ningún frame, ya que "Función random" no tiene un frame asociado
            pass
        elif selected in self.frames:
            frame = self.frames[selected]
            frame.grid(row=6, column=0, sticky="nsew")
            frame.tkraise()

    def validaciones(self):
        mensaje=''
        mostrarMensaje=False
        cantidad = int(self.controller.cantidadGenerar.get()) if self.controller.cantidadGenerar.get() else 0
        z = self.controller.z.get().replace(",", ".")
        if(not z):
            mensaje+="Debe ingresar el valor de tabla z\n"
            mostrarMensaje=True

        if(not cantidad or cantidad<=0):
            mensaje+="Debe ingresar la cantidad a generar"
            mostrarMensaje=True

        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
            return None, None
        else:
            return cantidad,z

    def aceptar(self):
        selected = self.controller.intervaloSelectGenerador.get()
        cantidad,z=self.validaciones()
        if z:
            if selected=="1":
                sucesion=funciones.generarRandom(cantidad)
                self.controller.nrosAleatoriosGenerados=sucesion
                self.controller.aceptar("9")
            else:
                self.controller.cantidadGenerarPruebas=cantidad
                frameHijo = self.frames[selected]
                frameHijo.validaciones()

class FrameVarianza(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelChi = tk.Label(self, text="Chi cuadrada inferior (tabla)")
        labelChi.grid(row=0, column=0,padx=50, pady=10)

        entryChi = tk.Entry(self, textvariable=self.controller.chi)
        entryChi.grid(row=0, column=1,padx=50, pady=10)

        labelChi2 = tk.Label(self, text="Chi cuadrada superior (tabla)")
        labelChi2.grid(row=1, column=0,padx=50, pady=10)

        entryChi2 = tk.Entry(self, textvariable=self.controller.chi2)
        entryChi2.grid(row=1, column=1,padx=50, pady=10)

        labelCantidadGenerar = tk.Label(self, text="Cantidad de números aleatorios")
        labelCantidadGenerar.grid(row=2, column=0,padx=50, pady=10)

        entryCantidadGenerar = tk.Entry(self, textvariable=self.controller.cantidadGenerar)
        entryCantidadGenerar.grid(row=2, column=1,padx=50, pady=10)

        labelIntervalos = tk.Label(self, text="Generación de números aleatorios")
        labelIntervalos.grid(row=3, column=0, rowspan=3,padx=50, pady=2)

        radioIntervalo1 = tk.Radiobutton(self, text="Función random", variable=self.controller.intervaloSelectGenerador, value="1", command=self.show_selected_frame)
        radioIntervalo1.grid(row=3, column=1,padx=50, pady=2)

        radioIntervalo3 = tk.Radiobutton(self, text="Congruencial aditivo", variable=self.controller.intervaloSelectGenerador, value="FrameCongruencialLinealAditivo", command=self.show_selected_frame)
        radioIntervalo3.grid(row=4, column=1,padx=50, pady=2)

        radioIntervalo5 = tk.Radiobutton(self, text="Cuadrados medios", variable=self.controller.intervaloSelectGenerador, value="FrameCuadradosMedios", command=self.show_selected_frame)
        radioIntervalo5.grid(row=5, column=1,padx=50, pady=2)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.aceptar)
        buttonAceptar.grid(row=7, column=0,padx=50, pady=50)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuPruebas"))
        buttonVolver.grid(row=7, column=1,padx=50, pady=50)

        # Contenedor para los frames
        self.frame_container = tk.Frame(self)
        self.frame_container.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # Frames a ser mostrados
        self.frames = {}
        
        for F in (FrameCongruencialLinealAditivo, FrameCuadradosMedios):
            #mostrar_botones = False if F == FrameCongruencialLinealMixto else True
            #caller = "KS" if F == FrameCongruencialLinealMixto else None
            frame = F(parent=self.frame_container, controller=self.controller, mostrar_botones=False, framePadre="varianza")
            
            self.frames[F.__name__] = frame
            frame.grid(row=6, column=0, sticky="nsew")


        self.show_selected_frame()

    def show_selected_frame(self):
        self.controller.limpiarFramesHijos()
        '''Mostrar el frame seleccionado por el radio button'''
        selected = self.controller.intervaloSelectGenerador.get()

        # Ocultar todos los frames primero
        for frame in self.frames.values():
            frame.grid_remove()

        if selected == "1":
            # Mostrar el frame correspondiente a "Función random"
            # No hay necesidad de mostrar ningún frame, ya que "Función random" no tiene un frame asociado
            pass
        elif selected in self.frames:
            frame = self.frames[selected]
            frame.grid(row=6, column=0, sticky="nsew")
            frame.tkraise()

    def validaciones(self):
        mensaje=''
        mostrarMensaje=False
        cantidad = int(self.controller.cantidadGenerar.get()) if self.controller.cantidadGenerar.get() else 0
        chi = self.controller.chi.get().replace(",", ".")
        chi2=self.controller.chi2.get().replace(",", ".")
        if(not chi or not chi2):
            mensaje+="Debe ingresar los valores superior e inferior de chi\n"
            mostrarMensaje=True

        if(not cantidad or cantidad<=0):
            mensaje+="Debe ingresar la cantidad a generar"
            mostrarMensaje=True

        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
            return None, None, None
        else:
            return cantidad, chi, chi2

    def aceptar(self):
        selected = self.controller.intervaloSelectGenerador.get()
        cantidad, chi, chi2=self.validaciones()
        if chi and chi2:
            if selected=="1":
                sucesion=funciones.generarRandom(cantidad)
                self.controller.nrosAleatoriosGenerados=sucesion
                self.controller.aceptar("10")
            else:
                self.controller.cantidadGenerarPruebas=cantidad
                frameHijo = self.frames[selected]
                frameHijo.validaciones()

class FrameTransformadaInversa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        labelIntervalos = tk.Label(self, text="Intervalos")
        labelIntervalos.grid(row=1, column=0, rowspan=4,padx=50, pady=5)

        radioIntervalo1 = tk.Radiobutton(self, text="5", variable=self.controller.intervaloSelect, value="5")
        radioIntervalo1.grid(row=1, column=1, padx=50, pady=0)

        radioIntervalo2 = tk.Radiobutton(self, text="10", variable=self.controller.intervaloSelect, value="10")
        radioIntervalo2.grid(row=2, column=1, padx=50, pady=0)

        radioIntervalo3 = tk.Radiobutton(self, text="15", variable=self.controller.intervaloSelect, value="15")
        radioIntervalo3.grid(row=3, column=1, padx=50, pady=0)

        radioIntervalo4 = tk.Radiobutton(self, text="20", variable=self.controller.intervaloSelect, value="20")
        radioIntervalo4.grid(row=4, column=1, padx=50, pady=0)

        labelFA = tk.Label(self, text="Valores observados")
        labelFA.grid(row=5, column=0, padx=50, pady=0)

        entryFA = tk.Entry(self, textvariable=self.controller.secuenciaVA)
        entryFA.grid(row=5, column=1, padx=50, pady=0)

        labelAdvSec = tk.Label(self, text="Recuerde ingresar la cantidad de valores acorde a la cantidad de intervalos seleccionados\nIngrese los números separados por una coma sin espacios", 
                            fg="red",wraplength=420, justify="center")
        labelAdvSec.grid(row=6, column=0,columnspan=3, padx=0, pady=2)

        labelVA = tk.Label(self, text="Variables aleatorias")
        labelVA.grid(row=7, column=0, padx=50, pady=0)

        entryVA = tk.Entry(self, textvariable=self.controller.variablesAleatorias)
        entryVA.grid(row=7, column=1, padx=50, pady=0)

        labelAdvSec = tk.Label(self, text="Recuerde ingresar la cantidad de variables acorde a la cantidad de intervalos seleccionados\nIngrese los números separados por una coma sin espacios", 
                            fg="red",wraplength=420, justify="center")
        labelAdvSec.grid(row=8, column=0,columnspan=3, padx=0, pady=2)

        labelIntervalos = tk.Label(self, text="Generación de números aleatorios")
        labelIntervalos.grid(row=10, column=0, rowspan=3,padx=50, pady=2)

        radioIntervalo1 = tk.Radiobutton(self, text="Función random", variable=self.controller.intervaloSelectGenerador, value="1", command=self.show_selected_frame)
        radioIntervalo1.grid(row=10, column=1,padx=50, pady=2)

        radioIntervalo2 = tk.Radiobutton(self, text="Congruencial mixto", variable=self.controller.intervaloSelectGenerador, value="FrameCongruencialLinealMixto", command=self.show_selected_frame)
        radioIntervalo2.grid(row=11, column=1,padx=50, pady=2)

        labelCantidadGenerar = tk.Label(self, text="Cantidad de números aleatorios")
        labelCantidadGenerar.grid(row=9, column=0,padx=50, pady=2)

        entryCantidadGenerar = tk.Entry(self, textvariable=self.controller.cantidadGenerar)
        entryCantidadGenerar.grid(row=9, column=1,padx=50, pady=2)

        buttonAceptar = tk.Button(self, text="Aceptar",
                            command=self.aceptar)
        buttonAceptar.grid(row=13, column=0, padx=50, pady=10)

        buttonVolver = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("FrameMenuVariablesAleatorias"))
        buttonVolver.grid(row=13, column=1, padx=50, pady=10)

        # Contenedor para los frames
        self.frame_container = tk.Frame(self)
        self.frame_container.grid(row=12, column=0, columnspan=2, sticky="nsew")

        # Frames a ser mostrados
        self.frames = {}
        
        frame = FrameCongruencialLinealMixto(parent=self.frame_container, controller=self.controller, mostrar_botones=False, framePadre="VA")
        
        self.frames["FrameCongruencialLinealMixto"] = frame
        frame.grid(row=12, column=0, sticky="nsew")

        self.show_selected_frame()

    def show_selected_frame(self):
        self.controller.limpiarFramesHijos()
        selected = self.controller.intervaloSelectGenerador.get()

        # Ocultar todos los frames primero
        for frame in self.frames.values():
            frame.grid_remove()

        if selected == "1":
            # No mostrar ningún frame, ya que "Función random" no tiene uno asociado
            pass
        elif selected in self.frames:
            frame = self.frames[selected]
            frame.grid(row=12, column=0, sticky="nsew")
            frame.tkraise()

    def validaciones(self):
        mostrarMensaje=False
        mensaje=''
        valoresObservados=self.controller.secuenciaVA.get()
        variablesAleatorias=self.controller.variablesAleatorias.get()
        intervalo=self.controller.intervaloSelect.get()
        patron=re.compile(r'[^\w\s,]')
        cantidad = int(self.controller.cantidadGenerar.get()) if self.controller.cantidadGenerar.get() else 0
        if(not valoresObservados or ',' not in valoresObservados or patron.search(valoresObservados)):
            mensaje+="Los valores observados deben ser números separados por coma sin espacios\n"
            mostrarMensaje=True
        elif ',' in valoresObservados:
            valoresObservados=valoresObservados.split(",")
            if(len(valoresObservados)!=int(intervalo)):
                mensaje+="No coincide la cantidad de valores observados con el intervalo seleccionado\n"
                mostrarMensaje=True
        if not variablesAleatorias or ',' not in variablesAleatorias or patron.search(variablesAleatorias):
            mensaje+="Las variables aleatorias deben ser números separados por coma sin espacios\n"
            mostrarMensaje=True
        elif ',' in variablesAleatorias:
            variablesAleatorias=variablesAleatorias.split(",")
            if(len(variablesAleatorias)!=int(intervalo)):
                mensaje+="No coincide la cantidad de variables aleatorias con el intervalo seleccionado\n"
                mostrarMensaje=True
        if(not cantidad or cantidad<=0):
            mensaje+="Debe ingresar la cantidad a generar"
            mostrarMensaje=True

        if(mostrarMensaje):
            messagebox.showerror("Error", mensaje)
            return None, None, None
        else:
            return valoresObservados, variablesAleatorias, cantidad

    def aceptar(self):
        selected = self.controller.intervaloSelectGenerador.get()
        valoresObservados, variablesAleatorias, cantidad=self.validaciones()
        if valoresObservados and variablesAleatorias:
            if selected=="1":
                sucesion=funciones.generarRandom(cantidad)
                self.controller.nrosAleatoriosGenerados=sucesion
                self.controller.aceptar("11")
            else:
                self.controller.cantidadGenerarPruebas=cantidad
                frameHijo = self.frames[selected]
                frameHijo.validaciones()


if __name__ == "__main__":
    app = PaginaPrincipal()
    app.mainloop()