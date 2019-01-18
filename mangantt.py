#! /usr/bin/env python
#-*- coding: UTF-8 -*-

'''Programa para la creacion y manejo de diagramas de Gantt'''



##  EXCEPCIONES  ##
class Error_de_tipo(Exception):
    """Se lanza al utilizar un tipo no válido"""
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return "El tipo " + self.val + " no es válido"

class Error_de_progreso(Exception):
    """Ocurre al no poder computar u obtener el progreso de un elemento"""
    def __init__(self, elem):
        self.elem = elem

    def __str__(self):
        return "No se puede obtener el progreso del elemento " + elem.nombre
        
class Progreso_no_valido(Exception):
    """Error al ingresar un valor de progreso que no es correcto para la acción que se intenta realizar"""
    def __init__(self, valor):
        self.valor = valor
        self.mensaje = "El valor " + str(self.valor) + " no es correcto"

    def __str__(self):
        return self.mensaje


class Error_de_agregado(Exception):
    """Error al intentar agregar un elemento que no es apto para tal accion"""
    def __init__(self, valor):
        self.valor = valor
        self.mensaje = "El elemento " + str(self.nombre) + " no se puede agregar."

    def __str__(self):
        return self.mensaje


class Elemento(object):
    """Elementos basicos de un diagrama de Gantt"""
    __id_actual = 0
    __elems = {}

    @staticmethod
    def get_id():
        '''Devuelve un número de identificador disponible'''
        res = Elemento.__id_actual
        Elemento.__id_actual =+ 1

        return res


    def __init__(self, nombre, tipo):
        
        self.__nombre = nombre
        self.__id = Elemento.get_id()  # Identificador del elemento
        self.__tipo_elem = tipo  # Tipo de elemento ('hito', 'tarea', 'grupo')
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
        '''Identificador unico del elemento. Solo lectura.'''
    def id(self):
        return self.__id

    @property
    def tipo_elem(self):
        '''Tipo de elemento (hito, tarea, grupo). Solo lectura.'''
        return self.__tipo_elem
    
    @property
    def padre(self):
        """Padre del elemento. Si el elemento no tiene padre, entonces vale None"""
        return self.__padre
    
        

class Hito(Elemento):
    """Hito de un proyecto. Representa instantes de tiempo en un proyecto o tarea. Cuando no se especifica el tipo de hito
    se crea un hito de tiempo por defecto."""
    

    def __init__(self, nombre, valor, tipo='tiempo', padre=None):  #  Los valores para el tipo pueden ser 'tiempo' o 'progreso'
        super(Hito, self).__init__(nombre, 'hito')
        
        self.__ocurrido = False
        self.__valor = valor
        self.__tipo = tipo
        self._Hito__padre = padre

        if tipo=='tiempo':
            self.__momento = valor
        elif tipo=='progreso':
            if not hasattr(padre, progreso):
                raise Error_de_progreso(padre)

            self.__momento = None
        else:
            raise Error_de_tipo(tipo)


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
    def tipo(self):
        """Tipo de hito. Los valores que puede adquirir esta propiedad son 'tiempo' y 'progreso', siendo el hito
        de tiempo el valor por defecto. Si es un hito de tiempo su estado de ocurrencia pasara a True cuando el
        tiempo global del proyecto sea mayor que el establecido como valor del hito. En caso de que sea de progreso
        se debe establecer una tarea o grupo y su estado de ocurrencia será True cuando el progreso de dicha tarea
        o grupo sea mayor al establecido como valor del hito. Solo lectura."""
        return self.__tipo
    

    @property
    def valor(self):
        '''Valor que definira cuando se produce un hito. Si es de tiempo, valor se compara con el tiempo global del 
        proyecto, y si es de progreso se compara con el progreso del elemento pasado como padre.'''
        return self.__valor
    
    @valor.setter
    def valor(self, val):
        self.__valor = val
    

    @property
    def padre(self):
        """Elemento del cual se obtiene el progreso cuando el tipo de hito es 'progreso'. Solo lectura."""
        return self.__padre
    
    

class Tarea(Elemento):
    """Tarea a realizar en un proyecto"""
    def __init__(self, nombre, inicio, fin, precedentes=[]):
        super(Tarea, self).__init__(nombre, 'tarea')
        self.__inicio = Hito('inicia:'+nombre, inicio) 
        self.__fin = Hito('fin:'+nombre, fin)  
        self.__precedentes = precedentes
        self.__estado = 'espera'  #  Los estados posibles son: 'esperando', 'demorado', 'ejecutando', 'pausado', 'cancelado', 'finalizado'
        self.__padre = None  #  Si pertenece a un grupo, ese grupo será el padre de esta tarea
        self.__progreso = 0.0  #  Progreso de la tarea


    @property
    def inicio(self):
        """Hito de inicio de la tarea. Solo lectura."""
        return self.__inicio

    @property
    def fin(self):
        """Hito de fin de la tarea. Solo lectura."""
        return self.__fin
    
    @property
    def duracion(self):
        '''Duracion de la tarea. Solo lectura'''
        return self.__fin.valor - self.__inicio.valor
    
    @property
    def precedentes(self):
        """Hitos que cuyo estado de ocurrencia debe ser True para que la tarea comience. Solo lectura."""
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
    
    @property
    def grupo_padre(self):
        """Grupo al que pertenece la tarea en el caso que así fuera. Si no tiene grupo asignado el valor es None. 
        Solo lectura."""
        return self.__padre
    
    @property
    def progreso(self):
        '''Porcentaje con el progreso actual de la tarea'''
        return self.__progreso
    
    
    @progreso.setter
    def progreso(self, val):
        self.__progreso = val
    
        

class Grupo(Elementos):
    """Elemento para agrupar distintas tareas o grupos de tareas"""
    def __init__(self, nombre, hijos=[]):
        super(Grupo, self).__init__(nombre, 'grupo')
        
        #self.__padre = None  --> Esta definido en la clase madre Elemento
        self.__hijos = hijos

    def agregar_hijo(self, hijo):
        """Agrega una tarea o grupo al grupo actual"""
        if not hasattr(hijo, grupo_padre):
            raise Error_de_agregado(hijo)

        self.__hijos.append(hijo)
        if hijo.tipo_elem == 'tarea':
            hijo._Tarea__padre = self
        elif hijo.tipo_elem == 'grupo':
            hijo._Grupo__padre = self


    @property
    def hijos(self):
        """Devuelve una tupla con los integrantes del grupo. Solo lectura."""
        return tuple(self.__hijos)

    @property
    def grupo_padre(self):
        """Grupo al que pertenece el grupo en el caso que así fuera. Si no tiene grupo asignado el valor es None. 
        Solo lectura."""
        return self.padre  # Obtiene el valor de Elemento
    

    @property
    def inicio(self):
        """Busca en los hitos de sus hijos el momento mas bajo y devuelve un hito de tiempo con ese valor.
        Si hay hitos de progreso que aun no han ocurrido se los ignora. Solo lectura."""

        menor = 0  #  Menor momento encontrado

        for h in self.__hijos:
            mh = h.inicio.momento
            if not mh == None:
                if mh < menor:
                    menor = mh

        hito_inicio = Hito('inicia:'+self.nombre, menor)

        
        return self.hito_inicio
    

    @property
    def fin(self):
        """Busca en los hitos de sus hijos el momento mas alto y devuelve un hito de tiempo con ese valor.
        Si hay hitos de progreso que aun no han ocurrido se los ignora. Solo lectura."""

        mayor = 0  #  Mayor momento encontrado

        for h in self.__hijos:
            mh = h.inicio.momento
            if not mh == None:
                if mh > mayor:
                    mayor = mh

        hito_fin = Hito('fin:'+self.nombre, mayor)

        
        return self.hito_fin
    

    @property
    def duracion(self):
        """Devuelve la duracion del grupo. Solo lectura."""
        return self.fin.momento - self.inicio.momento

    @property
    def progreso(self):
        """Devuelve un porcentaje indicando el progreso actual del grupo"""

        valor_total = 0.0
        valor_actual = 0.0

        for h in self.__hijos:
            valor_total =+ 100
            valor_actual =+ h.progreso

        porcentaje = (valor_actual/valor_total)*100


        return porcentaje
        
    


    
    