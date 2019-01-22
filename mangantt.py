#! /usr/bin/env python
#-*- coding: UTF-8 -*-

'''Estructura de clases del sistema de gestion de diagramas de Gantt'''

# def init(Nombre):
#     '''Inicializa un proyecto'''
#     return Elemento(Nombre, 'proyecto')

class Elemento(object):
    """Elementos basicos de un diagrama de Gantt"""
    __id_actual = 1  #  Comienzo por 1. El id 0 va a ser siempre asignado al proyecto
    __elems = {}

    @staticmethod
    def get_id():
        '''Devuelve un número de identificador disponible'''
        res = Elemento.__id_actual
        Elemento.__id_actual =+ 1

        return res

    @staticmethod
    def get_elem(id):
        '''Devuelve el elemento indicado según su id'''
        return Elemento.__elems[id]

    @staticmethod
    def get_proyecto():
        '''Devuelve el proyecto. Es equivalente a hacer get_elem(0)'''
        return Elemento.__elems[0]

    def __init__(self, nombre, tipo):
        
        self.__nombre = nombre
        self.__id = Elemento.get_id()  # Identificador del elemento
        self.__tipo_elem = tipo  # Tipo de elemento ('hito', 'tarea', 'grupo', 'proyecto')
        self.__padre = None

        # Agrego el objeto creado al diccionario de elementos, con el id como clave
        Elemento.__elems[self.id] = self

    @property
    def nombre(self):
        '''Nombre del elemento.'''
        return self.__nombre
    
    
    @nombre.setter
    def nombre(self, val):
        self.__nombre = val
    
    @property
    def id(self):
        '''Identificador unico del elemento. Solo lectura.'''
        return self.__id

    @property
    def tipo_elem(self):
        '''Tipo de elemento (hito, tarea, grupo). Solo lectura.'''
        return self.__tipo_elem
    
    @property
    def padre(self):
        """Padre del elemento. Si el elemento no tiene padre, entonces vale None. Solo lectura."""
        return self.__padre
    
        

class Hito(Elemento):
    """Hito de un proyecto. Representa instantes de tiempo en un proyecto o tarea. Cuando no se especifica el tipo de hito
    se crea un hito de tiempo por defecto."""
    

    def __init__(self, nombre, valor, subtipo, id_padre=0):  #  Los valores para el tipo pueden ser 'tiempo' o 'progreso'
        super(Hito, self).__init__(nombre, 'hito')
        
        self.__ocurrido = False
        self.__valor = valor
        self.__subtipo = subtipo
        self._Hito__padre = padre
        self.__momento = None

    @property
    def ocurrido(self):
        '''Estado del hito. Si el hito ya ha ocurrido devuelve True, de lo contrario devuelve False. Solo lectura.'''
        return self.__ocurrido
    
    
    @property
    def momento(self):
        """Momento en que ocurre el hito. Si el tipo de hito es 'progreso', entonces momento es igual a None hasta 
        que el hito se produzca, donde adquiere como valor el tiempo global en el que se produce. Si el tipo de hito
        es 'tiempo' entonces momento es igual al valor establecido, se haya producido o no. Solo lectura"""
        return self.__momento

    
    @property
    def subtipo(self):
        """Establece un tipo de hito. En las clases derivadas Hito_tmpo e Hito_prog ésta propiedad adquiere los valores
        'tiempo' y 'progreso' respectivamente. Se puede establecer un nuevo tipo de hito si se extiende la clase Hito y
        se asigna el tipo en ésta propiedad"""

        # """Tipo de hito. Los valores que puede adquirir esta propiedad son 'tiempo' y 'progreso', siendo el hito
        # de tiempo el valor por defecto. Si es un hito de tiempo su estado de ocurrencia pasara a True cuando el
        # tiempo global del proyecto sea mayor que el establecido como valor del hito. En caso de que sea de progreso
        # se debe establecer una tarea o grupo y su estado de ocurrencia será True cuando el progreso de dicha tarea
        # o grupo sea mayor al establecido como valor del hito. Solo lectura."""
        return self.__subtipo
    

    @property
    def valor(self):
        '''Valor que definira cuando se produce un hito. Lo que representa éste valor depende del tipo de hito que sea.
        Si es de tiempo, valor será el momento de ocurrencia del hito, y si es de progreso será el porcentaje de progreso
        del padre que se debe comparar para establecer el momento de ocurrencia.'''
        return self.__valor
    
    @valor.setter
    def valor(self, val):
        self.__valor = val
    

    def actualizar(self):
        '''Analiza el estado del hito para saber si se ha producido o no. Este método debe extenderse cuando se deriven 
        clases a partir de la clase Hito.'''
        pass


class Hito_tmpo(Hito):
    """Hito de tiempo. Define un momento específico del proyecto. El padre puede ser un grupo o tarea o no tener un padre
    explícito, sin embargo el momento siempre está definido respecto del proyecto. Si no tiene asignado un padre
    explícitamente se asume como padre el proyecto mismo."""

    def __init__(self, nombre, valor, id_padre=0):
        super(Hito_tmpo, self).__init__(nombre, valor, 'tiempo', id_padre)
        self._Hito__momento = valor
        
    def actualizar(self):
        '''Analiza el estado del hito para saber si se ha producido o no. Cuando el tiempo del proyecto sea mayor que el
        valor establecido en el hito, entonces habrá ocurrido'''

        if Elemento.get_proyecto().tmpo_actual >= self.valor:
            self.__ocurrido = True
        else:
            self.__ocurrido = False

    # @property
    # def momento(self):
    #     """Momento en que ocurre el hito, se haya producido o no. Solo lectura"""
    #     return self.__momento



class Hito_prog(Hito):
    """Hito de progreso. Define el momento en el que el padre alcanzó el progreso especificado en la propiedad valor. El
    padre puede ser un grupo, una tarea o no estar definido explícitamente. En el caso de que no sea explícito se asume 
    como padre el proyecto mismo. Si el hito aún no ocurrió el valor del momento será None, y en caso de que haya ocurrido
    tendrá el valor de tiempo correspondiente. Éste valor de tiempo siempre será relativo al proyecto, no importa quién sea
    el padre del hito."""

    def __init__(self, nombre, valor, id_padre=0):
        super(Hito_tmpo, self).__init__(nombre, valor, 'progreso', id_padre)
        self._Hito__momento = None

        # Si el padre no tiene la propiedad progreso, entonces devuelvo un error
        if not hasattr(padre, progreso):
            raise Error_de_progreso(padre)

    def actualizar(self):
        '''Analiza el estado del hito para saber si se ha producido o no. Cuando el progreso del padre sea mayor que el
        valor establecido en el hito, entonces habrá ocurrido'''

        if Elemento.get_elem(self.id_padre).progreso >= self.valor:
            self.__ocurrido = True
            self._Hito__momento = Elemento.get_proyecto().tmpo_actual
        else:
            self.__ocurrido = False
            self._Hito__momento = None



    # @property
    # def momento(self):
    #     """Momento en que ocurre el hito. Si el hito ya ha ocurrido adquiere como valor el tiempo global en el que se 
    #     produce. Si aún no ha ocurrido, su valor es None hasta que el hito ocurra. Solo lectura"""
    #     return self.__momento

    

class Bloque(Elemento):
    """Elemento que define un bloque de avance en un proyecto. Puede ser una tarea, un grupo de tareas, o el proyecto
    completo."""

    def __init__(self, nombre, inicio, fin, precedentes=[], subtipo=None, padre=0):
        super(Bloque, self).__init__(nombre, 'bloque')
        self.__inicio = Hito_tmpo('inicia:'+nombre, inicio, self.id) 
        self.__fin = Hito_tmpo('fin:'+nombre, fin, self.id)  
        self.__precedentes = precedentes 
        self.__estado = 'esperando'  #  Los estados posibles son: 'esperando', 'demorado', 'ejecutando', 'pausado', 'cancelado', 'finalizado'
        self.__padre = 0  
        self.__progreso = 0.0  # Progreso del bloque
        self.__subtipo = subtipo  # Subtipo de bloque. Puede ser grupo, tarea o proyecto



    @property
    def inicio(self):
        """Hito de inicio del bloque. Solo lectura."""
        return self.__inicio

    @property
    def fin(self):
        """Hito de fin del bloque. Solo lectura."""
        return self.__fin    
    
    @property
    def duracion(self):
        '''Duracion del bloque. Solo lectura'''
        return self.__fin.valor - self.__inicio.valor
    
    @property
    def precedentes(self):
        """Hitos cuyos estados de ocurrencia deben ser True para que el bloque comience. Si no hay precedentes, entonces 
        comienza en el valor establecido en inicio. Solo lectura."""
        return self.__precedentes

    @property
    def estado(self):
        """Estado actual de la tarea. Solo lectura.
        Los estados posibles son:
        'esperando'  --> La tarea aún está a término, esperando a que se complete su lista de precedentes
        'demorado'   --> La tarea está retrasada, esperando a que se complete su lista de precedentes
        'ejecutando' --> La tarea comenzó y se está ejecutando
        'pausado'    --> La tarea comenzó, pero se ha establecido una pausa en su ejecución
        'cancelado'  --> La tarea había comenzado, pero se produjo la cancelación de su ejecución
        'finalizado' --> La tarea llegó al final de su ejecución
        """
        return self.__estado
    
    # @property
    # def grupo_padre(self):
    #     """Grupo al que pertenece la tarea en el caso que así fuera. Si no tiene grupo asignado el valor es None. 
    #     Solo lectura."""
    #     return self.__padre
    
    @property
    def progreso(self):
        '''Porcentaje con el progreso actual de la tarea. Solo lectura.'''
        return self.__progreso
    

    @property
    def tipo_bloque(self):
        return self._tipo_bloque
    
        

class Grupo(Bloque):
    """Elemento para agrupar distintos hitos, tareas u otros grupos."""
    def __init__(self, nombre, hijos=[], precedentes=[], padre=0):

        # Busco el menor y mayor momento entre los hijos del grupo
        inicio = 0
        fin = 1  #  El bloque tiene como minimo una duracion de 1

        if len(hijos)==0 :  # Verifico que tenga hijos
            raise Error_de_grupo(nombre)

        else:
            for h in hijos:
                if h.tipo == 'hito':  #  Si es un hito contiene el atributo momento, que es un int
                    if h.momento < inicio:
                        inicio = h.momento
                    elif h.momento > fin:
                        fin = h.momento
                elif h.tipo == 'bloque':  #  Si es un bloque contiene el atributo inicio, que es de tipo hito
                    if h.inicio.momento < inicio:
                        inicio = h.inicio.momento
                    if h.fin.momento > fin:
                        fin = h.fin.momento
                else:
                    raise Error_de_momento(h)

        super(Grupo, self).__init__(nombre, inicio, fin, precedentes, 'grupo', padre)

        self.__hijos = hijos

    def agregar_hijo(self, hijo):
        """Agrega un hito, tarea o grupo al grupo actual"""

        if hijo.tipo == 'hito':  #  Si es un hito contiene el atributo momento, que es un int
            momento_ini = hijo.momento
            momento_fin = hijo.momento
        elif hijo.tipo == 'bloque':  #  Si es un bloque contiene el atributo inicio, que es de tipo hito
            momento_ini = hijo.inicio.momento
            momento_fin = hijo.fin.momento
        


        if momento_ini < self.inicio.momento:
            self._Bloque__inicio = Hito_tmpo('inicia:'+self.nombre, momento_ini, self.id) 

        if momento_fin > self.fin.momento:
            self._Bloque__fin = Hito_tmpo('fin:'+self.nombre, momento_fin, self.id) 

        self.__hijos.append(hijo)
        hijo._Elemento__padre = self.id


    @property
    def hijos(self):
        """Devuelve una tupla con los integrantes del grupo. Solo lectura."""
        return tuple(self.__hijos)
    

    @property
    def progreso(self):
        """Devuelve un porcentaje indicando el progreso actual del grupo"""

        valor_total = 0.0
        valor_actual = 0.0

        for h in self.__hijos:
            if h.tipo == 'bloque':
                valor_total =+ 100
                valor_actual =+ h.progreso

        porcentaje = (valor_actual/valor_total)*100


        return porcentaje
        
    
class Tarea(Bloque):
    """Elemento que define un proceso a realizar en un proyecto."""
    def __init__(self, nombre, inicio, fin, precedentes=[], padre=0):
        super(Tarea, self).__init__(nombre, inicio, fin, precedentes, 'tarea', padre)

    @property
    def progreso(self):
        '''Porcentaje realizado de la tarea'''
        return self._Bloque__progreso
    
    
    @progreso.setter
    def progreso(self, val):
        self._Bloque__progreso = val
    
        
class Proyecto(Bloque):
    """Clase que engloba todo el contenido del proyecto."""

    def __init__(self, nombre):
        super(Proyecto, self).__init__(nombre, 0, None, [], 'proyecto', None)

        del precedentes # El proyecto no tiene preecdentes. Siempre puede inicializarse
        del padre  # El proyecto es padre de todos los elementos. No tiene ningun objeto de mayor jerarquia

        self._Bloque__id = 0  # El proyecto siempre tiene el id = 0
        Elemento.__elems[0] = self

        self.base_tmpo = 0
        self.unidad = 'Intervalos'
        self.tmpo_transcurrido = 0
    
    