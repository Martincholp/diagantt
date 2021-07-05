#! /usr/bin/env python
#-*- coding: UTF-8 -*-

from excepciones import *


'''Estructura de clases del sistema de gestion de diagramas de Gantt'''


#####   CONSTANTES UTILIZADAS EN EL MODULO   ############

##   ESTADO DE EJECUCION DE UNA TAREA, GRUPO, DIAGRAMA O PROYECTO   ###

Estado_indeterminado = 0
Estado_esperando     = 1
Estado_demorado      = 2
Estado_ejecutando    = 3
Estado_pausado       = 4
Estado_cancelado     = 5
Estado_finalizado    = 6


def estados_string(estado):
    ''' Devuelve un string indicando el estado de ejecucion de una tarea, grupo, diagrama o proyecto que representa el entero pasado '''

    estados = {0:'indeterminado' ,1:'esperando', 2:'demorado', 3:'ejecutando', 4:'pausado', 5:'cancelado', 6:'finalizado'}

    return estados[estado]

##   TIPOS DE ELEMENTOS   ##

Tipo_proyecto    = 0
Tipo_hito        = 1
Tipo_tarea       = 2
Tipo_grupo       = 3
Tipo_diagrama    = 4


def tipos_string(tipo):
    ''' Devuelve un string indicando el tipo de elemento que representa el entero pasado '''

    tipos = {0:'proyecto', 1:'hito', 2:'tarea', 3:'grupo', 4:'diagrama'}

    return tipos[tipo]


class Proyecto(object):
    """Clase que engloba todo el contenido del proyecto."""

    id_disponible = 1  # Id a devolver cuando se solicite. En ese momento se incrementa en 1 para la próxima petición

    def __init__(self):

        self.__tipo = 0  #  Inidica que es un proyecto
        self.__diagramas = []  # Lista con todos los diagramas del proyecto
        self.__elementos = {}
        
        self.__tiempo_global = 0
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
    def tiempo_global(self):
        ''' Tiempo transcurrido desde el comienzo del proyecto, medido en la unidad indicada en Unidad_de_tiempo. Solo lectura '''
        return self.__tiempo_global

    @property
    def estado(self):
        ''' Estado de ejecucion del proyecto. Solo lectura'''

        ###  CALCULAR A PARTIR DEL ESTADO DE SUS DIAGRAMAS  ###
        pass
    
   

    ###################################   METODOS   ################################

    def lista_diagramas(self):
        ''' Devuelve una tupla con los diagramas del proyecto. '''

        tupla_diag = tuple(self.__diagramas)  # Lo transformo a tupla para que sea inmutable

        return tupla_diag

    def add_diagrama(self, diagrama=None, nombre=None):
        """ Agrega el diagrama pasado al proyecto. Si no se pasa ningún diagrama se debe pasar un nombre para crear uno nuevo. Si tampoco hay un nombre se lanza una excepción """

        if diagrama == None:
            diag_aux = self.crear_diagrama(nombre, self)
        else:
            diag_aux = diagrama

        # Verifico que el id del diagrama no exista (si acabo de crearlo no existe, pero si estaba en otro contexto puede generar conflicto)
        while self.__elementos.has_key(diag_aux.id):
            diag_aux._Elemento__id = self.crear_id()

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

    def crear_diagrama(self, nombre):
        """ Crea y devuelve un diagrama vacío con el nombre pasado. Es un diagrama huérfano, ya que no queda asociado a ningún proyecto"""

        # Verifico que el nombre no exista
        for n in self.lista_diagramas():
            if n.nombre == nombre:
                raise Nombre_repetido(nombre)

        NewDiag = Diagrama(nombre)

        return NewDiag

    @staticmethod
    def crear_id():
        """ Crea y devuelve un identificador válido dentro del contexto del proyecto """
        id_valido = Proyecto.id_disponible
        Proyecto.id_disponible += 1
        return id_valido

    def get_elem(self, id_elem):
        '''Devuelve el elemento indicado según su id. Si no hay ningún elemento con ese id devuelve None'''

        e = self.__elementos.get(id_elem)

        return e

    def set_tiempo(self, tiempo):
        """ Establece el tiempo global del proyecto """
        self.__tiempo_global = tiempo

    def set_estado(self, val_estado):
        ''' Establece el estado de ejecucion del proyecto '''

        ######   Hacer que tambien cambien de estado sus diagramas   ######
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
        self.__tipo = tipo  # Int. Tipo de elemento (hito = 1, tarea = 2, grupo = 3, diagrama = 4)
        self.__padre = None  # Elemento. Padre del elemento
        self.__estado = Estado_esperando  # Integer. Estado del elemento (no valido para hitos)
        self.__id = Proyecto.crear_id()  # Integer. Identificador del elemento

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
        ''' Tipo de elemento (Tipo_hito, Tipo_tarea, Tipo_grupo, Tipo_diagrama). Solo lectura.'''
        return self.__tipo

    @property
    def padre(self):
        """ Padre del elemento. Si el elemento no tiene padre, entonces vale None. Solo lectura. """
        return self.__padre

    @property
    def estado(self):
        ''' Estado de ejecucion de una tarea, grupo, diagrama o proyecto'''
        return self.__estado

    def t_transcurrido(self):
        ''' Tiempo transcurrido desde el inicio de la tarea, grupo, diagrama o proyecto. Si el elemento no inicio vale None'''

        T_transc = None

        if self.inicio.ocurrido:                      #  Solo puede haber tiempo transcurrido si el elemento ha iniciado
            if self.padre.tipo == None:               #  Si el elemento es huerfano no esta asociado a ningun proyecto,
                raise Elemento_huerfano(self)   #  por lo tanto no se puede obtener el tiempo global

            T_global = self.padre._Elemento__T_global()   #  Pregunto el tiempo global al padre
            T_transc = T_global - self.inicio.t_ocur             #  Calculo el tiempo transcurrido

        return T_transc

    def __T_global(self):
        ''' Funcion que devuelve el tiempo global del proyecto '''

        if self.padre.tipo == None:         #  Si el elemento es huerfano no esta asociado a ningun proyecto,
            raise Elemento_huerfano(self)   #  por lo tanto no se puede obtener el tiempo global

        if self.padre.tipo == Tipo_proyecto:        #  Si el padre del elemento actual es el proyecto
            tg = self.padre.tiempo_global           #  obtengo el tiempo global
        else:                                       #  De lo contrario
            tg = self.padre._Elemento__T_global()   #  sigo preguntando recursivamente a los ancestros

        return tg

    def __str__(self):
        ''' Valor que se devuelve al convertir a string el elemento '''
        return self.nombre + '(' + tipos_string(self.tipo) + ')'

    def set_estado(self, val_estado):
        ''' Establece el estado de ejecucion de una tarea, grupo, diagrama o proyecto'''

        if val_estado < 0 or val_estado > 5:  #  Verifico que sea un valor correcto para el estado
            raise Error_de_estado(val_estado)

        self.__estado = val_estado


class Hito(Elemento):
    """Hito de un proyecto. Representa instantes de tiempo en un proyecto o tarea. """

    def __init__(self, nombre, t_plan, progreso=0, padre=None):

        if padre != None and padre.tipo == Tipo_hito:  #  El padre de un hito no puede ser otro hito
            raise Padre_no_valido(padre)

        super(Hito, self).__init__(nombre, padre, Tipo_hito)

        self.__ocurrido = False            #  Estado del hito
        self.__t_plan = t_plan             #  Tiempo planificado
        self.__t_ocur = None               #  Tiempo en que ocurrio. Si aun no ocurrio vale None
        # self.__t_desv = None             #  Desviacion entre el tiempoocurrido y el planificado. (lo hago directamente en una propiedad)
        self.__progreso = progreso         #  Valor de progreso que debe tener el padre para que el hito ocurra
        self.__precedentes = {}            #  Diccionario con los precedentes
        self.__triggers_ocurrido = []      #  Lista de funciones a ejecutar cuando ocurra el hito (ya sea manualmente o porque se cumple)
        self.__triggers_no_ocurrido = []   #  Lista de funciones a ejecutar si se establece manualmente como falso la ocurrencia

        #  Un hito es un instante de tiempo, por lo tanto no existe un valor transcurrido desde su inicio
        del self.t_transcurrido

        #  Ademas no tiene estados de ejecucion asociados
        del self.__estado
        del self.estado
        del self.set_estado

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

    def __init__(self, nombre, inicio, duracion, padre=None):

        if padre != None and (padre.tipo == Tipo_hito or padre.tipo == Tipo_tarea):  #  El padre de una tarea no puede ser un hito u otra tarea
            raise Padre_no_valido(padre)

        super(Tarea, self).__init__(nombre, padre, Tipo_tarea)

        self.__inicio =  Hito('Inicio', inicio, 0, self)
        self.__duracion = duracion

        #  Al establecer la duracion, hay que crear un hito para el final
        self.__fin = Hito('Final', inicio + duracion, 100, self)

        self.__progreso = 0   #  Porcentaje del progreso actual
        self.__hitos = {}  #  Lista de hitos del usuario

        #########################   PROPIEDADES   ###########################

    @property
    def inicio(self):
        ''' Hito de inicio de la tarea '''
        return self.__inicio

    @property
    def fin(self):
        ''' Hito del final de la tarea '''
        return self.__fin

    @property
    def progreso(self):
        ''' Progreso de la tarea'''
        return self.__progreso

    @progreso.setter
    def progreso(self, prog):

        if prog < 0 or prog > 100:  #  Si el progreso no está entre 0 y 100 lanzo una excepcion (debe ser expresado en porcentaje)
            raise Error_de_progreso(prog)

        self.__progreso = prog

    @property
    def duracion_plan(self):
        ''' Duracion planificada de la tarea '''
        return self.__duracion

    @property
    def duracion_ocur(self):
        ''' Duracion ocurrida de la tarea. Si la tarea aun no termino vale None '''

        dur = None

        if self.fin.ocurrido:    # Solo se puede obtener la duracion ocurrida si el hito del final ya ha ocurrido.
            dur = self.fin.t_ocur - self.inicio.t_ocur

        return dur

        #########################   METODOS   ###########################

    def crear_hito(self, nombre, t_plan, progreso=0):
        """ Crea un hito y lo agrega a la lista de hitos de usuario"""

        H = Hito(nombre, t_plan, progreso, self)  #  Hito creado para agregar

        add_hito(H)                         #  Agrego el hito a la lista de hitos de usuario

        return H                            #  Devuelvo el hito que acabo de crear

    def add_hito(self, hito):
        """ Agrega un hito a la lista de hitos de usuario """
        self.__hitos[hito.id] = hito

    def rem_hito(self, id):
        """  Quita el hito indicado de la lista de hitos de usuario """
        return self.__hitos.pop(id)

    def get_hito(self, id):
        """  Retorna el hito de usuario indicado """
        return self.__hitos[id]

    def lista_hitos(self):
        """ Devuelve una tupla con los hitos de usuario de la tarea """
        return tuple(self.__hitos.values())


class Grupo(Elemento):
    """ Clase que define un contenedor de otros elementos, como Tareas, Hitos y otros Grupos """

    def __init__(self, nombre, padre=None):
        super(Grupo, self).__init__(nombre, padre, 3)

        self.__hijos = {}

        del self.__estado  #  Lo calculo directamente con la propiedad estado y la funcion set_estado

    ############################   PROPIEDADES   ##########################

        # Buscar el menor inicio y el mayor fin entre los hijos
        #   self.__inicio = None
        #   self.__fin = None

        # Calcular la duracion planeada y la ocurrida. Deben ser property de solo lectura
        #   self.__duracion_plan = None
        #   self.__duracion_ocur = None

        # Calcular el progreso segun el de los hijos. Debe ser property de solo lectura
        #   self.__progreso = None

    # @property
    # def estado(self):
    #     ''' Devuelve el estado del grupo '''

    #     # Calcular el estado segun los estados de los hijos
    #     return self.__estado

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

    ########   Hacer que modifique todos los estados de sus hijos (grupos y tareas) tambien   #########
    # def set_estado(self, val_estado):
    #    pass


class Diagrama(Grupo):
    """ Clase que define un diagrama de Gantt """

    def __init__(self, nombre, proyecto=None):
        super(Diagrama, self).__init__(nombre, 0)

        self.__proyecto = proyecto
        self.__tipo = 4

    ####################   PROPIEDADES   ####################

    @property
    def proyecto(self):
        """ Proyecto al cual pertenece el diagrama. Si proyecto=None se considera un diagrama huerfano. Es equivalente a la propiedad 'Diagrama.padre'. Solo lectura """
        return self.__proyecto

    @property
    def padre(self):
        """ Proyecto al cual pertenece el diagrama. Si proyecto=None se considera un diagrama huerfano. Es equivalente a la propiedad 'Diagrama.proyecto'. Solo lectura """

        return self.__proyecto  #  Se utiliza por compatibilidad

    def set_proyecto(self, proyecto):
        """ Establece a que proyecto pertenece el diagrama. Para dejarlo huerfano hacer proyecto=None """

        if self.__proyecto != None:
            # Eliminar este diagrama de la lista del proyecto anterior
            self.__proyecto.rem_diagrama(self)

        self.__proyecto = proyecto



