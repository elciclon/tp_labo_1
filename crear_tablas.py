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

censo_2010 = pd.read_csv('censo_2010_limpio.csv')
censo_2022 = pd.read_csv('censo_2022_limpio.csv')
defunciones = pd.read_csv('defunciones_limpio.csv')
instituciones = pd.read_csv('instituciones_limpio.csv')


#%% Creamos la estructura de tablas

