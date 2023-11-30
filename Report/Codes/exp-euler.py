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

# condição inicial (começando com inverno)
def f(t):
    if (0 <= t <= 0.5):
        f = 1
    elif (0.5 < t <= 1):
        f = 10
    return f

# condições de contorno
def initial_condition(t, x):
    return f(t) * np.exp(-0.71 * x)

def right_boundary_condition(t, x):
    return np.zeros_like(x)

# função para fazer a animação
def update(frame):
    line.set_ydata(frames[frame])
    time = (frame + 1) * dt  # Calculate current time
    timer_text.set_text(f't = {time:.2f} anos')
    return line, timer_text

# criação da malha espacial
x_values = np.linspace(0, L, Nx+1)

u = initial_condition(0, x_values)

frames = []

specific_times = [0, 0.25, 0.5, 0.75, 1.0]
specific_frames = []

# aplicando o esquema de Euler explícito
for n in range(Nt):
    u_new = np.zeros_like(u)
    
    # aplicando as condições de contorno
    u_new[0] = f((n+1) * dt)
    u_new[-1] = right_boundary_condition((n+1) * dt, x_values)[-1]
    
    for i in range(1, Nx):
        u_new[i] = u[i] + k * dt * (u[i+1] - 2 * u[i] + u[i-1]) / (dx**2)
    
    # salvando a solução para fazer a animação
    u = u_new.copy()
    frames.append(u.copy())
    
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

ax.set_ylim(0,10)

ax.axvline(x=4.4, color='red', linestyle='--', label='x = 4.4')
ax.axhline(y=1, color='green', linestyle='--', label='y = 1')

timer_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

ani = FuncAnimation(fig, update, frames=len(frames), interval=50)

ani.save('exp-euler.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

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

plt.savefig('exp-euler.pdf', bbox_inches='tight')