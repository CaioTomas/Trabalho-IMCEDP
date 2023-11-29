import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
k = 6.3  # Thermal diffusivity (m^2/year)
L = 15.0  # Length of the rod (m)
T = 1.0  # Total time (years)
Nx = 150  # Number of spatial points
Nt = 1260 #200  # Number of time steps
dx = L / Nx  # Spatial step size
dt = T / Nt  # Time step size

# Initial condition function
def f(t):
    if (0 <= t <= 0.5) or (1 < t <= 1.5):
        f = 1
    elif (0.5 < t <= 1) or (1.5 < t <= 2):
        f = 10
    return f

# Boundary condition functions
def initial_condition(t, x):
    return f(t) * np.exp(-0.71 * x)

def right_boundary_condition(t, x):
    return np.zeros_like(x)

# Create grid
x_values = np.linspace(0, L, Nx+1)  # Spatial grid
u = initial_condition(0, x_values)  # Initial temperature distribution

frames = []  # To store frames for animation

# Explicit Euler method
for n in range(Nt):
    u_new = np.zeros_like(u)
    
    # Applying boundary conditions
    u_new[0] = f((n+1) * dt)
    u_new[-1] = right_boundary_condition((n+1) * dt, x_values)[-1]
    
    for i in range(1, Nx):  # Update inner points
        u_new[i] = u[i] + k * dt * (u[i+1] - 2 * u[i] + u[i-1]) / (dx**2)
    
    u = u_new.copy()
    frames.append(u.copy())  # Store current temperature distribution for each frame
    
# Create an animation
fig, ax = plt.subplots()
line, = ax.plot(x_values, frames[0], label='Temperature distribution')
plt.title('Temperature distribution over 1D rod')
plt.xlabel('Position')
plt.ylabel('Temperature')
plt.legend()
plt.grid(True)

# Set y-axis range
ax.set_ylim(0,10)

# Vertical line at x = 4.4
ax.axvline(x=4.4, color='red', linestyle='--', label='x = 4.4')

# Timer text
timer_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def update(frame):
    line.set_ydata(frames[frame])
    time = (frame + 1) * dt  # Calculate current time
    timer_text.set_text(f'Time: {time:.2f} years')  # Update timer text
    return line, timer_text

ani = FuncAnimation(fig, update, frames=len(frames), interval=50)

# Save the animation as an MP4 file
ani.save('temperature_evolution.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# plt.show()