import matplotlib.pyplot as plt
from math import sqrt, log, pi, exp
import numpy as np

with open("single_daphnia_positions.txt", "r") as f1:
    points = []
    lines = f1.readlines()
    for l in lines:
        vals = [float(v) for v in l.split()]
        points.append(vals)
x = []
y = []
v = []
t = []
vx = []
vy = []
t_int = []
for i in range(1, len(points)):
    dx = points[i][0] - points[i - 1][0]
    dy = points[i][1] - points[i - 1][1]
    dt = points[i][2] - points[i - 1][2]
    t_avg = (points[i][2] + points[i - 1][2])/2
    s = sqrt(dx*dx + dy*dy)/dt    
    x.append(points[i - 1][0])
    y.append(points[i - 1][1])
    v.append(s)
    t.append(t_avg)
    vx.append(dx/dt)
    vy.append(dy/dt)
    t_int.append((points[i - 1][2], points[i][2]))

x.append(points[-1][0])
y.append(points[-1][1])

plt.figure(1, figsize=(6, 6))
plt.plot(x, y, 'b-', linewidth=1)
plt.xlabel("x Position(pixels)")
plt.ylabel("y Position(pixels)")
plt.show()

plt.figure(2, figsize=(15, 5))
plt.plot(t, v, 'k-', linewidth=1)
plt.xlabel('Time(s)')
plt.ylabel('Speed(pixels/s)')
plt.show()

a = []
t2 = []
for i in range(1, len(v)):
    dv = v[i] - v[i - 1]
    dt = t[i] - t[i - 1]
    t_avg2 = (t[i] + t[i - 1])/2
    a.append(dv/dt)
    t2.append(t_avg2)

plt.figure(3, figsize=(15, 5))
plt.plot(t2, a, 'g-', linewidth=1)
plt.xlabel("Time(s)")
plt.ylabel("Acceleration(pixels/s^2)")
plt.show()

f, axarr = plt.subplots(2, sharex=True, figsize=(12, 6))
axarr[0].plot(t, vx, 'k-', linewidth=1)
axarr[1].plot(t, vy, 'r-', linewidth=1)
axarr[0].set_title('x Component of Velocity')
axarr[1].set_title('y Component of Velocity')
f.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
plt.xlabel("Time(s)")
plt.ylabel("Velocity(pixels/s)", labelpad=20)
plt.show()






