#! /usr/bin/env python
#-*- coding: UTF-8 -*-

from excepciones import *


'''Estructura de clases del sistema de gestion de diagramas de Gantt'''


class Proyecto(object):
    """Clase que engloba todo el contenido del proyecto."""

    id_disponible = 1  # Id a devolver cuando se solicite. En ese momento se incrementa en 1 para la próxima petición

    def __init__(self):

        self.__diagramas = []  # Lista con todos los diagramas del proyecto
        self.__elementos = {}

        self.__tiempo_transcurrido = 0
        self.__tiempo_unidad = ''
        self.__nombre = ''
        self.__ultima_url = ''

    #######################   PROPIEDADES   ##################

    @property
    def nombre(self):
        ''' Establece el nombre del proyecto '''
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def unidad_de_tiempo(self):
        ''' Establece cual va a ser la unidad de tiempo representado en el diagrama '''
        return self.__tiempo_unidad

    @unidad_de_tiempo.setter
    def unidad_de_tiempo(self, unidad):
        self.__tiempo_unidad = unidad

    @property
    def tiempo_transcurrido(self):
        ''' Tiempo transcurrido desde el comienzo del proyecto, medido en la unidad indicada en Unidad_de_tiempo. Solo lectura '''
        return self.__tiempo_transcurrido

    ###################################   METODOS   ################################

    def lista_diagramas(self):
        ''' Devuelve una tupla con los diagramas del proyecto. '''

        tupla_diag = tuple(self.__diagramas)  # Lo transformo a tupla para que sea inmutable

        return tupla_diag

    def add_diagrama(self, diagrama=None, nombre=None):
        """ Agrega el diagrama pasado al proyecto. Si no se pasa ningún diagrama se debe pasar un nombre para crear uno nuevo. Si tampoco hay un nombre se lanza una excepción """

        if diagrama == None:
            diag_aux = self.create_diagrama(nombre, self)
        else:
            diag_aux = diagrama

        # Verifico que el id del diagrama no exista (si acabo de crearlo no existe, pero si estaba en otro contexto puede generar conflicto)
        while self.__elementos.has_key(diag_aux.id):
            diag_aux._Elemento__id = self.create_id()

        # Agrego el diagrama a la lista de diagramas y de elementos
        self.__diagramas.append(diag_aux)
        self.__elementos[diag_aux.id] = diag_aux

        #  Devuelvo el diagrama agregado
        return diag_aux

    def rem_diagrama(self, diagrama):
        """ Quita el diagrama indicado del proyecto """

        # Quito el diagrama de la lista de diagramas y de elementos y lo hago huerfano
        self.__diagramas.remove(diagrama)
        self.__elementos.pop(diagrama.id)
        diagrama._Diagrama__proyecto = None

        # Devuelvo el diagrama que acabo de quitar
        return diagrama

    def buscar_diagrama_por_nombre(self, nombre):
        """ Retorna el diagrama indicado buscando por el nombre. Si no se encuentra un diagrama con ese nombre devuelve None"""

        res = None

        for diag in self.lista_diagramas():
            if diag.nombre == nombre:
                res = diag
                break

        return res

    def buscar_diagrama_por_id(self, diag_id):
        """ Retorna el diagrama indicado buscando por el id. Si no se encuentra un diagrama con ese id devuelve None"""

        res = None

        for diag in self.lista_diagramas():
            if diag.id == diag_id:
                res = diag
                break

        return res

    def create_diagrama(self, nombre):
        """ Crea y devuelve un diagrama vacío con el nombre pasado. Es un diagrama huérfano, ya que no queda asociado a ningún proyecto"""

        # Verifico que el nombre no exista
        for n in self.lista_diagramas():
            if n.nombre == nombre:
                raise Nombre_repetido(nombre)

        NewDiag = Diagrama(nombre)

        return NewDiag

    @staticmethod
    def create_id():
        """ Crea y devuelve un identificador válido dentro del contexto del proyecto """
        id_valido = Proyecto.id_disponible
        Proyecto.id_disponible += 1
        return id_valido

    def get_elem(self, id_elem):
        '''Devuelve el elemento indicado según su id. Si no hay ningún elemento con ese id devuelve None'''

        e = self.__elementos.get(id_elem)

        return e

    def set_tiempo(self, valor):
        """  """
        pass

    def cargar(self, url):
        """ Carga el proyecto especificado en 'url' """

        ################   COMPLETAR: NO ESTA TERMINADA  #############

        self.__ultima_url = url  # Hacer esto si la carga es exitosa

    def guardar(self, url=None):
        """ Guarda el proyecto en la ruta indicada en 'url'. Si no se especifica una url se utiliza la última pasada """

        ################   COMPLETAR: NO ESTA TERMINADA  #############

        if url == None:
            ruta = self.__ultima_url
        else:
            ruta = url

        if ruta == '':
            # Lanzar error de url vacia
            pass

        else:
            # Intentar guardar. Luego guardar la ultima url solo si el guardado es exitoso
            self.__ultima_url = ruta


class Elemento(object):
    """ Elementos basicos de un diagrama de Gantt """

    def __init__(self, nombre, padre, tipo):

        if nombre == None or nombre == '':
            raise Nombre_no_valido(nombre)

        self.__nombre = nombre  # String. Nombre asigando al elemento
        self.__tipo = tipo  # String. Tipo de elemento ('hito', 'tarea', 'grupo', 'diagrama')
        self.__padre = None  # Elemento. Padre del elemento
        self.__id = Proyecto.create_id()  # Integer. Identificador del elemento

    #########################   PROPIEDADES   #########################

    @property
    def id(self):
        '''Identificador unico del elemento. Solo lectura.'''
        return self.__id

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

    def __init__(self, nombre, t_plan, progreso=0, padre=None):
        super(Hito, self).__init__(nombre, padre, 'hito')

        self.__ocurrido = False            #  Estado del hito
        self.__t_plan = t_plan             #  Tiempo planificado
        self.__t_ocur = None               #  Tiempo en que ocurrio. Si aun no ocurrio vale None
        # self.__t_desv = None             #  Desviacion entre el tiempoocurrido y el planificado. (lo hago directamente en una propiedad)
        self.__progreso = progreso         #  Valor de progreso que debe tener el padre para que el hito ocurra
        self.__precedentes = {}            #  Diccionario con los precedentes
        self.__triggers_ocurrido = []      #  Lista de funciones a ejecutar cuando ocurra el hito (ya sea manualmente o porque se cumple)
        self.__triggers_no_ocurrido = []   #  Lista de funciones a ejecutar si se establece manualmente como falso la ocurrencia

    ######################   PROPIEDADES   ################################

    @property
    def ocurrido(self):
        '''Estado del hito. Si el hito ya ha ocurrido devuelve True, de lo contrario devuelve False. Solo lectura.'''
        return self.__ocurrido

    @property
    def progreso(self):
        """ Progreso que debe tener el padre para que el hito ocurra. Solo lectura"""
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

    ######################   METODOS   ################################

    def actualizar(self):
        ''' Verifica la ocurrencia del hito según el tiempo planificado y el progreso, y cambia su estado de ocurrencia ejecutando los trigger correspondientes '''

        if not self.ocurrido:                                   #  Si el hito no ocurrio hago las verificaciones

            padre = self.padre                                  #  Verifico cual es el elemento padre
            if padre == None:                                   #  y si no tiene (es un hito huerfano)
                raise Elemento_huerfano(self)                   #  lanzo una excepcion

            aux_ocurrir = False                                 #  Auxiliar para saber si debe ocurrir o no. Por defecto no debe ocurrir

            if self.padre.progreso >= self.progreso:            #  Si el progreso del padre es mayor o igual que el del hito
                aux_ocurrir = True                              #  establezco la variable aux_ocurrir a True y
                for prec in self.__precedentes.itervalues():    #  verifico los precedentes.
                    if not prec.ocurrido:                       #  Si algun precedente no ocurrio
                        aux_ocurrir = False                     #  establezco la aux_ocurrir a Falso
                        break                                   #  y salgo del bucle
                                                                #  Si todos los precedentes ocurrieron, aux_ocurrir seguira siendo True

            if aux_ocurrir:                                     #  Si debe ocurrir
                self.set_ocurrido(True)                         #  seteo su estado a verdadero

        return self.ocurrido                                    #  Devuelvo el estado final en que quedo el hito

    def set_ocurrido(self, estado):
        """ Establece el estado del hito sin verificar el progreso ni los precedentes, y ejecuta los triggers asociados. """

        if estado:                                  #  Si el hito ha ocurrido
            self.__ocurrido = True                  #  establezco a True la variable interna
            for t in self.__triggers_ocurrido:      #  y a cada trigger de la lista de ocurrido
                t()                                 #  lo ejecuto.
        else:                                       #  Si el hito no ha ocurrido
            self.__ocurrido = False                 #  establezco a False la variable interna
            for t in self.__triggers_no_ocurrido:   #  y a cada trigger de la lista de no ocurrido
                t()                                 #  lo ejecuto

        return self.ocurrido                        #  Devuelvo el estado final del hito

    def add_trigger_ocur(self, trigger):
        """ Agrega un trigger que se ejecutara cuando se establezca el hito a True """
        self.__triggers_ocurrido.append(trigger)

    def rem_trigger_ocur(self, trigger):
        """ Quita el trigger indicado de la lista de triggers para el hito ocurrido """
        self.__triggers_ocurrido.remove(trigger)

    def lista_trigger_ocur(self):
        """ Devuelve una tupla con los trigger para el hito ocurrido """
        return tuple(self.__triggers_ocurrido)

    def add_trigger_no_ocur(self, trigger):
        """ Agrega un trigger que se ejecutara cuando se establezca el hito a False """
        self.__triggers_no_ocurrido.append(trigger)

    def rem_trigger_no_ocur(self, trigger):
        """ Quita el trigger indicado de la lista de triggers para el hito no_ocurrido """
        self.__triggers_no_ocurrido.remove(trigger)

    def lista_trigger_no_ocur(self):
        """ Devuelve una tupla con los trigger para el hito no_ocurrido """
        return tuple(self.__triggers_no_ocurrido)

    def add_precedente(self, precedente):
        """ Agrega un precedente a la lista de precedentes """
        self.__precedentes[precedente.id] = precedente

    def rem_precedente(self, id):
        """ Quita de la lista de precedentes el hito con el id indicado """
        return self.__precedentes.pop(id)

    def get_precedente(self, id):
        """ Obtiene el hito precedente con el id indicado """
        return self.__precedentes[id]

    def lista_precedentes(self):
        """ Devuelve una tupla con los precedentes """
        return tuple(self.__precedentes.values())


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

    ############################   PROPIEDADES   ##########################

        # Buscar el menor inicio y el mayor fin entre los hijos
        #   self.__inicio = None
        #   self.__fin = None

        # Calcular la duracion planeada y la ocurrida. Deben ser property de solo lectura
        #   self.__duracion_plan = None
        #   self.__duracion_ocur = None

        # Calcular el progreso segun el de los hijos. Debe ser property de solo lectura
        #   self.__progreso = None

    ############################   METODOS   ##########################

    def add_hijo(self, hijo):
        """ Agrega un hijo al contenedor (hito, tarea, u otro grupo)"""
        pass

    def rem_hijo(self, id):
        """ Quita el hijo indicado del contenedor """
        pass

    def get_hijo(self, id):
        """ Retorna el hijo con el id indicado """
        pass

    def lista_hijos(self):
        """ Devuelve una tupla con todos los hijos del grupo """
        pass


class Diagrama(Grupo):
    """ Clase que define un diagrama de Gantt """

    def __init__(self, nombre, proyecto=None):
        super(Diagrama, self).__init__(nombre, 0)

        del self.padre
        del self.__padre
        self.__proyecto = proyecto
        self.__tipo = 'diagrama'

    ####################   PROPIEDADES   ####################

    @property
    def proyecto(self):
        ''' Proyecto al cual pertenece el diagrama. Si proyecto=None se considera un diagrama huerfano. Solo lectura '''
        return self.__proyecto

    def set_proyecto(self, proyecto):
        """ Establece a que proyecto pertenece el diagrama. Para dejarlo huerfano hacer proyecto=None """

        if self.__proyecto != None:
            # Eliminar este diagrama de la lista del proyecto anterior
            self.__proyecto.rem_diagrama(self)

        self.__proyecto = proyecto



