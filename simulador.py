import simpy
import random
import numpy as np
RANDOM_SEED = 28
CPU_INSTRUCCIONES = 3 #modificable
NUM_PROCESOS = 25 #Modificable
interval = 10 #Modificable

#Donde se generan los procesos aleatoriamente y se siguen hasta que se terminen
def proceso(env, ram, cpu, tiempos):
    #Hasta que el mismo número de procesos sea el de terminados, se acaba la simulación
    for i in range(NUM_PROCESOS):
        e = ejecucion(env, ram, cpu, tiempos)
        env.process(e)
        t = random.expovariate(1/interval)
        yield env.timeout(t)

def ejecucion(env, ram, cpu, tiempos):
    global terminated
    usar_ram = random.randint(1,10)
    proceso_instrucciones = random.randint(1,10)    
    llegada = env.now
    #Si se obtiene memoria, se pasa al estado de ready, de lo contrario sigue esperando hasta que pueda reicbir memoria
    with ram.get(usar_ram) as req:
        yield req
        while proceso_instrucciones > 0:
            #Ejecutar un proceso en la CPU
            with cpu.request() as req_cpu:
                yield req_cpu
                yield env.timeout(1)  
                if(proceso_instrucciones>=CPU_INSTRUCCIONES):
                    proceso_instrucciones -= CPU_INSTRUCCIONES
                else:
                    proceso_instrucciones -= proceso_instrucciones
            
            #Estado terminated
            if proceso_instrucciones == 0:
                terminated = "Terminad"
            else:
                #Estado waiting
                if random.randint(1, 2) == 1:
                    yield env.timeout(1)
                #Estado ready
                else:
                    continue
        yield ram.put(usar_ram)
        tiempos.append(env.now - llegada)

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


