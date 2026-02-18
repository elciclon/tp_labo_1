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
#%% Cargamos las tablas

import pandas as pd
import duckdb as dd

provincia = pd.read_csv('provincia.csv')
defuncion = pd.read_csv('defuncion.csv')
grupoPoblacional = pd.read_csv('grupoPoblacional.csv')
departamento = pd.read_csv('departamento.csv')
establecimiento = pd.read_csv('establecimiento.csv')

#%% EJERCICIO I

cantidadConCobertura2010 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2010 AND gp.tiene_cobertura = True
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadConCobertura2010 = dd.sql(cantidadConCobertura2010).df()

cantidadSinCobertura2010 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2010 AND gp.tiene_cobertura = False
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadSinCobertura2010 = dd.sql(cantidadSinCobertura2010).df()

cantidadConCobertura2022 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2022 AND gp.tiene_cobertura = True
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadConCobertura2022 = dd.sql(cantidadConCobertura2022).df()

cantidadSinCobertura2022 = """

                            SELECT p.nombre, gp.rango, SUM(gp.cantidad) AS cantidad
                            FROM provincia AS p JOIN grupoPoblacional AS gp
                            ON p.id_provincia = gp.id_provincia
                            WHERE gp.año = 2022 AND gp.tiene_cobertura = False
                            GROUP BY p.nombre, gp.rango

                            """
              
cantidadSinCobertura2022 = dd.sql(cantidadSinCobertura2022).df()

coberturaDeSalud = """

                    SELECT DISTINCT c1.nombre AS Provincia, c1.rango AS 'Grupo etario',
                    c1.cantidad AS 'Habitantes con Cobertura en 2010',
                    s1.cantidad AS 'Habitantes sin Cobertura en 2010',
                    c2.cantidad AS 'Habitantes con Cobertura en 2022',
                    s2.cantidad AS 'Habitantes sin Cobertura en 2022'
                    FROM cantidadConCobertura2010 AS c1 JOIN cantidadSinCobertura2010 AS s1
                    ON c1.nombre = s1.nombre AND c1.rango = s1.rango
                    JOIN cantidadConCobertura2022 AS c2 
                    ON c1.nombre = c2.nombre AND c1.rango = c2.rango
                    JOIN cantidadSinCobertura2022 AS s2
                    ON c1.nombre = s2.nombre AND c1.rango = s2.rango

                    """
                    
coberturaDeSalud = dd.sql(coberturaDeSalud).df()

#%% EJERCICIO II

establecimientosConTerapiaIntensiva = """
                SELECT p.nombre AS Provincia, COUNT(*) as 'Cantidad de Establecimientos de Salud',
                e.financiamiento as 'Tipo de Financiamiento'
                FROM provincia AS p JOIN establecimiento AS e
                ON p.id_provincia = e.id_provincia
                WHERE tiene_terapia = True
                GROUP BY p.nombre, e.financiamiento
              """
              
establecimientosConTerapiaIntensiva = dd.sql(establecimientosConTerapiaIntensiva).df()

#%% EJERCICIO III

causasDeMuerteAux = """
                SELECT d.rango, d.sexo, d.causa, 
                SUM(d.cantidad) AS Total
                FROM defuncion AS d 
                GROUP BY d.causa, d.rango, d.sexo
                ORDER BY SUM(d.cantidad)
        
              """

causasDeMuerteAux = dd.sql(causasDeMuerteAux).df()

causasDeMuerteMasFrecuentes = """
                SELECT ca.rango AS 'Grupo etario', ca.sexo,
                ca.causa AS 'Categoría de Defunción', ca.total
                FROM (SELECT * 
                      FROM causasDeMuerteAux
                      ORDER BY total DESC
                      LIMIT 5
                      ) AS ca
                ORDER BY ca.rango, ca.sexo
        
              """

causasDeMuerteMenosFrecuentes = """
                SELECT ca.rango AS 'Grupo etario', ca.sexo,
                ca.causa AS 'Categoría de Defunción', ca.total
                FROM (SELECT * 
                      FROM causasDeMuerteAux
                      LIMIT 5
                      ) AS ca
                ORDER BY ca.rango, ca.sexo
        
              """

causasDeMuerteMenosFrecuentes = dd.sql(causasDeMuerteMenosFrecuentes).df()
causasDeMuerteMasFrecuentes = dd.sql(causasDeMuerteMasFrecuentes).df()

#%% EJERCICIO IV

personasPorProvinciayRango2022 = """
            SELECT id_provincia, rango, SUM(cantidad) AS 'Cantidad'
            FROM grupoPoblacional
            WHERE año = 2022
            GROUP BY id_provincia, rango
            
            """
personasPorProvinciayRango2022 = dd.sql(personasPorProvinciayRango2022).df()


muertesPorProvinciayRango2022 = """
            SELECT id_provincia, rango, SUM(cantidad) AS 'Cantidad'
            FROM defuncion
            WHERE año = 2022
            GROUP BY id_provincia, rango
            
            """
muertesPorProvinciayRango2022 = dd.sql(muertesPorProvinciayRango2022).df()

tasaDeMortalidad = """
            SELECT p.nombre AS Provincia, ppr.rango AS 'Grupo Etario', 
            (mpr.cantidad / ppr.cantidad) * 1000 AS 'Tasa de Mortalidad'
            FROM provincia AS p JOIN personasPorProvinciayRango2022 AS ppr
            ON p.id_provincia = ppr.id_provincia 
            LEFT OUTER JOIN muertesPorProvinciayRango2022 AS mpr
            ON p.id_provincia = mpr.id_provincia AND ppr.rango = mpr.rango
            """
        
tasaDeMortalidad = dd.sql(tasaDeMortalidad).df()

#%% EJERCICIO V

cantidadDeDefuncionesPorCategoria2010 = """
                                SELECT causa, SUM(cantidad) AS Cantidad
                                FROM defuncion
                                WHERE año = 2010
                                GROUP BY causa
                                """
                           
cantidadDeDefuncionesPorCategoria2010 = dd.sql(cantidadDeDefuncionesPorCategoria2010).df()

cantidadDeDefuncionesPorCategoria2022 = """
                                SELECT causa, SUM(cantidad) AS Cantidad
                                FROM defuncion
                                WHERE año = 2022
                                GROUP BY causa
                                """
                                
cantidadDeDefuncionesPorCategoria2022 = dd.sql(cantidadDeDefuncionesPorCategoria2022).df()

cambiosEnLasCausasDeDefuncion = """
                        SELECT c22.causa AS 'Categoría de Defunción',
                        ABS(c22.cantidad - CASE WHEN c10.cantidad IS NULL THEN 0 ELSE c10.cantidad END) AS Diferencia
                        FROM cantidadDeDefuncionesPorCategoria2022 AS c22
                        LEFT OUTER JOIN cantidadDeDefuncionesPorCategoria2010 AS c10
                        ON c22.causa = c10.causa
                        ORDER BY Diferencia DESC
                        """
                        
cambiosEnLasCausasDeDefuncion = dd.sql(cambiosEnLasCausasDeDefuncion).df()