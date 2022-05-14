import docker

client = docker.from_env()
print('Criando volume container')

volume = client.volumes.create(name='portainer_data_01')
print('Criando gerenciador do container')

gerenciador_container = client.containers.run("portainer/portainer-ce", 
                         name="gerenciador_container",
                         ports={"8000/tcp":8000,"9000/tcp":9000},
                         restart_policy={"Name": "always"},
                         volumes=['/var/run/docker.sock:/var/run/docker.sock','portainer_data_01:/data'],            
                         detach=True)

print('Criando NoSQL Database')
banco_dados = client.containers.run("mongo:latest", 
                         name="banco_nosqgl_mongodb",
                         ports={"27017/tcp":27017},
                         restart_policy={"Name": "always"},
                         detach=True)

print('Criando SGBD Metabase')
gerenciador_banco = client.containers.run("metabase/metabase", 
                         name="sgbd_metabase",
                         ports={"3000/tcp":3000},
                         restart_policy={"Name": "always"},
                         detach=True)

print('Criando Banco Relacional MySQL)
acessos_sql = {'MYSQL_ROOT_PASSWORD':'RootPassword', 'MYSQL_DATABASE':'Backoffice', 'MYSQL_USER':'MainUser', 'MYSQL_PASSWORD':'MainPassword'}
banco_dados_sql = client.containers.run("mysql:latest", 
                         name="banco_sql_mysql",
                         ports={"3306/tcp":3306},
                         restart_policy={"Name": "always"},
                         environment = acessos_sql,
                         detach=True)

print('Criando Elyra para pipeline)
elyra = client.containers.run("elyra/elyra:dev", 
                         user="root",
                         environment=["GRANT_SUDO=yes"],
                         command="jupyter lab --debug --allow-root",
                         name="elyra",
                         ports={"8888/tcp":8888},
                         detach=True)
      
      
print('Lista de containers')
lista_de_containers = client.containers.list()
print(lista_de_containers)