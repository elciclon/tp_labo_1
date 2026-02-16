#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
Este archivo incluye todo el código para crear las tablas a partir de los 
documentos provistos ya saneados, y responder a los requerimientos de la 
consigna.

"""

#%% Cargamos archivos saneados
import pandas as pd

censo_2010 = pd.read_csv('censo_2010_limpio.csv', index_col=0)
censo_2022 = pd.read_csv('censo_2022_limpio.csv', index_col=0)
defunciones = pd.read_csv('defunciones_limpio.csv')
instituciones = pd.read_csv('instituciones_limpio.csv', index_col=0)


#%% Creamos la estructura de tablas

provincia = pd.DataFrame(columns= ['id_provincia', 'nombre'])

provincia = provincia.set_index('id_provincia')

defuncion = defunciones

defuncion = defuncion.set_index(['id_provincia', 'causa', 'rango', 'sexo', 'año'])

grupoPoblacional = pd.DataFrame(columns= ['id_provincia', 'rango', 'sexo', 'año', 'tiene_cobertura', 'cantidad'])

grupoPoblacional = grupoPoblacional.set_index(['id_provincia', 'rango', 'sexo', 'año', 'tiene_cobertura'])

departamento = pd.DataFrame(columns= ['id_departamento', 'nombre', 'id_provincia'])

departamento = departamento.set_index('id_departamento')

establecimiento = pd.DataFrame(columns= ['id_establecimiento', 'financiamiento', 'tiene_terapia', 'id_departamento'])

establecimiento = establecimiento.set_index('id_establecimiento')
