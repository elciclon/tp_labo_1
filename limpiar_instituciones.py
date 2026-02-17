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
instituciones = instituciones.rename(columns={"tipologia_nombre": "tiene_terapia"})

#%% Simplificamos tipo de financiamiento a Público o Privado
for i in instituciones.index:
    financiamiento = str(instituciones.loc[i, 'origen_financiamiento']).lower()
    if ('privado' in financiamiento) or (financiamiento in ['obra social', 'mutual','otros']):
        instituciones.loc[i, 'origen_financiamiento'] = 'privado'
    else:
        instituciones.loc[i, 'origen_financiamiento'] = 'estatal'
        
    
#%%

instituciones[
    instituciones['departamento_nombre'].isin(['LA CAPITAL', 'CAPITAL'])
    ][['departamento_nombre', 'provincia_nombre']].value_counts()    

    
#%% Hay dos IDs para la misma provincia
instituciones.loc[instituciones['provincia_id'] == 86, 'provincia_id'] = 22
instituciones.loc[instituciones['provincia_id'] == 62, 'provincia_id'] = 26
instituciones.loc[instituciones['provincia_id'] == 66, 'provincia_id'] = 14
instituciones.loc[instituciones['provincia_id'] == 50, 'provincia_id'] = 74
instituciones = instituciones.drop(18445)
#%% Guardamos el archivo
instituciones.to_csv('instituciones_limpio.csv')
