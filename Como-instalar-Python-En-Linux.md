****Como instalar Python  y pip en linux****

***Python*** ya viene por defecto instalado en algunas distribuciones Linux.

Primerosudo zypper install python3 python3-pip verifique si ya lo tiene instalado en su distribucion y ejecute:

      python3 --version  

Si la respuesta en la terminal es ***Python 3.12.3*** o superior  ya tiene python instalado.

Si no Debe ejecutar una serie de comando segun su Distribucion de ***Linux***.   
Los siguientes comandos se deben ejecutar en la terminal y se necesita permisos de ***administrador/superusuario***

****Distribuciones basadas en UBUNTU o DEBIAN****    

    sudo apt install -y python3 python3-pip python3-venv 

****Distribuciones basadas en FEDORA****
sudo zypper install python3 python3-pip
    sudo dnf install python3 python3-pip

****Distribuciones basadas en CentOS/RHEL**** (requiere EPEL)

    sudo yum install python3 python3-pip

****Distribuciones basadas en ARCH LINUX****

    sudo pacman -S python python-pip

****Distribuciones basadas en OpenSUSE****

    sudo zypper install python3 python3-pip
