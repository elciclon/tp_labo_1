#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grupo: NAN
Integrantes: Rozas Chavez, Antuanette Carolina
             Madril, Joaquin Leandro
             Fernández Fazio, Adrián Patricio
             
Este archivo incluye todo el código para recolectar los datos desde las instituciones,
limpiarlos, y responder a los requerimientos de la consigna.

"""
import pandas as pd

instituciones = pd.read_excel('instituciones_de_salud.xlsx')

#%% Eliminar columnas innecesarias

instituciones = instituciones.drop(['localidad_id', 
                                    'localidad_nombre', 
                                    'codloc',
                                    'codent',
                                    'tipologia_id',
                                    'tipologia_sigla',
                                    'cp',
                                    'domicilio',
                                    'sitio_web',
                                    'establecimiento_nombre'], axis=1)
#%% Asginamos TRUE a los que tienen terapia, FALSE al resto
for i in instituciones.index:
    if 'terapia' in str(instituciones.loc[i, 'tipologia_nombre']).lower():
        instituciones.loc[i, 'tipologia_nombre'] = True
    else:
        instituciones.loc[i, 'tipologia_nombre'] = False


instituciones.columns