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


defuncion = defunciones

defuncion = defuncion.set_index(['id_provincia', 'causa', 'rango', 'sexo', 'año'])



#%% Populamos provincia

provincia['id_provincia'] = instituciones['provincia_id']
provincia['nombre'] = instituciones['provincia_nombre']
provincia = provincia.drop_duplicates()
provincia = provincia.set_index('id_provincia')

#%% Populamos grupoPoblacional

censo_2010['año'] = 2010
censo_2022['año'] = 2022
grupoPoblacional = pd.concat([censo_2010, censo_2022])
grupoPoblacional = grupoPoblacional.reset_index(drop=True)


provincias_dict = {}
for e in provincia.itertuples():
    provincias_dict[str(e.nombre).lower()] = e.Index

for i in grupoPoblacional.index:
    grupoPoblacional.loc[i, 'provincia'] = provincias_dict[str(grupoPoblacional.loc[i, 'provincia']).lower()]
    
grupoPoblacional.rename(columns={"provincia": "id_provincia", 
                             "cobertura": "tiene_cobertura",                                                 
                      }, inplace=True)
grupoPoblacional = grupoPoblacional[['id_provincia', 'rango', 'sexo', 'año', 'tiene_cobertura', 'cantidad']]
grupoPoblacional = grupoPoblacional.set_index(['id_provincia', 'rango', 'sexo', 'año', 'tiene_cobertura'])
#%% Populamos departamento
departamento = instituciones
departamento = departamento.drop(['establecimiento_id',
                  'provincia_nombre',
                  'origen_financiamiento',
                  'tiene_terapia'], axis=1
                  )
departamento = departamento.rename(columns={"provincia_id": "id_provincia",
                             "departamento_nombre": "nombre",
                             "departamento_id": "id_departamento"})
departamento = departamento[['id_provincia', 'id_departamento', 'nombre']]
departamento.drop_duplicates(inplace=True, ignore_index=True)
departamento = departamento.set_index(['id_provincia', 'id_departamento'])
#%% Populamos establecimiento
establecimiento = pd.DataFrame(columns= ['id_establecimiento', 'financiamiento', 'tiene_terapia', 'id_departamento'])
establecimiento = instituciones
establecimiento = establecimiento.drop(['provincia_nombre',
                                        'departamento_nombre',
                                        
                  ], axis=1
                  )
establecimiento = establecimiento.rename(columns={"establecimiento_id": "id_establecimiento",
                                                  "origen_financiamiento": "financiamiento",
                                                  "departamento_id": "id_departamento", "provincia_id": "id_provincia"})
establecimiento = establecimiento[['id_establecimiento', 'financiamiento', 'tiene_terapia', 'id_departamento', 'id_provincia']]
establecimiento = establecimiento.set_index('id_establecimiento')
#%% Exportamos todas las tablas a csv
provincia.to_csv('provincia.csv')
defuncion.to_csv('defuncion.csv')
grupoPoblacional.to_csv('grupoPoblacional.csv')
departamento.to_csv('departamento.csv')
establecimiento.to_csv('establecimiento.csv')