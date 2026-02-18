import subprocess

def correr_scripts():
    scripts = ["limpiar_censos.py", 
               "limpiar_defunciones.py", 
               "limpiar_instituciones.py",
               "crear_tablas.py",
               "consultas_SQL.py"]
    for script in scripts:
        print(f"---Ejecutando {script}---")
        try:
            subprocess.run(["python3", script], check=True)
            print(f"{script} terminó exitosamente\n")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {script}: {e}\n")
            break
        
if __name__ == "__main__":
    correr_scripts()