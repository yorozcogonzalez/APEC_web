import matplotlib
matplotlib.use('Agg')
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from pyvdwsurface import vdwsurface

f = open('rPSB.xyz', 'r')
data = f.read()
f.close

data = data.split()

atom = data[1::4]
x = data[2::4]
y = data[3::4]
z = data[4::4]
x = [float(i) for i in x]
y = [float(i) for i in y]
z = [float(i) for i in z]


coordinates = np.ndarray(shape=(len(atom),3), dtype=float, order='C')
elements = []
for i in range(len(atom)):
    coordinates[i] = [x[i], y[i], z[i]]
    elements.append(atom[i])
    
scale_factor = 2.0
density=1

points = vdwsurface(coordinates, elements, scale_factor, density)

pointsXx = []
pointsXx.append([len(points), "", "", ""])
pointsXx.append(["", "", "", ""])
print('{} points on the surface'.format(len(points)))
for i in range(len(points)):
    pointsXx.append(["Xx", points[i,0], points[i,1], points[i,2]])
np.asarray(pointsXx)

np.savetxt("pointsXx.xyz", pointsXx, fmt='%s')
np.savetxt("points.txt", points, fmt='%8.4f')

#print(points)
#print(type(points))

fig = plt.figure()
ax = Axes3D(fig)
#ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2], marker='o')
#ax.set_xlim(-2,2)
#ax.set_ylim(-2,2)
#ax.set_zlim(-2,2)
#plt.show()
plt.savefig('example.png')
