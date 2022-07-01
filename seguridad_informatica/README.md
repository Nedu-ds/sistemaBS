# Division de seguridad de la Informacion

--By Nedu--

Python Framework Flask

-----
Instalar sshpass

Debian

apt install sshpass

RHEL
yum install sshpass

-----
Clonar repositorio

sshpass -p [password] git clone -l -s -n ssh://[user]@[host]:[port]/path_repo/.git  path_destino
git checkout master

------
Ambiente virtual

------
Instalar python

yum install python38
yum install venv

apt install python38
apt install venv

venv -> phyton 3.5 o superior

------
Crear ambient virtual

python3 -m venv nombre-venv
cd nombre-venv/bin/activate  -> para activar
pip3 install -r requirements.txt

---------
Ejecucion de la aplicacion

python3 main.py
