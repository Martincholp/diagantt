#! /usr/bin/env python
#-*- coding: UTF-8 -*-

'''Estructura de clases del sistema de gestion de diagramas de Gantt'''


class Elemento(object):
    """ Elementos basicos de un diagrama de Gantt """

    def __init__(self, nombre, padre, tipo):

        self.__nombre = nombre  # String. Nombre asigando al elemento
        self.__tipo = tipo  # String. Tipo de elemento ('hito', 'tarea', 'grupo', 'diagrama')
        self.__padre = None  # Elemento. Padre del elemento

    # COSAS PARA HACER

        # Solicitar un id disponible a la clase proyecto
        #   self.__id = 0  # Integer. Identificador del elemento

    # @property
    # def id(self):
    #     '''Identificador unico del elemento. Solo lectura.'''
    #     return self.__id

    @property
    def nombre(self):
        '''Nombre del elemento.'''
        return self.__nombre

    @nombre.setter
    def nombre(self, val):
        self.__nombre = val

    @property
    def tipo(self):
        ''' Tipo de elemento (hito, tarea, grupo, diagrama). Solo lectura.'''
        return self.__tipo

    @property
    def padre(self):
        """ Padre del elemento. Si el elemento no tiene padre, entonces vale None. Solo lectura. """
        return self.__padre


class Hito(Elemento):
    """Hito de un proyecto. Representa instantes de tiempo en un proyecto o tarea. """

    def __init__(self, nombre, t_plan, progreso=0, padre=None):  #  Los valores para el tipo pueden ser 'tiempo' o 'progreso'
        super(Hito, self).__init__(nombre, padre, 'hito')

        self.__ocurrido = False
        self.__t_plan = t_plan
        self.__t_ocur = None
        # self.__t_desv = None    LO HAGO CON PROPERTY
        self.__progreso = progreso
        self.__precedentes = {}
        self.__triggers_lanzar = []
        self.__triggers_restablecer = []

    @property
    def ocurrido(self):
        '''Estado del hito. Si el hito ya ha ocurrido devuelve True, de lo contrario devuelve False. Solo lectura.'''
        return self.__ocurrido

    @property
    def progreso(self):
        """ Progreso que debe tener el padre para que el hito para que ocurra. Solo lectura"""
        return self.__progreso

    @property
    def t_plan(self):
        """ Instante de tiempo planificado en el hito. Solo lectura"""
        return self.__t_plan

    @property
    def t_ocur(self):
        """ Instante de tiempo en el que ocurre el hito. Si aún no ocurrió su valor es None. Solo lectura"""
        return self.__ocur

    @property
    def t_desv(self):
        """ Desviación entre el momento en que ocurrió el hito y el tiempo planificado. Si aún el hito no ocurrió su valor es None. Solo lectura"""
        if self.ocurrido:
            return self.__t_plan - self.__t_ocur
        else:
            return None

    def actualizar(self):
        ''' Verifica la ocurrencia del hito según el tiempo planificado y el progreso, y cambia su estado de ocurrencia ejecutando los trigger correspondientes '''
        pass

    def add_trigger_lanzar(self, accion):
        """  """
        pass

    def rem_trigger_lanzar(self, index):
        """  """
        pass

    def get_trigger_lanzar(self, index):
        """  """
        pass

    def add_trigger_restablecer(self, accion):
        """  """
        pass

    def rem_trigger_restablecer(self, index):
        """  """
        pass

    def get_trigger_restablecer(self, index):
        """  """
        pass

    def add_precedente(self, precedente):
        """  """
        pass

    def rem_precedente(self, id):
        """  """
        pass

    def get_precedente(self, id):
        """  """
        pass

    def lanzar(self):
        """ Establece el hito como ocurrido sin verificar el progreso ni los precedentes, y ejecuta los triggers_lanzar asociados. """
        pass

    def resetear(self):
        """ Establece el hito como no ocurrido sin verificar el progreso ni los precedentes, y ejecuta los triggers_restablecer asociados. """
        pass


class Tarea(Elemento):
    """ Elemento que define un proceso a realizar en un proyecto."""

    def __init__(self, nombre, inicio, fin, padre=None):
        super(Tarea, self).__init__(nombre, padre, 'tarea')

        self.__inicio = inicio
        self.__fin = fin
        self.__progreso = 0
        self.__estado = 'esperando'  # 'esperando'|'demorado'|'ejecutando'|'pausado'|'cancelado'|'finalizado'
        self.__hitos = {}  #  Lista de hitos del usuario

    # COSAS PARA HACER

        # Calcular la duracion planificada y la duracion ocurrida. Hacerlo en una property de solo lectura
        #   self.__duracion_plan = None
        #   self.__duracion_ocur = None

    def add_hito(self, hito):
        """ Agrega un hito a la lista de hitos de la tarea """
        pass

    def rem_hito(self, id):
        """  Quita el hito indicado de la lista de hitos de la tarea  """
        pass

    def get_hito(self, id):
        """  Retorna el hito indicado """
        pass


class Grupo(Elemento):
    """ Clase que define un contenedor de otros elementos, como Tareas, Hitos y otros Grupos """

    def __init__(self, nombre, padre=None):
        super(Grupo, self).__init__(nombre, padre, 'grupo')

        self.__hijos = {}

    # COSAS PARA HACER.

        # Buscar el menor inicio y el mayor fin entre los hijos
        #   self.__inicio = None
        #   self.__fin = None

        # Calcular la duracion planeada y la ocurrida. Deben ser property de solo lectura
        #   self.__duracion_plan = None
        #   self.__duracion_ocur = None

        # Calcular el progreso segun el de los hijos. Debe ser property de solo lectura
        #   self.__progreso = None

    def add_hijo(self, hijo):
        """ Agrega un hijo al contenedor (hito, tarea, u otro grupo)"""
        pass

    def rem_hijo(self, id):
        """ Quita el hijo indicado del contenedor """
        pass

    def get_hijo(self, id):
        """ Retorna el hijo con el id indicado """
        pass


class Diagrama(Grupo):
    """ Clase que define un diagrama de Gantt """

    def __init__(self, nombre, proyecto=None):
        super(Diagrama, self).__init__(nombre, 0)

        del self.padre
        self.__proyecto = proyecto
        self.__tipo = 'diagrama'


class Proyecto(object):
    """Clase que engloba todo el contenido del proyecto."""

    def __init__(self):

        self.__diagramas = {}
        self.__elementos = {}

        self.__tiempo_transcurrido = 0
        self.__tiempo_unidad = ''

    def nuevo(self, nombre):
        """ Crea un nuevo proyecto vacío """
        pass

    def cargar(self, url):
        """ Carga el proyecto especificado en 'url' """
        pass

    def guardar(self, url):
        """ Guarda el proyecto en la ruta indicada en 'url' """
        pass

    def add_diagrama(self, diagrama):
        """ Agrega una diagrama nuevo al proyecto """
        pass

    def rem_diagrama(self, id):
        """ Quita el diagrama indicado del proyecto """
        pass

    def get_diagrama(self, id):
        """ Retorna el diagrama indicado """
        pass

    def create_id(self):
        """ Crea un identificador válido dentro del cotexto del proyecto """
        pass

   @staticmethod
    def get_elem(id):
        '''Devuelve el elemento indicado según su id'''
        pass

    def set_tiempo(self, valor):
        """  """
        pass



