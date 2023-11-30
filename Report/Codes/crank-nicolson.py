import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.rcParams['text.usetex'] = True

# parâmetros
k = 6.3     # difusividade térmica (m^2/year)
L = 15.0    # profundidade máxima na integração
T = 1.0     # tempo total de integração (em anos)
Nx = 150    # quantidade de pontos espaciais
Nt = 1260   # quantidade de timesteps
dx = L / Nx
dt = T / Nt

# condições de contorno (começando com inverno)
def f(t):
    if (0 <= t <= 0.5):
        f = 1
    elif (0.5 < t <= 1):
        f = 10
    return f

def right_boundary_condition(t, x):
    return np.zeros_like(x)

# condição inicial
def initial_condition(t, x):
    return f(t) * np.exp(-0.71 * x)

# solver do sistema linear, usando o algoritmo de Thomas
def tdma_solver(a:np.ndarray, b:np.ndarray, c:np.ndarray, d:np.ndarray) -> np.ndarray:
    """
    Resolve um sistema de equações lineares tridiagonal usando o algoritmo de Thomas.

    Argumentos:
    a: array, coeficientes da diagonal inferior (comprimento Nx-1)
    b: array, coeficientes da diagonal principal (comprimento N)
    c: array, coeficientes da diagonal superior (comprimento N-1)
    d: array, lado direito do sistema (comprimento N)

    Retorna:
    x: array, vetor solução de comprimento N
    """

    N = len(b)
    c_linha = np.zeros(N - 1)
    d_linha = np.zeros(N)

    c_linha[0] = c[0] / b[0]
    d_linha[0] = d[0] / b[0]

    for i in range(1, N - 1):
        c_linha[i] = c[i] / (b[i] - a[i - 1] * c_linha[i - 1])
    for i in range(1, N):
        d_linha[i] = (d[i] - a[i - 1] * d_linha[i - 1]) / (b[i] - a[i - 1] * c_linha[i - 1])

    # substituição de trás para frente (o terceiro -1 no argumento do range indica iteração com passo negativo: começamos em N-2 e vamos até 0)
    x = np.zeros(N)
    x[-1] = d_linha[-1]
    for i in range(N - 2, -1, -1):
        x[i] = d_linha[i] - c_linha[i] * x[i + 1]

    return x

# função para fazer a animação
def update(frame):
    line.set_ydata(frames[frame])
    time = (frame + 1) * dt
    timer_text.set_text(f't = {time:.2f} anos')
    return line, timer_text


# criação da malha espacial
x_values = np.linspace(0, L, Nx+1)

u = initial_condition(0, x_values)

frames = []

specific_times = [0, 0.25, 0.5, 0.75, 1.0]
specific_frames = []

alpha = k * dt / (2 * dx**2)

time_values = []

# aplicando o método de Crank-Nicolson
for n in range(Nt):
    u_new = np.zeros_like(u)
    
    # aplicando as condições de contorno
    u_new[0] = f((n+1) * dt)
    u_new[-1] = right_boundary_condition((n+1) * dt, x_values)[-1]

    # resolvendo o sistema com o algoritmo de Thomas
    u_interior = u[1:Nx]
    b = u_interior + alpha * (u[2:Nx+1] - 2 * u_interior + u[:Nx-1])
    b[0] += alpha * f((n+1) * dt)
    b[-1] += alpha * right_boundary_condition((n+1) * dt, x_values)[1]

    lower_diag = np.full(Nx - 2, -alpha)
    main_diag = np.full(Nx - 1, 1 + 2 * alpha)
    upper_diag = np.full(Nx - 2, -alpha)

    u_new[1:Nx] = tdma_solver(lower_diag, main_diag, upper_diag, b)

    # salvando a solução para fazer a animação
    u = u_new.copy()
    frames.append(u.copy())
    time_values.append(n*dt)
    
    # salvando a solução para fazer a figura
    if (n * dt) in specific_times:
        print(n*dt)
        specific_frames.append(u.copy())

# append para pegar a última iteração temporar (t=1)
specific_frames.append(u.copy())

# criando a animação
fig, ax = plt.subplots()
line, = ax.plot(x_values, frames[0], label='')
plt.title('Perfil de temperatura')
plt.xlabel('Profundidade')
plt.ylabel('Temperatura')
plt.legend()
plt.grid(True)

ax.set_ylim(0, 10)

ax.axvline(x=4.4, color='red', linestyle='--', label='')
ax.axhline(y=1, color='green', linestyle='--', label='')

timer_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

ani = FuncAnimation(fig, update, frames=len(frames), interval=50)

ani.save('crank-nicolson.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# criando a figura
plt.figure(figsize=(8, 6))

for i, time in enumerate(specific_times):
    plt.plot(x_values, specific_frames[i], label=f't = {time} anos')

plt.axvline(x=4.4, color='red', linestyle='--', label='')
plt.axhline(y=1, color='green', linestyle='--', label='')

plt.title('Perfil de temperatura')
plt.xlabel('Profundidade')
plt.ylabel('Temperatura')
plt.legend()
plt.grid(True)

plt.savefig('crank-nicolson.pdf', bbox_inches='tight')

with open('crank-nicolson.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['tempo', 'temperatura'])
    for time, frame in zip(time_values, frames):
        writer.writerow([time] + frame.tolist())