import os
import subprocess
import sys
import venv

def main():
    venv_dir = "venv"
    
    # 1. Crear entorno virtual automáticamente si no existe
    if not os.path.exists(venv_dir):
        print("Creando el entorno virtual (venv)...")
        venv.create(venv_dir, with_pip=True)
        print("Entorno virtual creado exitosamente.")
    else:
        print("El entorno virtual ya existe.")

    # Determinar rutas según el sistema operativo (Windows o Linux)
    if os.name == "nt":
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_executable = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_executable = os.path.join(venv_dir, "bin", "python")
        pip_executable = os.path.join(venv_dir, "bin", "pip")

    # 2. Instalar dependencias automáticamente
    if os.path.exists("requirements.txt"):
        print("Instalando dependencias desde requirements.txt...")
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"], check=True)
    else:
        print("Instalando PySide6...")
        subprocess.run([pip_executable, "install", "PySide6"], check=True)
    print("Dependencias listas.")

    # 3. Ejecutar Stocky
    script_principal = "Stocky-GUI.py"
    if os.path.exists(script_principal):
        print(f"Iniciando {script_principal}...")
        os.execv(python_executable, [python_executable, script_principal])
    else:
        print(f"Error: No se encuentra el archivo {script_principal}.")

if __name__ == "__main__":
    main()
