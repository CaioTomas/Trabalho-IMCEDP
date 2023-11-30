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

# criação da malha espacial
x_values = np.linspace(0, L, Nx+1)

u = initial_condition(0, x_values)

frames = []

specific_times = [0, 0.25, 0.5, 0.75, 1.0]
specific_frames = []

alpha = k * dt / (2 * dx**2)

# contruindo matriz (tridiagonal) dos coeficientes
A = np.diag(1 + 2 * alpha * np.ones(Nx-1)) + \
    np.diag(-alpha * np.ones(Nx-2), k=1) + \
    np.diag(-alpha * np.ones(Nx-2), k=-1)

# aplicando o método de Crank-Nicolson
for n in range(Nt):
    u_new = np.zeros_like(u)
    
    # aplicando as condições de contorno
    u_new[0] = f((n+1) * dt)
    u_new[-1] = right_boundary_condition((n+1) * dt, x_values)[-1]

    # Update inner points using matrix inversion
    u_interior = u[1:Nx]  # Interior points
    b = u_interior + alpha * (u[2:Nx+1] - 2 * u_interior + u[:Nx-1])
    b[0] += alpha * f((n+1) * dt)
    b[-1] += alpha * right_boundary_condition((n+1) * dt, x_values)[1]

    u_new[1:Nx] = np.linalg.solve(A, b)

    u = u_new.copy()
    frames.append(u.copy())
    
    if (n * dt) in specific_times:
        print(n*dt)
        specific_frames.append(u.copy())

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

def update(frame):
    line.set_ydata(frames[frame])
    time = (frame + 1) * dt  # Calculate current time
    timer_text.set_text(f't = {time:.2f} anos')
    return line, timer_text

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