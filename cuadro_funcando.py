# -*- coding: utf8 -*-

import pygame
import sys
import random
from datetime import*
from time import gmtime, strftime
sys.path.append('../driver')
import bluePoV
try:  # Esto funciona en python 2 y 3
  from Tkinter import Tk
  from tkFileDialog import askopenfilename
except ImportError:
  from tkinter import Tk
  from  tkinter.filedialog import askopenfilename



class Cursor(pygame.Rect): #defino clase cursor
   def __init__(self):
      pygame.Rect.__init__(self,0,0,1,1)  #inicializo el cursor en la coordenada (0,0)
   def update(self):                      # con un ancho de (1,1)
      self.left,self.top=pygame.mouse.get_pos() #le paso a left y top las coordenadas del cursor


"""class Barra(pygame.sprite.Sprite):
   def __init__(self,barrita,barrita2,x=200,y=60):
      self.imagen_normal=barrita
   def update(self,pantalla):
      pantalla.blit(self.imagen_actual,self.rect)"""

class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=200,y=200):
        self.imagen_normal=imagen1
        self.imagen_seleccion=imagen2
        self.imagen_actual=self.imagen_normal
        self.rect=self.imagen_actual.get_rect()
        self.rect.left,self.rect.top=(x,y)

    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual=self.imagen_seleccion
        else: self.imagen_actual=self.imagen_normal

        pantalla.blit(self.imagen_actual,self.rect)

class BotonToggle(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=200,y=200):
        self.imagen_normal=imagen1
        self.imagen_seleccion=imagen2
        self.rect=self.imagen_normal.get_rect()
        self.rect.left,self.rect.top=(x,y)
        self.state = 0

    def toggle(self):
        self.state = 0 if self.state else 1

    def set(self):
        self.state = 1

    def unset(self):
        self.state = 0

    def update(self,pantalla,cursor):
        i = self.imagen_seleccion if self.state else self.imagen_normal
        pantalla.blit(i,self.rect)


class Barra(pygame.sprite.Sprite):

   def __init__(self,imagen1,imagen2,imagen3,imagen4,x=200,y=200):

      self.imagen_uno=imagen1
      self.imagen_dos=imagen2
      self.imagen_tres=imagen3
      self.imagen_cuatro=imagen4
      self.imagen_actual=self.imagen_uno
      self.rect=self.imagen_actual.get_rect()
      self.rect.left,self.rect.top=(x,y)

   def update(self,pantalla,cursor,x):

      if cursor.colliderect(self.rect):
         if x < 30:
            self.imagen_actual=self.imagen_uno
            ROJO = 0
         if x >=30 and x<60:
            self.imagen_actual=self.imagen_dos
            ROJO = 85
         if x >=60 and x<90:
            self.imagen_actual=self.imagen_tres
            ROJO = 168
         if x >=90:
            self.imagen_actual=self.imagen_cuatro
            ROJO = 255


      pantalla.blit(self.imagen_actual,self.rect)


def main():

   # BluePoV init & variables
   print ("Port? (default /dev/ttyUSB0)")
   port = input()
   if not port:
      port = "/dev/ttyUSB0"
   sckt = bluePoV.SerialSocket()
   sckt.connect(port,115200,timeout=0.1)
   driver = bluePoV.Driver(sckt,(480,32),depth=1)
   blueCount = 0
   bSpeed = 0x0f46#4320
   sincronizar = True
   changeSpeed = False
   delayEntreBurst8 = 2
   delayEntreBurst64 = 5
   delayEntreBurst = delayEntreBurst8

   #
   pygame.init()
   pantalla=pygame.display.set_mode([960,800]) #configuro la vetana
   pantalla.fill((112,128,144)) #defino color blaco el fondo

   GRIS2 =(100,100,100) #Declaro lista con valor del color gris
   ROJO = 0 #IDEM color rojo
   VERDE = 0#IDEM color verde
   AZUL = 0#IDEM color azul
   COLOR = (ROJO,VERDE,AZUL) #defino por defaul el color como gris
   grosor = 1 #defino variable grosor

   cursor1=Cursor()#Defino cursor

   pos = [0,0] #defino pos y pos2 como listas
   pos2 = [0,0]
   distx = 250
   disty = 400
   disty2 = 450
   disty3 = 500
   #rojo1=pygame.image.load("rojo.png")
   #rojo2=pygame.image.load("rojo2.png")
   #azul1=pygame.image.load("azul.png")
   #azul2=pygame.image.load("azul2.png")
   barra=pygame.image.load("zaza.png")
   barra2=pygame.image.load("zaza2.png")
   barra3=pygame.image.load("zaza4.png")
   barra4=pygame.image.load("zaza5.png")
   barrav=pygame.image.load("sasa.png")
   barrav2=pygame.image.load("sasa2.png")
   barrav3=pygame.image.load("sasa3.png")
   barrav4=pygame.image.load("sasa4.png")
   barrar=pygame.image.load("eaea.png")
   barrar2=pygame.image.load("eaea2.png")
   barrar3=pygame.image.load("eaea3.png")
   barrar4=pygame.image.load("eaea4.png")
   boton1=pygame.image.load("borrar.png")
   boton2=pygame.image.load("borrar2.png")
   boton3=pygame.image.load("imag.png")
   boton4=pygame.image.load("imag2.png")
   boton5=pygame.image.load("hora.png")
   boton6=pygame.image.load("hora2.png")
   boton7=pygame.image.load("msj.png")
   boton8=pygame.image.load("msj2.png")
   boton9=pygame.image.load("dimm.png")
   boton10=pygame.image.load("dimm2.png")
   boton11=pygame.image.load("colores8.png")
   boton12=pygame.image.load("colores64.png")
   bot1=Boton(boton1,boton2,500,400)
   bot2=Boton(boton3,boton4,500,430)
   bot3=Boton(boton5,boton6,500,460)
   bot4=Boton(boton7,boton8,500,490)
   bot5=BotonToggle(boton9,boton10,500,520)
   bot6=BotonToggle(boton11,boton12,500,550)
   bar1=Barra(barra,barra2,barra3,barra4,distx,disty)
   bar2=Barra(barrav,barrav2,barrav3,barrav4,distx,disty2)
   bar3=Barra(barrar,barrar2,barrar3,barrar4,distx,disty3)

   #boton1=Boton(rojo1,rojo2,50,100)
   #boton2=Boton(azul1,azul2,200,100)

   estabaApretando = False
   s1 = pygame.Surface((240,32)) #defino la superficie sobre la que voy a dibujar
   s2 = pygame.Surface((40,40))
   s9000 = pygame.Surface((480,32))
   posicionS1 = (0,200)  #Digo donde imprimo la superficie
   posicionS2 = (400,435)
   s1.fill((0,0,0)) #Defino el color de la superficie
   s2.fill(COLOR)
   #s1 = pygame.transform.scale2x(s1) #agrando el doble la superficie 1
   #s1 = pygame.transform.scale2x(s1)

   #fondo = pygame.image.load("fondo.jpg").convert() #Defino como fondo la imagen fondo que se encuentra en la misma carpeta
   #pantalla.blit(fondo, (0, 0)) #imprimo el fondo en la pantalla

   pygame.display.set_caption("Interfaz usuario - Grupo 5")#Nombre de la ventana
   reloj=pygame.time.Clock() #declaro un clock
   fuente=pygame.font.Font(None,40)#defino tipo de fuente
   fuente2=pygame.font.Font(None,100)
   pygame.display.update() #actualizo display
   salir=False
   pantalla.blit(s1,posicionS1)#imprimo superficie
   pantalla.blit(s2,posicionS2)
   pygame.display.flip()#actualizo ventana
   cambioColor = False
   barrainit = False
   botonloco = False
   posbar = 0
   posbar2 = 0
   posbar3 = 0

   hayimagen = False
   hora = False


   ttt = 0
   while salir!=True:  #Loop principal, como el for infinito
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #para que se cierre la ventana con la cruz
                     salir=True

                elif event.type==pygame.KEYDOWN: # si se presiona una tecla

                    if event.key==pygame.K_0:# Si es el 0 defino el color gris para dibujar
                       COLOR = GRIS2
                       cambioColor = True

                    elif event.key==pygame.K_1:#Si es el 1 es el rojo
                       COLOR = (255,0,0)
                       cambioColor = True

                    elif event.key==pygame.K_2:#Si es el 2 es el verde
                       COLOR = (0,255,0)
                       cambioColor = True

                    elif event.key==pygame.K_3:#Si es el 3 es el azul
                        COLOR = (0,0,255)
                        cambioColor = True

                    elif event.key==pygame.K_4:#Si es el 4 es el random
                        r = int(random.random() * 255)
                        g = int(random.random() * 255)
                        b = int(random.random() * 255)
                        COLOR = (r,g,b)
                        cambioColor = True

                    elif event.key==pygame.K_KP_PLUS:
                          grosor = grosor +1

                    elif event.key==pygame.K_KP_MINUS:
                       if grosor > 1:
                          grosor = grosor - 1

                    elif event.key==pygame.K_ESCAPE:
                          salir = True

                    elif event.key==pygame.K_UP:
                          bSpeed += 1
                          #changeSpeed = True
                          driver.setSpeed(bSpeed)
                          print('s: '+str(bSpeed))

                    elif event.key==pygame.K_DOWN:
                          bSpeed -= 1
                          #changeSpeed = True
                          driver.setSpeed(bSpeed)
                          print('s: '+str(bSpeed))

                    elif event.key==pygame.K_RIGHT:
                          bSpeed -= 10
                          #changeSpeed = True
                          driver.setSpeed(bSpeed)
                          print('s: '+str(bSpeed))

                    elif event.key==pygame.K_LEFT:
                          bSpeed += 10
                          #changeSpeed = True
                          driver.setSpeed(bSpeed)
                          print('s: '+str(bSpeed))

                    elif event.key==pygame.K_p:
                          sincronizar = True # synchro

                elif event.type==pygame.MOUSEBUTTONUP:
                         if event.button == 8:
                            ttt = 0

                elif event.type==pygame.MOUSEBUTTONDOWN:
                         if event.button == 8:
                            ttt = 1
                         if cursor1.colliderect(bar1.rect):
                           pos5 = pygame.mouse.get_pos()
                           pos6= pos5[0] - distx
                           posbar = pos6
                           bar1.update(pantalla,cursor1,pos6)
                           if pos6 < 30:
                              ROJO = 0
                           if pos6 >=30 and pos6 < 60:
                              ROJO = 85
                           if pos6 >=60 and pos6 < 90:
                              ROJO = 168
                           if pos6 >= 90:
                              ROJO = 255
                           COLOR = (ROJO,VERDE,AZUL)
                         if cursor1.colliderect(bar2.rect):
                           pos7 = pygame.mouse.get_pos()
                           pos8 = pos7[0] - distx
                           posbar2 = pos8
                           bar2.update(pantalla,cursor1,pos8)
                           if pos8 < 30:
                              VERDE = 0
                           if pos8 >=30 and pos8 < 60:
                              VERDE = 85
                           if pos8 >=60 and pos8 < 90:
                              VERDE = 168
                           if pos8 >= 90:
                              VERDE = 255
                           COLOR = (ROJO,VERDE,AZUL)
                         if cursor1.colliderect(bar3.rect):
                           pos9 = pygame.mouse.get_pos()
                           pos10 = pos9[0] - distx
                           posbar3 = pos10
                           bar3.update(pantalla,cursor1,pos10)
                           if pos10 < 30:
                              AZUL = 0
                           if pos10 >=30 and pos10 < 60:
                              AZUL = 85
                           if pos10 >=60 and pos10 < 90:
                              AZUL = 168
                           if pos10 >= 90:
                              AZUL = 255
                           COLOR = (ROJO,VERDE,AZUL)
                         if cursor1.colliderect(bot1.rect):
                            hora = False
                            s1.fill((0,0,0))
                         if cursor1.colliderect(bot2.rect):
                            s1.fill((0,0,0))
                            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                            filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
                            try:
                              bla = pygame.image.load(filename)
                              jeje = pygame.transform.scale(bla,(240,32))
                              s1.blit(jeje,(0,0))
                              hora = False
                            except:
                              pass
                         if cursor1.colliderect(bot3.rect):
                            s1.fill((0,0,0))
                            hora = True
                         if cursor1.colliderect(bot4.rect):
                            s1.fill((0,0,0))
                            texto2=fuente.render("EXPO PIO 2013",0,(200,150,150))
                            s1.blit(texto2,(10,5))
                            hora = False
                         if cursor1.colliderect(bot5.rect):
                            bot6.unset()
                            bot5.toggle()
                            driver.setDimm(bot5.state)
                         if cursor1.colliderect(bot6.rect):
                            bot5.unset()
                            bot6.toggle()
                            driver.setDepth(bot6.state+1)
                            delayEntreBurst = delayEntreBurst64 if bot6.state else delayEntreBurst8


            clockSpeed = 50
            reloj.tick(clockSpeed) #frecuencia del reloj

            #cadena = strftime("%H:%M:%S", gmtime())#Mostrar tiempo más facil
            #texto=fuente.render(cadena,0,(200,150,150))

            now=datetime.now() #/Forma de mostrar hora almacenando en variables
            H= now.hour   #/guardo horas en variable H
            M= now.minute #/guardo minutos en variable M
            S= now.second #/guardo segundos en variable S
            cadena2= str(H) #/paso horas a string
            dospuntos = ":" #/guardo : en string
            cadena3= str(M) #/paso minutos a string
            cadena4= str(S) #/paso segundos a string
            if hora == True:
               s1.fill((0,0,0))
               s1.blit(texto3,(55,5))

            if M<10:
               if S< 10:
                  texto3=fuente.render(cadena2+":0"+cadena3+":0"+cadena4,0,(200,150,150))
               else:
                  texto3=fuente.render(cadena2+":0"+cadena3+":"+cadena4,0,(200,150,150))
            else:
               if S< 10:
                  texto3=fuente.render(cadena2+":"+cadena3+":0"+cadena4,0,(200,150,150))
               else:
                  texto3=fuente.render(cadena2+":"+cadena3+":"+cadena4,0,(200,150,150))

            texto=fuente2.render("BluePov",0,(72,118,255))
            texto2=fuente.render("EXPO PIO 2013",0,(200,150,150))

            pantalla.fill((112,128,144))# Para que actualioze tiempo sin que se sobreponga
            pantalla.blit(texto,(365,60))# Imprimo el tiempo en pantalla
            cursor1.update() #Actualizo el cursor q es una pequeña superficie
            #boton1.update(pantalla,cursor1)#modifico el boton si el cursor esta sobre este
            #boton2.update(pantalla, cursor1)#lo mismo
            bar1.update(pantalla,cursor1,posbar)
            bar2.update(pantalla,cursor1,posbar2)
            bar3.update(pantalla,cursor1,posbar3)
            bot1.update(pantalla,cursor1)
            bot2.update(pantalla, cursor1)
            bot3.update(pantalla,cursor1)
            bot4.update(pantalla,cursor1)
            bot5.update(pantalla,cursor1)
            bot6.update(pantalla,cursor1)

            if pygame.mouse.get_pressed()[0] or ttt: #veo si se presiono el click izquierdo del mouse
                if not estabaApretando: #Si no se estaba apretando

                    estabaApretando = True  #Ahora se esta apretando
                    pos3 = pygame.mouse.get_pos()#guardo posicion del cursor en pos 3
                    pos[0] = (pos3[0] - posicionS1[0])/4#guardo cada posicion de la lista pos3 en cada una de pos
                    pos[1] = (pos3[1] - posicionS1[1])/4#le resto posicion s1 ya que las coordenadas estan en funcion de la ventana y no de s1
                    g = int(grosor/2.15)
                    pygame.draw.circle(s1, COLOR, (int(pos[0]),int(pos[1])),int(g))#Dibujo linea entre posicion en la que aprete y posicion actual del cursor


                else:   #si se estaba apretando
                    pos3 = pygame.mouse.get_pos() #Mismo que antes
                    pos2[0] = (pos3[0] - posicionS1[0])/4#Lo mismo pero con pos2
                    pos2[1] = (pos3[1] - posicionS1[1])/4#obtengo la posicion actual
                    pygame.draw.line(s1, COLOR, (int(pos[0]),int(pos[1])), (int(pos2[0]),int(pos2[1])),grosor)#Dibujo linea entre posicion en la que aprete y posicion actual del cursor
                    pygame.draw.circle(s1, COLOR, (int(pos2[0]),int(pos2[1])),int(grosor/2.15))#Dibujo un circulo donde esta el cursor

                    if cambioColor == True:
                       pygame.draw.circle(s1, COLOR, (int(pos[0]),int(pos[1])),int(grosor/2.15))#Dibujo un circulo donde estaba el cursor

                    pos = list(pos2) #Guardo la posicion actual en posicion anterior
            else:
               estabaApretando = False #digo que no se estaba apretando antes
            if pygame.mouse.get_pressed()[2]: #Si apreto click derecho se limpia la pantalla
               s1.fill((0,0,0))#Se vuelve a llenar el fondo de s1
               hora = False
            cambioColor = False
            s2.fill(COLOR)
            pantalla.blit(s2,posicionS2)
            pantalla.blit(pygame.transform.scale2x(pygame.transform.scale2x(s1)),posicionS1) #imprimo en la ventana s1 con lo dibujado
            pygame.display.update()# actualizo ventana

            if not blueCount:
                if sincronizar:
                  driver.syncro()
                  sincronizar = False
                if changeSpeed:
                  driver.setSpeed(bSpeed)
                  changeSpeed = False
                s9000.blit(s1,(0,0))
                driver.pgBlit(s9000)
                blueCount = int(delayEntreBurst * clockSpeed)
            blueCount -= 1


   pygame.quit()

main()
