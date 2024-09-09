import numpy as np
import os
 
 ##presentado por yeferson gomez muñoz y jaden otalvaro giraldo
 
def limpiar_consola():
    # Limpiar consola para diferentes sistemas operativos
    if os.name == 'nt':  # Para Windows
        os.system('cls')

def seleccionar_nueva_opcion():
    input("Presione Enter para seleccionar otra opción...")
    limpiar_consola()   
    
def agregar_proceso(procesos):
    print("Agregue su proceso \n")
    nombre = input("Nombre del proceso: ")
    rafaga = int(input("Ráfaga: "))
    t_llegada = int(input("Tiempo de llegada: "))

    proceso = [nombre, rafaga, t_llegada]

    if len(procesos) == 0:
        return np.array([proceso])
    else:
        return np.vstack((procesos, proceso))


def calcular_fifo(Matriz_de_procesos):
    sumatoria_de_procesos=0
    for i in range(Matriz_de_procesos.shape[0]):
        sumatoria_de_procesos=sumatoria_de_procesos+int(Matriz_de_procesos[i][1])
        
    #crear diagrama con matriz de ceros
    tamaño_filas_diagrama=int(Matriz_de_procesos.shape[0])+1
    tamaño_columnas_diagrama=sumatoria_de_procesos+10
    diagrama = np.zeros((tamaño_filas_diagrama, tamaño_columnas_diagrama), dtype=object)
    
    #ordenar nombres de procesos por tiempo de salida de menor a mayor en elje y de arriba hacia abajo

    lista_de_llegada=[]
    lista_menor_a_mayor_llegada=[]
    lista_menor_a_mayor_llegada_nombre=[]
    lista_menor_a_mayor_llegada_rafaga=[]
    lista_de_tiempos_de_no_ejecucion=[]
    
    for i in range(Matriz_de_procesos.shape[0]):
        lista_de_llegada.append(float(Matriz_de_procesos[i][2]))
    lista_menor_a_mayor_llegada=sorted(lista_de_llegada)
    
    for i in range(int(len(lista_menor_a_mayor_llegada))):
        for posicion in range(int(Matriz_de_procesos.shape[0])):
            #usando el menor tiempo de llegada se ordena en una lista el nombre de los procesos segun tiempo de llegada
            if(float(lista_menor_a_mayor_llegada[i])==float(Matriz_de_procesos[posicion][2])):
                lista_menor_a_mayor_llegada_nombre.append(str(Matriz_de_procesos[posicion][0]))
                #crear lista de rafaga segun orden de llegada
                lista_menor_a_mayor_llegada_rafaga.append(int(Matriz_de_procesos[posicion][1]))
                
    for i in range(int(len(lista_menor_a_mayor_llegada_nombre))):
        diagrama[i][0]=str(lista_menor_a_mayor_llegada_nombre[i])
        
    #ordenar tiempo en el eje x
    for i in range(int(sumatoria_de_procesos)+10):
        diagrama[int(Matriz_de_procesos.shape[0])][i]=i  
        
    #asignar procesos al diagrama
    
    tiempo_de_no_ejecucion=0
    sum_tiempo_de_ejecucion_procesos_anteriores=0
    for i in range(len(lista_menor_a_mayor_llegada)):
        t_de_llegada=int(lista_menor_a_mayor_llegada[i])###lista de tiempos de llegada
        if(sum_tiempo_de_ejecucion_procesos_anteriores>=t_de_llegada):
            tiempo_de_no_ejecucion=sum_tiempo_de_ejecucion_procesos_anteriores
        else:
            tiempo_de_no_ejecucion=t_de_llegada
        #asignar los tiempos de no ejecucion a una lista
        lista_de_tiempos_de_no_ejecucion.append(tiempo_de_no_ejecucion)
        
            
        for cont in range(int(lista_menor_a_mayor_llegada_rafaga[i])):      
            diagrama[i][tiempo_de_no_ejecucion+1]=1
            tiempo_de_no_ejecucion=tiempo_de_no_ejecucion+1
            sum_tiempo_de_ejecucion_procesos_anteriores=tiempo_de_no_ejecucion

            
 
        
    
    
    #imprimir diagrama
    
    for fila in diagrama:
        print(" ".join(f"{str(elem):>2}" for elem in fila))
        
    #tiempo de espera 
    lista_tiempo_espera=[] 
    print("              ")
    print("tiempo de espera")  
    for cont in range(len(lista_de_tiempos_de_no_ejecucion)):
        tiempo_espera=int(lista_de_tiempos_de_no_ejecucion[cont])-float(lista_menor_a_mayor_llegada[cont])
        print(str(lista_menor_a_mayor_llegada_nombre[cont])+':'+str(tiempo_espera) )
        
        lista_tiempo_espera.append(tiempo_espera)
    
    #tiempo de sistema
    sumatoria_t_sistema=0
    promedio_t_sistema=0
    print("              ")
    print("tiempo de sistema") 
    
    for cont in range(len(lista_tiempo_espera)):
        tiempo_sistema=lista_tiempo_espera[cont]+lista_menor_a_mayor_llegada_rafaga[cont]
        print(str(lista_menor_a_mayor_llegada_nombre[cont])+':'+ str(tiempo_sistema))
        sumatoria_t_sistema=sumatoria_t_sistema+tiempo_sistema
        
    print("              ")
    
    promedio_t_sistema=sumatoria_t_sistema/(len(lista_menor_a_mayor_llegada_nombre))
    print(str("promedio tiempo de sistema") + ':' +str(promedio_t_sistema))

 
def agregar_ranking_matriz_procesos(ranking,tiempo_transcurrido,Matriz_de_procesos,matriz_de_procesos_copia,lista_prioridades_validas):
    lista_menor_mayor_raf_valid = sorted(lista_prioridades_validas)
    rafaga_menor=lista_menor_mayor_raf_valid[0]
    
    #asignar ranking a la matriz de procesos
    cont=0
    while ((int(Matriz_de_procesos[cont][1])) != (rafaga_menor)):
        cont= cont+1
    Matriz_de_procesos[cont][4]=ranking
    Matriz_de_procesos[cont][5]=1
    ranking=ranking+1
    tiempo_transcurrido=tiempo_transcurrido+int(Matriz_de_procesos[cont][1])
    
    
    #borrar proceso de matriz copia donde ya se asigno ranking
    matriz_de_procesos_copia = np.empty((0, 6))
    matriz_filtrada=eliminar_filas_con_uno(Matriz_de_procesos)
    matriz_de_procesos_copia=np.vstack(( matriz_de_procesos_copia, matriz_filtrada))
    return ranking,tiempo_transcurrido,Matriz_de_procesos,matriz_de_procesos_copia        
 
 
def eliminar_filas_con_uno(matriz):
    # Filtrar las filas donde el valor en la quinta columna no es 1
    matriz_filtrada = matriz[matriz[:, 5] != 1]
    return matriz_filtrada
 
    
    
def calcular_sjf(Matriz_de_procesos):
    sumatoria_de_procesos=0
    for i in range(Matriz_de_procesos.shape[0]):
        sumatoria_de_procesos=sumatoria_de_procesos+int(Matriz_de_procesos[i][1])
        
    #crear diagrama con matriz de ceros
    tamaño_filas_diagrama=int(Matriz_de_procesos.shape[0])+1
    tamaño_columnas_diagrama=sumatoria_de_procesos+10
    diagrama = np.zeros((tamaño_filas_diagrama, tamaño_columnas_diagrama), dtype=object)  
    
    
    #ordenar nombres de procesos por tamaño de rafaga de menor a mayor en eje y de arriba hacia abajo

    
            # Crear una nueva columna para orden de dibujado de cada proceso
    nueva_columna = np.zeros((Matriz_de_procesos.shape[0], 1))

            # Agregar la nueva columna de ceros a la matriz original
    Matriz_de_procesos = np.hstack((Matriz_de_procesos, nueva_columna))
    # Crear una nueva columna para estados de bloqueo y el agoritmo no lo tome en cuenta para ranking -->0.disponible y 1-bloqueo
    nueva_columna2 = np.zeros((Matriz_de_procesos.shape[0], 1))
    Matriz_de_procesos = np.hstack((Matriz_de_procesos, nueva_columna2))
            #obtener matriz con el orden de dibujado
    matriz_de_procesos_copia=np.empty((0, 6))
    matriz_de_procesos_copia=np.vstack(( matriz_de_procesos_copia, Matriz_de_procesos))
    
    tiempo_transcurrido=0
    ranking=1
    cont_aux=0
    while (cont_aux<matriz_de_procesos_copia.shape[0]):
        lista_prioridades_validas=[]
        for cont in range (matriz_de_procesos_copia.shape[0]):
            if (int((matriz_de_procesos_copia[cont][2]))<=tiempo_transcurrido):
                lista_prioridades_validas.append(int(matriz_de_procesos_copia[cont][1]))
            [ranking,tiempo_transcurrido,Matriz_de_procesos,matriz_de_procesos_copia]=agregar_ranking_matriz_procesos(ranking,tiempo_transcurrido,Matriz_de_procesos,matriz_de_procesos_copia,lista_prioridades_validas)
        cont_aux=cont_aux+1
    
     
    lista_valor_dibujado=[]
    lista_dibujado_ordenados=[]
    lista_orden_aux=[] 
    for i in range(Matriz_de_procesos.shape[0]):
        lista_valor_dibujado.append(Matriz_de_procesos[i][4])
        
    lista_orden_aux=sorted(lista_valor_dibujado)
    
    lista_orden_aux.append(lista_orden_aux.pop(0))
    lista_dibujado_ordenados=lista_orden_aux
    
    
    lista_nombres_ordenados=[]
    lista_rafagas_ordenadas=[]
    lista_tllegada_ordenadas=[]
    for i in range(int(len(lista_dibujado_ordenados))):
        for posicion in range(int(Matriz_de_procesos.shape[0])):
            #usando el menor tiempo de llegada se ordena en una lista el nombre de los procesos segun tiempo de llegada
            if(float(lista_dibujado_ordenados[i])==float(Matriz_de_procesos[posicion][4])):
                lista_nombres_ordenados.append(str(Matriz_de_procesos[posicion][0]))
                #crear lista de rafaga segun orden de llegada
                lista_rafagas_ordenadas.append(int(Matriz_de_procesos[posicion][1]))
                #lista tiempo de llegada
                lista_tllegada_ordenadas.append(int(Matriz_de_procesos[posicion][2]))
                
    
    #poner nombres eje x           
    for i in range(int(len(lista_nombres_ordenados))):
        diagrama[i][0]=str(lista_nombres_ordenados[i])
        
    #ordenar tiempo en el eje x
    for i in range(int(sumatoria_de_procesos)+10):
        diagrama[int(Matriz_de_procesos.shape[0])][i]=i 
        
    #asignar procesos al diagrama
    lista_de_tiempos_de_no_ejecucion=[]
    tiempo_de_no_ejecucion=0
    sum_tiempo_de_ejecucion_procesos_anteriores=0
    for i in range(len(lista_rafagas_ordenadas)):
        t_de_llegada=int(lista_tllegada_ordenadas[i])###lista de tiempos de llegada
        if(sum_tiempo_de_ejecucion_procesos_anteriores>=t_de_llegada):
            tiempo_de_no_ejecucion=sum_tiempo_de_ejecucion_procesos_anteriores
        else:
            tiempo_de_no_ejecucion=t_de_llegada
        #asignar los tiempos de no ejecucion a una lista
        lista_de_tiempos_de_no_ejecucion.append(tiempo_de_no_ejecucion)
        
            
        for cont in range(int(lista_rafagas_ordenadas[i])):      
            diagrama[i][tiempo_de_no_ejecucion+1]=1
            tiempo_de_no_ejecucion=tiempo_de_no_ejecucion+1
            sum_tiempo_de_ejecucion_procesos_anteriores=tiempo_de_no_ejecucion  
         
        
         
    #imprimir diagrama   
    for fila in diagrama:
        print(" ".join(f"{str(elem):>2}" for elem in fila))
        
    #tiempo de espera 
    lista_tiempo_espera=[] 
    print("              ")
    print("tiempo de espera")  
    for cont in range(len(lista_de_tiempos_de_no_ejecucion)):
        tiempo_espera=int(lista_de_tiempos_de_no_ejecucion[cont])-float(lista_tllegada_ordenadas[cont])
        print(str(lista_nombres_ordenados[cont])+':'+str(tiempo_espera) )
        
        lista_tiempo_espera.append(tiempo_espera)
    
    #tiempo de sistema
    sumatoria_t_sistema=0
    promedio_t_sistema=0
    print("              ")
    print("tiempo de sistema") 
    
    for cont in range(len(lista_tiempo_espera)):
        tiempo_sistema=lista_tiempo_espera[cont]+lista_rafagas_ordenadas[cont]
        print(str(lista_nombres_ordenados[cont])+':'+ str(tiempo_sistema))
        sumatoria_t_sistema=sumatoria_t_sistema+tiempo_sistema
        
    print("              ")
    
    promedio_t_sistema=sumatoria_t_sistema/(len(lista_nombres_ordenados))
    print(str("promedio tiempo de sistema") + ':' +str(promedio_t_sistema))


class Proceso:
    def __init__(self, nombre, tiempo_rafaga, tiempo_llegada, prioridad):
        self.nombre = nombre
        self.tiempo_rafaga = int(tiempo_rafaga)
        self.tiempo_llegada = int(tiempo_llegada)
        self.prioridad = int(prioridad)

    def __lt__(self, other):
        if self.prioridad != other.prioridad:
            return self.prioridad < other.prioridad
        else:
            return self.tiempo_llegada < other.tiempo_llegada

def ordenar_por_prioridad(matriz_procesos):
    sumatoria_de_procesos=0
    for i in range(Matriz_de_procesos.shape[0]):
        sumatoria_de_procesos=sumatoria_de_procesos+int(Matriz_de_procesos[i][1])
        
    #crear diagrama con matriz de ceros
    tamaño_filas_diagrama=int(Matriz_de_procesos.shape[0])+1
    tamaño_columnas_diagrama=sumatoria_de_procesos+10
    diagrama = np.zeros((tamaño_filas_diagrama, tamaño_columnas_diagrama), dtype=object) 
    
    procesos = []
    for fila in matriz_procesos:
        proceso = Proceso(fila[0], fila[1], fila[2], fila[3])
        procesos.append(proceso)

    procesos.sort()

    lista_nombres_ordenados=[proceso.nombre for proceso in procesos] 
    
    
    """---------------------------"""
    
    
    lista_rafagas_ordenadas=[]
    lista_tllegada_ordenadas=[]
    for i in range(int(len(lista_nombres_ordenados))):
        for posicion in range(int(Matriz_de_procesos.shape[0])):
            #crear lista de rafagas y tiempos de llegada por orden de prioridad
            if(str(lista_nombres_ordenados[i])==str(Matriz_de_procesos[posicion][0])):
                #crear lista de rafaga segun orden de llegada
                lista_rafagas_ordenadas.append(int(Matriz_de_procesos[posicion][1]))
                #lista tiempo de llegada
                lista_tllegada_ordenadas.append((Matriz_de_procesos[posicion][2]))
                
    
    #poner nombres eje x           
    for i in range(int(len(lista_nombres_ordenados))):
        diagrama[i][0]=str(lista_nombres_ordenados[i])
        
    #ordenar tiempo en el eje x
    for i in range(int(sumatoria_de_procesos)+10):
        diagrama[int(Matriz_de_procesos.shape[0])][i]=i 
        
    #asignar procesos al diagrama
    lista_de_tiempos_de_no_ejecucion=[]
    tiempo_de_no_ejecucion=0
    sum_tiempo_de_ejecucion_procesos_anteriores=0
    for i in range(len(lista_rafagas_ordenadas)):
        t_de_llegada=int(lista_tllegada_ordenadas[i])###lista de tiempos de llegada
        if(sum_tiempo_de_ejecucion_procesos_anteriores>=t_de_llegada):
            tiempo_de_no_ejecucion=sum_tiempo_de_ejecucion_procesos_anteriores
        else:
            tiempo_de_no_ejecucion=t_de_llegada
        #asignar los tiempos de no ejecucion a una lista
        lista_de_tiempos_de_no_ejecucion.append(tiempo_de_no_ejecucion)
        
            
        for cont in range(int(lista_rafagas_ordenadas[i])):      
            diagrama[i][tiempo_de_no_ejecucion+1]=1
            tiempo_de_no_ejecucion=tiempo_de_no_ejecucion+1
            sum_tiempo_de_ejecucion_procesos_anteriores=tiempo_de_no_ejecucion  
         
        
         
    #imprimir diagrama   
    for fila in diagrama:
        print(" ".join(f"{str(elem):>2}" for elem in fila))
        
    #tiempo de espera 
    lista_tiempo_espera=[] 
    print("              ")
    print("tiempo de espera")  
    for cont in range(len(lista_de_tiempos_de_no_ejecucion)):
        tiempo_espera=int(lista_de_tiempos_de_no_ejecucion[cont])-float(lista_tllegada_ordenadas[cont])
        print(str(lista_nombres_ordenados[cont])+':'+str(tiempo_espera))
        
        lista_tiempo_espera.append(tiempo_espera)
    
    #tiempo de sistema
    sumatoria_t_sistema=0
    promedio_t_sistema=0
    print("              ")
    print("tiempo de sistema") 
    
    for cont in range(len(lista_tiempo_espera)):
        tiempo_sistema=lista_tiempo_espera[cont]+lista_rafagas_ordenadas[cont]
        print(str(lista_nombres_ordenados[cont])+':'+ str(tiempo_sistema))
        sumatoria_t_sistema=sumatoria_t_sistema+tiempo_sistema
        
    print("              ")
    
    promedio_t_sistema=sumatoria_t_sistema/(len(lista_nombres_ordenados))
    print(str("promedio tiempo de sistema") + ':' +str(promedio_t_sistema))
    



"-------------------------------------------------main--------------------------------------------------"
# Variables
opcion = 0
Matriz_de_procesos = np.array([["a", "4", "0", "1"], ["b", "2", "2", "1"], ["c", "6", "3", "2"], ["d", "1", "5", "3"]
                     ])

while  opcion != 7:
    print("---------------MENU----------------------")
    print("1- Agregar proceso")
    print("2- Ver procesos")
    print("3- Calcular por FIFO")
    print("4- calcular sjf")
    print("5- calcular prioridad")
    print("6- Terminar")

    opcion = int(input('Elija una opción: '))

    if opcion == 1:
        Matriz_de_procesos = agregar_proceso(Matriz_de_procesos)
        seleccionar_nueva_opcion()

    elif opcion == 2:
       print(Matriz_de_procesos) 
       seleccionar_nueva_opcion()

    elif opcion == 3:
      calcular_fifo(Matriz_de_procesos)
      seleccionar_nueva_opcion()

    elif opcion == 4:
       calcular_sjf(Matriz_de_procesos)
       seleccionar_nueva_opcion()
    elif opcion == 5:
       pocesos=ordenar_por_prioridad(Matriz_de_procesos)
       print(pocesos)
       seleccionar_nueva_opcion()

    elif opcion == 6:
        break