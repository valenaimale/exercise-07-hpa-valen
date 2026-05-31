import random                          # para generar nombres de nodos unicos y evitar duplicados
from locust import HttpUser, task, between  # HttpUser: usuario virtual que hace requests HTTP
                                            # task: decorador que marca una funcion como tarea de carga
                                            # between: genera un tiempo de espera aleatorio entre dos valores

class NodeApiUser(HttpUser):           # cada instancia de esta clase simula UN usuario concurrente
    wait_time = between(1, 3)          # entre tarea y tarea, el usuario espera entre 1 y 3 segundos (simula comportamiento real)

    @task(3)                           # peso 3: esta tarea se ejecuta 3 veces mas que una de peso 1
    def health_check(self):            # simula un cliente que consulta el estado de la app
        self.client.get("/health")     # hace GET /health — el endpoint mas liviano, genera carga base constante

    @task(2)                           # peso 2: se ejecuta con frecuencia media
    def list_nodes(self):              # simula un cliente que lista los nodos registrados
        self.client.get("/api/nodes")  # hace GET /api/nodes — consulta la base de datos, genera mas carga que /health

    @task(1)                           # peso 1: se ejecuta con menor frecuencia (es la operacion mas costosa)
    def create_node(self):             # simula un cliente que registra un nuevo nodo
        node_name = f"node-{random.randint(1, 100000)}"  # nombre aleatorio para evitar el error 409 (nodo ya existe)
        self.client.post(              # hace POST /api/nodes con un body JSON
            "/api/nodes",
            json={
                "name": node_name,     # campo requerido por NodeCreate en schemas.py
                "host": "192.168.1.1", # host del nodo que se esta registrando
                "port": 8080,          # puerto valido (entre 1 y 65535, definido en schemas.py)
            },
        )
