import simpy
import random
import numpy as np
RANDOM_SEED = 25
CPU_INSTRUCCIONES = 3 #modificable
NUM_PROCESOS = 25 #Modificable
interval = 10 #Modificable

#Donde se generan los procesos aleatoriamente y se siguen hasta que llegue a NUM_PROCESOS
def proceso(env, ram, cpu, tiempos):
    for i in range(NUM_PROCESOS):
        e = ejecucion(env,'proceso%02d' % i, ram, cpu, tiempos)
        env.process(e)
        t = random.expovariate(1/interval)
        yield env.timeout(t)


def ejecucion(env, nombre, ram, cpu, tiempos):
    llegada = env.now
    usar_ram = random.randint(1,10)
    proceso_instrucciones = random.randint(1,10)
    yield ram.get(usar_ram)
    estado = ""
    while estado != "terminated":
        #Ejecutar un proceso en la CPU
        with cpu.request() as req_cpu:
            yield req_cpu
            yield env.timeout(1)  
            if(proceso_instrucciones>=CPU_INSTRUCCIONES):
                proceso_instrucciones -= CPU_INSTRUCCIONES
            else:
                proceso_instrucciones -= proceso_instrucciones
        if proceso_instrucciones == 0:
            estado = "terminated"
            print(nombre, "se tardó:", (env.now-llegada))
            tiempos.append(env.now - llegada)
            yield ram.put(usar_ram)
        else:
            if random.randint(1,2) == 1:
                estado = "waiting"
                yield env.timeout(1)
            else:
                estado = "ready"
        

#Inicialización de la simulación
env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1) #La capacity muestra el número de procesadores
tiempos = []
random.seed(RANDOM_SEED)


env.process(proceso(env, RAM, CPU, tiempos))
env.run()

print("Tiempo promedio para " + str(NUM_PROCESOS) + " procesos con " + str(interval) + " intervalos: " + str(np.mean(tiempos)))
print("Desviación estándar para " + str(NUM_PROCESOS) + " procesos con " + str(interval) + " intervalos: " + str(np.std(tiempos)))


