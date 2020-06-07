import numpy as np

ref = 8.6680

f = open('Energies', 'r')
line = f.readline()
columns = len(line.split())
f.close()

f = open('Energies', 'r')
data = f.read()
f.close()
data = data.split()
data = [float(i) for i in data]

f = open('Energies_Ref', 'r')
data_ref = f.read()
f.close()
data_ref = data_ref.split()
data_ref = [float(i) for i in data_ref]

if columns == 6:  # excited state to study > first excites state
	energy_down = data[0::6]
	osc_down = data[1::6]
	energy_down_Ref = data_ref[0]
	osc_down_Ref = data_ref[1]

	energy = data[2::6]
	osc = data[3::6]
	energy_Ref = data_ref[2]
	osc_Ref = data_ref[3]

	energy_up = data[4::6]
	osc_up = data[5::6]
	energy_up_Ref = data_ref[4]
	osc_up_Ref = data_ref[5]

else:
	energy = data[0::4]
	osc = data[1::4]
	energy_Ref = data_ref[0]
	osc_Ref = data_ref[1]

	energy_up = data[2::4]
	osc_up = data[3::4]
	energy_up_Ref = data_ref[2]
	osc_up_Ref = data_ref[3]

#
# Modify here to add the oscilator straigh weighted average to the final energies: 
#
final_energy = energy
ref = energy_Ref
relative_energy = []
for i in range(len(final_energy)):
	relative_energy.append(final_energy[i] - ref)
maxi = max(relative_energy)
mini = min(relative_energy)

normal_energy = []
for i in range(len(final_energy)):
	if relative_energy[i] > 0:
		normal_energy.append(relative_energy[i]/maxi)
	else:
		normal_energy.append(-1*relative_energy[i]/mini)

f = open('points.txt', 'r')
coords = []
for i in range(len(final_energy)):
	line = f.readline().rstrip('\n')
	coords.append(line)
f.close()

f = open('Result.mol2','w')
f.write('@<TRIPOS>MOLECULE\n')
f.write('*****\n')
f.write(' %d 0 0 0 0\n' %len(final_energy)) # decimal integer
f.write('SMALL\n')
f.write('GASTEIGER\n')
f.write(' \n')
f.write('@<TRIPOS>ATOM\n')
for i in range(len(final_energy)):
	f.write('%7.0f H  %s   H   0   UNL  %7.4f\n' %(i+1, coords[i], normal_energy[i]))
f.close()

