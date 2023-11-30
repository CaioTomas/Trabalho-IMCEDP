import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

plt.rcParams['text.usetex'] = True

# parâmetros
L = 15.0    # profundidade máxima na integração
T = 1.0     # tempo total de integração (em anos)
Nx = 150    # quantidade de pontos espaciais
dx = L / Nx
alpha_values = [1, 2]

# difusividade variável (no espaço)
def thermal_diffusivity(x, a):
    diffusivity = (6.3 + x)**a
    return diffusivity

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

Nt_values = [5e3, 1e5]

for i in range(len(alpha_values)):
        
    # criação da malha espacial
    x_values = np.linspace(0, L, Nx+1)
    u = initial_condition(0, x_values)

    Nt = int(Nt_values[i])
    a = alpha_values[i]
    dt = T / Nt
    
    print(f'alpha={a}')
        
    for n in tqdm(range(Nt)):
        u_new = np.zeros_like(u)
        
        # aplicando as condições de contorno
        u_new[0] = f((n+1) * dt)
        u_new[-1] = right_boundary_condition((n+1) * dt, x_values)[-1]

        for i in range(1, Nx):
            k_imh = thermal_diffusivity(x_values[i - 1], a)
            k_iph = thermal_diffusivity(x_values[i], a)
            k_i = 0.5 * (k_imh + k_iph)

            u_new[i] = u[i] + dt * k_i * (u[i+1] - 2*u[i] + u[i-1]) / (dx**2)

        u = u_new.copy()

    plt.plot(x_values, u, label=r'$\alpha=$' + str(a))

plt.title('Perfil de temperatura')
plt.xlabel('Profundidade')
plt.ylabel('Temperatura')
plt.legend()
plt.grid(True)
plt.axhline(y=1, color='green', linestyle='--', label='')

plt.savefig('FVM.pdf', bbox_inches='tight')
