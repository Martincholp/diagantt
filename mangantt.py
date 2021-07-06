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
    ''' Devuelve un string indicando el estado de ejecución de una tarea, grupo, diagrama o proyecto.
        estado: número que representa uno de los estados posibles (int) '''

    estados = {0: 'indeterminado' , 1: 'esperando', 2: 'demorado', 3: 'ejecutando', 4: 'pausado', 5: 'cancelado', 6: 'finalizado'}

    return estados[estado]

##   TIPOS DE ELEMENTOS   ##

Tipo_proyecto    = 0
Tipo_hito        = 1
Tipo_tarea       = 2
Tipo_grupo       = 3
Tipo_diagrama    = 4


def tipos_string(tipo):
    ''' Devuelve un string indicando el tipo de elemento que representa el entero pasado.
        tipo: número que representa uno de los tipos de elementos (int) '''

    tipos = {0: 'proyecto', 1: 'hito', 2: 'tarea', 3: 'grupo', 4: 'diagrama'}

    return tipos[tipo]


class Proyecto(object):
    """ Clase que engloba todo el contenido del proyecto."""

    id_disponible = 1  # Id a devolver cuando se solicite. En ese momento se incrementa en 1 para la próxima petición

    def __init__(self):

        self.__tipo = Tipo_proyecto  #  Inidica que es un proyecto
        self.__diagramas = {}
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
        ''' Estado de ejecución del proyecto. Solo lectura'''

        ###  CALCULAR A PARTIR DEL ESTADO DE SUS DIAGRAMAS  ###
        pass

    ###################################   METODOS   ################################

    def lista_diagramas(self):
        ''' Devuelve una tupla con los diagramas del proyecto. '''

        tupla_diag = tuple(self.__diagramas.values())  # Lo transformo a tupla para que sea inmutable

        return tupla_diag

    def crear_diagrama(self, nombre):
        """ Crea y devuelve un diagrama vacío con el nombre pasado y lo agrega al proyecto.
            nombre: nombre que debe tener el diagrama a crear (str) """

        # Verifico que el nombre no exista
        for n in self.lista_diagramas():
            if n.nombre == nombre:
                raise Nombre_repetido(nombre)

        NewDiag = Diagrama(nombre, self)

        self.add_diagrama(NewDiag)

        return NewDiag

    def add_diagrama(self, diagrama):
        """ Agrega un diagrama al proyecto.
            diagrama: diagrama que se debe agregar (Diagrama) """

        # Verifico que el id del diagrama no exista (si acabo de crearlo no existe, pero si estaba en otro contexto puede generar conflicto)
        while self.__elementos.has_key(diagrama.id):
            diagrama._Elemento__id = self.crear_id()

        # Agrego el diagrama a la lista de diagramas y de elementos
        self.__diagramas[diagrama.id] = diagrama
        self.__elementos[diagrama.id] = diagrama

        #  Devuelvo el diagrama agregado
        return diagrama

    def rem_diagrama(self, diagrama):
        """ Quita un diagrama del proyecto.
            diagrama: diagrama a quitar (Diagrama) """

        # Quito el diagrama de la lista de diagramas y de elementos y lo hago huerfano
        self.__diagramas.pop(diagrama.id)
        self.__elementos.pop(diagrama.id)
        diagrama._Diagrama__proyecto = None

        # Devuelvo el diagrama que acabo de quitar
        return diagrama

    def buscar_diagrama_por_nombre(self, nombre):
        """ Retorna el diagrama indicado buscando por el nombre. Si no se encuentra un diagrama con ese nombre devuelve None.
            nombre: nombre del diagrama a buscar (str) """

        res = None

        for diag in self.lista_diagramas():
            if diag.nombre == nombre:
                res = diag
                break

        return res

    def buscar_diagrama_por_id(self, diag_id):
        """ Retorna el diagrama indicado buscando por el id. Si no se encuentra un diagrama con ese id devuelve None.
            id: identificador del diagrama a buscar (int) """

        return self.__diagramas.get(diag_id)

    @staticmethod
    def crear_id():
        """ Crea y devuelve un identificador válido dentro del contexto del proyecto. """

        id_valido = Proyecto.id_disponible
        Proyecto.id_disponible += 1
        return id_valido

    def get_elem(self, id_elem):
        ''' Devuelve el elemento indicado según su id. Si no hay ningún elemento con ese id devuelve None.
            id_elem: identificador del elemento a devolver (int) '''

        e = self.__elementos.get(id_elem)

        return e

    def set_tiempo(self, tiempo):
        """ Establece el tiempo global del proyecto.
            tiempo: valor a establecer para el tiempo (int) """

        self.__tiempo_global = tiempo

    def set_estado(self, val_estado):
        ''' Establece el estado de ejecución del proyecto.
            val_estado: valor que debe tomar el estado (int) '''

        ######   Hacer que tambien cambien de estado sus diagramas   ######
        pass

    def cargar(self, url):
        """ Carga el proyecto especificado en 'url' """

        pass

    def guardar(self, url=None):
        """ Guarda el proyecto en la ruta indicada en 'url'. Si no se especifica una url se utiliza la última pasada """

        pass


class Elemento(object):
    """ Elementos básicos de un diagrama de Gantt """

    def __init__(self, nombre, padre, tipo):
        ''' nombre: nombre del elemento (str)
            padre: padre del elemento (Elemento)
            tipo: tipo de elemento (int) '''

        if nombre == None or nombre == '':
            raise Nombre_no_valido(nombre)

        self.__nombre = nombre  # String. Nombre asigando al elemento
        self.__tipo = tipo  # Int. Tipo de elemento (hito = 1, tarea = 2, grupo = 3, diagrama = 4)
        self.__padre = None  # Elemento. Padre del elemento
        self.__id = Proyecto.crear_id()  # Integer. Identificador del elemento

        proy = self.proyecto
        if proy != None:
            proy._Proyecto__elementos[self.id] = self

    #########################   PROPIEDADES   #########################

    @property
    def id(self):
        '''Identificador único del elemento. Solo lectura.'''
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
        ''' Tipo de elemento. Solo lectura.'''
        return self.__tipo

    @property
    def padre(self):
        """ Padre del elemento. Si el elemento no tiene padre, entonces vale None. Solo lectura. """
        return self.__padre

    @property
    def proyecto(self):
        ''' Devuelve el proyecto al cual pertenece el elemento. Si el elemento o alguno de sus ancestros es huérfano devuelve None '''

        if self.padre == None:
            proy = None

        else:
            if self.padre.tipo == Tipo_proyecto:
                proy = self.padre
            else:
                proy = self.padre.proyecto

        return proy

    ##############################   METODOS   #################################

    def t_global(self):
        ''' Función que devuelve el tiempo global del proyecto '''

        proy = self.proyecto()              #  Obtengo el proyecto del elemento

        if proy == None:                    #  Si el elemento es huerfano no esta asociado a ningun proyecto,
            raise Elemento_huerfano(self)   #  por lo tanto no se puede obtener el tiempo global y lanzo una excepcion
        else:                               #  De lo contrario
            tg = proy.tiempo_global         #  obtengo el tiempo global

        return tg

    def __str__(self):
        ''' Valor que se devuelve al convertir a string el elemento '''
        return self.nombre + '(' + tipos_string(self.tipo) + ')'


class Hito(Elemento):
    """ Elemento que representa un instante de tiempo en un diagrama, grupo o tarea. """

    def __init__(self, nombre, t_plan, progreso=0, padre=None):
        ''' nombre: nombre del hito (str)
            t_plan: tiempo planificado (int)
            progreso: progreso que debe tener el padre para que el hito ocurra (int)
            padre: padre del hito (Diagrama|Grupo|Tarea)'''

        if padre != None and padre.tipo == Tipo_hito:  #  El padre de un hito no puede ser otro hito
            raise Padre_no_valido(padre)

        if progreso < 0 or progreso > 100:
            raise Progreso_no_valido(progreso)

        super(Hito, self).__init__(nombre, padre, Tipo_hito)

        self.__ocurrido = False            #  Estado del hito
        self.__t_plan = t_plan             #  Tiempo planificado
        self.__t_ocur = None               #  Tiempo en que ocurrio. Si aun no ocurrio vale None
        self.__progreso = progreso         #  Valor de progreso que debe tener el padre para que el hito ocurra
        self.__precedentes = {}            #  Diccionario con los precedentes
        self.__triggers_ocurrido = []      #  Lista de funciones a ejecutar cuando ocurra el hito (ya sea manualmente o porque se cumple)
        self.__triggers_no_ocurrido = []   #  Lista de funciones a ejecutar si se establece manualmente como falso la ocurrencia

    ######################   PROPIEDADES   ################################

    @property
    def ocurrido(self):
        '''Estado del hito. Si el hito ya ocurrió devuelve True, de lo contrario devuelve False. Solo lectura.'''
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
        """ Desviación entre el momento en que ocurrió el hito y el tiempo planificado. Si el hito aún no ocurrió su valor es None. Solo lectura"""
        if self.ocurrido:
            return self.__t_plan - self.__t_ocur
        else:
            return None

    ######################   METODOS   ################################

    def actualizar(self):
        ''' Verifica la ocurrencia del hito según el tiempo planificado, el progreso y los precedentes, y cambia su estado de ocurrencia ejecutando los trigger correspondientes '''

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

    def set_ocurrido(self, ocurrir):
        """ Establece la ocurrencia del hito sin verificar ni el tiempo planificado, ni el progreso ni los precedentes, y ejecuta los triggers asociados. 
            ocurrir: define si establecer el estado como ocurrido o no (bool)"""

        if ocurrir:                                 #  Si el hito ha ocurrido
            self.__ocurrido = True                  #  establezco a True la variable interna
            for t in self.__triggers_ocurrido:      #  y a cada trigger de la lista de ocurrido
                t()                                 #  lo ejecuto.
        else:                                       #  Si el hito no ha ocurrido
            self.__ocurrido = False                 #  establezco a False la variable interna
            for t in self.__triggers_no_ocurrido:   #  y a cada trigger de la lista de no ocurrido
                t()                                 #  lo ejecuto

        return self.ocurrido                        #  Devuelvo el estado final del hito

    def add_trigger_ocur(self, trigger):
        """ Agrega un trigger que se ejecutará en el momento en que el hito ocurra.
            trigger: función a ejecutar (func) """

        self.__triggers_ocurrido.append(trigger)

    def rem_trigger_ocur(self, trigger):
        """ Quita el trigger indicado de la lista de triggers para el hito ocurrido
            trigger: función que se debe quitar (func) """

        self.__triggers_ocurrido.remove(trigger)

    def lista_trigger_ocur(self):
        """ Devuelve una tupla con los trigger para el hito ocurrido """

        return tuple(self.__triggers_ocurrido)

    def add_trigger_no_ocur(self, trigger):
        """ Agrega un trigger que se ejecutará cuando se establezca el hito a False forzadamente
            trigger: función a ejecutar (func) """

        self.__triggers_no_ocurrido.append(trigger)

    def rem_trigger_no_ocur(self, trigger):
        """ Quita el trigger indicado de la lista de triggers para el hito no_ocurrido 
            trigger: función que se debe quitar (func) """

        self.__triggers_no_ocurrido.remove(trigger)

    def lista_trigger_no_ocur(self):
        """ Devuelve una tupla con los trigger para el hito no_ocurrido """

        return tuple(self.__triggers_no_ocurrido)

    def add_precedente(self, precedente):
        """ Agrega un precedente a la lista de precedentes.
            precedente: hito al cual debe verificarse su estado de ocurrencia (Hito)"""

        self.__precedentes[precedente.id] = precedente

    def rem_precedente(self, id):
        """ Quita de la lista de precedentes el hito con el id indicado
            id: identificador del hito a quitar """

        return self.__precedentes.pop(id)

    def get_precedente(self, id):
        """ Obtiene el hito precedente con el id indicado
            id: identificador del hito buscado """

        return self.__precedentes[id]

    def lista_precedentes(self):
        """ Devuelve una tupla con los precedentes """

        return tuple(self.__precedentes.values())


class Tarea(Elemento):
    """ Elemento que define un proceso a realizar en un proyecto."""

    def __init__(self, nombre, inicio, duracion, padre=None):
        ''' nombre: nombre de la tarea (str)
            inicio: tiempo planificado para el hito de inicio (int)
            duracion: tiempo que durará la tarea según lo planificado (int)
            padre: padre de la tarea (Diagrama|Grupo)'''

        if padre != None and (padre.tipo == Tipo_hito or padre.tipo == Tipo_tarea):  #  El padre de una tarea no puede ser un hito u otra tarea
            raise Padre_no_valido(padre)

        super(Tarea, self).__init__(nombre, padre, Tipo_tarea)

        #  Al establecer la duracion, hay que crear un hito para el final
        self.__inicio =  Hito('Inicio', inicio, 0, self)
        self.__fin = Hito('Final', inicio + duracion, 100, self)

        self.__estado = Estado_esperando  # Integer. Estado del elemento

        self.__progreso = 0   #  Porcentaje del progreso actual
        self.__hijos = {}  #  Lista de hitos del usuario

        #########################   PROPIEDADES   ###########################

    @property
    def inicio(self):
        ''' Hito del inicio '''
        return self.__inicio

    @property
    def fin(self):
        ''' Hito del final '''
        return self.__fin

    @property
    def progreso(self):
        ''' Progreso de la tarea expresado en porcentaje'''
        return self.__progreso

    @progreso.setter
    def progreso(self, prog):

        if prog < 0 or prog > 100:  #  Si el progreso no está entre 0 y 100 lanzo una excepcion (debe ser expresado en porcentaje)
            raise Error_de_progreso(prog)

        self.__progreso = prog

    @property
    def duracion_plan(self):
        ''' Duración planificada '''
        dur = self.fin.t_plan - self.inicio.t_plan

        return dur

    @property
    def duracion_ocur(self):
        ''' Duración ocurrida. Si el hito del final aún no ocurrió, entonces duracion_ocur vale None '''

        dur = None

        if self.fin.ocurrido:    # Solo se puede obtener la duracion ocurrida si el hito del final ya ha ocurrido.
            dur = self.fin.t_ocur - self.inicio.t_ocur

        return dur

    @property
    def estado(self):
        ''' Estado de ejecución de una tarea, grupo, diagrama o proyecto'''
        return self.__estado

        #########################   METODOS   ###########################

    def t_transcurrido(self):
        ''' Tiempo transcurrido desde el inicio de la tarea, grupo, diagrama o proyecto. Si el elemento aún no inició vale None'''

        T_transc = None

        if self.inicio.ocurrido:                      #  Solo puede haber tiempo transcurrido si el elemento ha iniciado
            if self.padre.tipo == None:               #  Si el elemento es huerfano no esta asociado a ningun proyecto,
                raise Elemento_huerfano(self)   #  por lo tanto no se puede obtener el tiempo global

            T_global = self.padre._Elemento__T_global()   #  Pregunto el tiempo global al padre
            T_transc = T_global - self.inicio.t_ocur             #  Calculo el tiempo transcurrido

        return T_transc

    def crear_hito(self, nombre, t_plan, progreso=0):
        """ Crea un hito y lo agrega a la lista de hitos de usuario.
            nombre: nombre del hito (str)
            t_plan: tiempo planificado (int)
            progreso: progreso que debe tener el padre para que el hito ocurra (int)"""

        H = Hito(nombre, t_plan, progreso, self)  #  Hito creado para agregar

        self.add_hijo(H)                         #  Agrego el hito a la lista de hitos de usuario

        return H                            #  Devuelvo el hito que acabo de crear

    def add_hijo(self, hito):
        """ Agrega un hito a la lista de hitos de usuario.
            hito: hito para agregar a la lista (Hito) """

        if hito.t_plan < self.inicio.t_plan or hito.t_plan > self.fin.t_plan:   #  Si el t_plan del hito no está dentro de la tarea
            raise Tiempo_no_valido(hito.t_plan)                                 #  lanzo una excepcion

        self.__hijos[hito.id] = hito

    def rem_hijo(self, id):
        """  Quita el hito indicado de la lista de hitos de usuario.
            id: identificador del hito a quitar (int) """

        return self.__hijos.pop(id)

    def get_hijo(self, id):
        """  Retorna el hito de usuario indicado.
             id: identificador del hito a devolver (int) """

        return self.__hijos[id]

    def lista_hijos(self):
        """ Devuelve una tupla con los hitos de usuario de la tarea """

        return tuple(self.__hijos.values())

    def set_estado(self, val_estado):
        ''' Establece el estado de ejecución de una tarea, grupo, diagrama o proyecto.
            val_estado: valor que debe tomar el estado (int) '''

        if val_estado < 1 or val_estado > 6:  #  Verifico que sea un valor correcto para el estado. El estado indeterminado no se puede setear manualmente
            raise Error_de_estado(val_estado)

        self.__estado = val_estado


class Grupo(Tarea):
    """ Elemento que define un contenedor para Tareas, Hitos y otros Grupos """

    def __init__(self, nombre, padre=None):
        ''' nombre: nombre del grupo (str)
            padre: padre del grupo (Grupo|Diagrama) '''

        if padre != None and (padre.tipo == Tipo_hito or padre.tipo == Tipo_tarea):  #  El padre de un grupo no puede ser un hito ni una tarea
            raise Padre_no_valido(padre)

        super(Grupo, self).__init__(nombre, 0, 0, padre)

        self.__tipo = Tipo_grupo  #  Establezco el tipo (como derivamos de tarea, inicialmente tiene ese valor)


    ####################  NO SE COMO BORRARLOS. LOS SOBREESCRIBO LANZANDO EXCEPCION
        # del Grupo.__estado     #  Lo calculo directamente con la propiedad estado y la funcion set_estado
        # del Grupo.__progreso   #  Lo calculo en la prop de solo lectura
        # del Grupo.add_hito     #  Lo reemplazo para que trabaje con hijo
        # del Grupo.rem_hito     #  Lo reemplazo para que trabaje con hijo
        # del Grupo.get_hito     #  Lo reemplazo para que trabaje con hijo
        # del Grupo.lista_hitos  #  Lo reemplazo para que trabaje con hijo

    ############################   PROPIEDADES   ##########################

    @property
    def progreso(self):
        ''' Progreso expresado en porcentaje'''

        prog_total = 0
        prog_parcial = 0

        for h in self.lista_hijos():                        #  De todos los hijos del grupo
            if h.tipo != Tipo_hito:                         #  busco los que no son hitos (otros grupos y tareas)
                prog_total += 100                           #  y obtengo un valor total
                prog_parcial += h.progreso                  #  y un valor parcial

        prog = int(100 * float(prog_total)/prog_parcial)    #  Y calculo el porcentaje con esos valores

        return prog

    @property
    def estado(self):
        ''' Devuelve el estado '''

        # Calcular el estado segun los estados de los hijos
        pass

    ############################   METODOS   ##########################


    def crear_hito(self, nombre, t_plan, progreso=0):
        """ Crea un hito y lo agrega a la lista de hijos del grupo. 
            nombre: nombre del hito (str)
            t_plan: tiempo planificado (int)
            progreso: progreso que debe tener el padre para que el hito ocurra (int) """

        H = Hito(nombre, t_plan, progreso, self)  #  Hito creado para agregar

        self.add_hijo(H)                          #  Agrego el hito a la lista de hijos del grupo

        return H                                  #  Devuelvo el hito que acabo de crear

    def crear_tarea(self, nombre, inicio, duracion):
        ''' Crea una tarea y la agrega a la lista de hijos del grupo.
            nombre: nombre de la tarea (str)
            inicio: tiempo planificado para el hito de inicio(int)
            duracion: tiempo que durará la tarea según lo planificado (int) '''

        T = Tarea(nombre, inicio, duracion, self)  #  Tarea creada para agregar

        self.add_hijo(T)     #  Agrego la tarea hija

        return T     #  Devuelvo la tarea que acabo de crear

    def crear_grupo(self, nombre):
        ''' Crea un grupo vacío y lo agrego a la lista de hijos del grupo.
            nombre: nombre del grupo (str) '''

        G = Grupo(nombre, self)  #  Grupo creado para agregar

        self.add_hijo(G)         #  Agrego el grupo hijo

        return G                 #  Devuelvo el grupo que acabo de crear

    def add_hijo(self, hijo):
        """ Agrega un hijo a la lista de hijos del grupo.
            hijo: elemento a agregar (Grupo|Tarea|Hito) """

        if hijo.tipo == Tipo_proyecto or hijo.tipo == Tipo_diagrama :                #  Si el hijo no es de un tipo valido
            raise Tipo_no_valido(tipos_string(hijo.tipo))                            #  lanzo una excepcion

        if hijo.tipo == tipo_hito:                                                   #  Si el hijo que agrego es un hito
            if hijo.t_plan < self.inicio.t_plan or hijo.t_plan > self.fin.t_plan:    #  el t_plan del hijo debe estar dentro del grupo
                raise Tiempo_no_valido(hijo.t_plan)                                  #  de lo contrario lanzo una excepcion

        else:                                                                        #  En cambio, si no es un hito (entonces es una tarea u otro grupo)
            if self.duracion_plan == 0:                                              #  Si el grupo tiene duracion = 0 entonces es el primer hijo
                self.inicio._Hito__t_plan = hijo.inicio.t_plan                       #  y hago que empiece junto con el hijo
                self.fin._Hito__t_plan = hijo.fin.t_plan                             #  y termine tambien con el.

            else:                                                                    #  Si ya habian hijos la duracion es distinta de 0.
                if hijo.inicio.t_plan < self.inicio.t_plan:                          #  Si el hijo agregado empieza antes que el grupo
                    self.inicio._Hito__t_plan = hijo.inicio.t_plan                   #  extiendo el inicio del grupo hasta el inicio del hijo,

                if hijo.fin.t_plan > self.fin.t_plan:                                #  y si el hijo agregado termina despues del grupo
                    self.fin._Hito__t_plan = hijo.fin.t_plan                         #  extiendo el final del grupo hasta el final del hijo

        self.__hijos[hijo.id] = hijo                                                 #  Una vez que esta todo listo agrego el hijo a la lista de hijos

    def rem_hijo(self, id):
        """ Quita el hijo indicado de la lista de hijos del grupo.
            id: identificador del hijo a quitar """

        ###########    Volver a verificar la duracion del grupo y que hacer con
        ###########    los hitos que quedan fuera del grupo

        return self.__hijos.pop(id)

    def get_hijo(self, id):
        """ Retorna el hijo indicado.
            id: identificador del hijo a devolver """

        return self.__hijos[id]

    def lista_hijos(self):
        """ Devuelve una tupla con los hijos del grupo. """

        return tuple(self.__hijos.values())

    def set_estado(self, val_estado):
        ''' Establece el estado de ejecución de una tarea, grupo, diagrama o proyecto.
            val_estado: valor que debe tomar el estado (int) '''

    ########   Hacer que modifique todos los estados de sus hijos (grupos y tareas) tambien   #########
        pass


class Diagrama(Grupo):
    """ Clase que define un diagrama de Gantt """

    def __init__(self, nombre, proyecto=None):
        ''' nombre: nombre del diagrama (str)
            proyecto: proyecto al cual pertenece el diagrama (Proyecto|None) '''

        super(Diagrama, self).__init__(nombre, proyecto)

        self.__tipo = Tipo_diagrama

    ####################   PROPIEDADES   ####################

    @property
    def proyecto(self):
        """ Proyecto al cual pertenece el diagrama. Si proyecto=None se considera un diagrama huérfano. Es equivalente a la propiedad 'Diagrama.padre'. Solo lectura """

        return self.padre

    def set_proyecto(self, proyecto):
        """ Establece a que proyecto pertenece el diagrama. Para dejarlo huérfano se debe establecer a None.
            proyecto: proyecto que contendrá al diagrama (Proyecto|None) """

        if self.proyecto != None:
            # Eliminar este diagrama de la lista del proyecto anterior
            self.proyecto.rem_diagrama(self)

        self._Elemento__padre = proyecto



