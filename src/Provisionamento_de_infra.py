import docker


class Infra(object):
    def __init__(self):
          self.client = docker.from_env()
        
    def gerenciador_container(self):
        print('Criando volume container')
        volume = self.client.volumes.create(name='portainer_data_01')
        print('Criando gerenciador do container')
        self.gerenciador_container = self.client.containers.run("portainer/portainer-ce", 
                            name="gerenciador_container",
                            ports={"8000/tcp":8000,"9000/tcp":9000},
                            restart_policy={"Name": "always"},
                            volumes=['/var/run/docker.sock:/var/run/docker.sock','portainer_data_01:/data'],            
                            detach=True)
        

    def banco_nosqgl_mongodb(self):
        print('Criando NoSQL Database')
        self.banco_dados = self.client.containers.run("mongo:latest", 
                            name="banco_nosqgl_mongodb",
                            ports={"27017/tcp":27017},
                            restart_policy={"Name": "always"},
                            detach=True)
        
    def sgbd_metabase(self):
        print('Criando SGBD Metabase')
        self.sgbd_metabase = self.client.containers.run("metabase/metabase", 
                            name="sgbd_metabase",
                            ports={"3000/tcp":3000},
                            restart_policy={"Name": "always"},
                            detach=True)
                          

    def banco_sql_mysql(self):
        print('Criando Banco Relacional MySQL')
        acessos_sql = {'MYSQL_ROOT_PASSWORD':'RootPassword', 'MYSQL_DATABASE':'Backoffice', 'MYSQL_USER':'MainUser', 'MYSQL_PASSWORD':'MainPassword'}
        self.banco_dados_sql = self.client.containers.run("mysql:latest", 
                            name="banco_sql_mysql",
                            ports={"3306/tcp":3306},
                            restart_policy={"Name": "always"},
                            environment = acessos_sql,
                            detach=True)
              

    def orquestrador_pipeline(self):
        print('Criando Elyra para pipeline')
        self.elyra = self.client.containers.run("elyra/elyra:dev", 
                            user="root",
                            environment=["GRANT_SUDO=yes"],
                            command="jupyter lab --debug --allow-root",
                            name="elyra",
                            ports={"8888/tcp":8888},
                            detach=True)

    def list_containers(self):
        return {
            "container_ids":self.client.containers.list(),
            "elyra-container": self.elyra,
            "metabase-container": self.sgbd_metabase,
            "mongodb-container": self.banco_dados,
            "mysql-container": self.banco_dados_sql,
            "portainer-container": self.gerenciador_container
        }  

      
class Model(object):
    def __init__(self):
        self.infra = Infra()
    def apply(self):
        self.infra.gerenciador_container()
        self.infra.banco_nosqgl_mongodb()
        self.infra.banco_sql_mysql()
        self.infra.sgbd_metabase()
        self.infra.orquestrador_pipeline()
        
    def destroy(self):
        # passar um for para derrubar os containers 
        # container.remove(force=True)
        return self.infra.list_containers()
 

def main():
    model = Model()
    model.apply()
    
if __name__ == "__main__":
    main()