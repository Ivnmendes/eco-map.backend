# eco-map.backend

comandos para iniciar

~~~bash
# criar o ambiente virtual e ativar
py -m venv ./venv
source ./venv/bin/activate

# instalar dependencias
pip install -r requirements.txt

# rodar
python manage.py startapp nomeDoApp
~~~

~~~sql
# criar banco
createdb eco_ponto_db
psql eco_ponto_db
CREATE USER eco_user WITH PASSWORD 'senha';
GRANT ALL PRIVILEGES ON DATABASE eco_ponto_db TO eco_user;
~~~

~~~bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~
