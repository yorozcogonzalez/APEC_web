#!/bin/bash

echo "Calculations started" >> Infos.dat

Templates=`grep "Templates" Infos.dat | awk '{ print $2 }'`
multiplicity=`grep "multiplicity" Infos.dat | awk '{ print $2 }'`
charge=`grep "charge" Infos.dat | awk '{ print $2 }'`
Project=`grep "Project" Infos.dat | awk '{ print $2 }'`
xyz_name=`grep "xyz_name" Infos.dat | awk '{ print $2 }'`
basis_set=`grep "basis_set" Infos.dat | awk '{ print $2 }'`
exc_state=`grep "selected_state" Infos.dat | awk '{ print $2 }'`
num_states=`grep "num_states" Infos.dat | awk '{ print $2 }'`

pointcharge=" 0.10"
batch=12

cp $Templates/gaussian_template ${Project}.com
sed -i "s/CHARGEGAU/$charge/" ${Project}.com
sed -i "s/MULTIGAU/$multiplicity/" ${Project}.com
sed -i "s/BASISGAU/$basis_set/" ${Project}.com
sed -i "s/NUMSTATESGAU/$num_states/" ${Project}.com

numxyz=`head -n1 $xyz_name | awk '{ print $1 }'`
check=`wc -l $xyz_name | awk '{ print $1 }'`
if [[ $check -eq $(($numxyz+1)) ]]; then
   echo -e "\n" >> $xyz_name
fi
head -n $(($numxyz+2)) $xyz_name | tail -n $numxyz >> ${Project}.com
echo "" >> ${Project}.com

j=0
cont=1
numpoints=`wc -l points.txt | awk '{ print $1 }'`

for i in $(eval echo "{1..$numpoints}"); do
   j=$(($j+1))
   point=`head -n $i points.txt | tail -n1 | awk '{ print $0 }'`
   echo "$point   $pointcharge" > temp
   if [[ $j -lt $batch ]]; then
      cat ${Project}.com temp >> ${Project}_batch_${cont}.com
      echo "" >> ${Project}_batch_${cont}.com
      if [[ $i -ne $numpoints ]]; then
         echo "--link1--" >> ${Project}_batch_${cont}.com
      fi
   fi
   if [[ $j -eq $batch ]]; then
      cat ${Project}.com temp >> ${Project}_batch_${cont}.com
      echo "" >> ${Project}_batch_${cont}.com
      j=0
      cont=$(($cont+1))
   fi
   rm temp
done

#
# Reference Configurations
#
cp $Templates/gaussian_template ${Project}_Ref.com

sed -i "s/CHARGEGAU/$charge/" ${Project}_Ref.com
sed -i "s/MULTIGAU/$multiplicity/" ${Project}_Ref.com
sed -i "s/BASISGAU/$basis_set/" ${Project}_Ref.com
sed -i "s/NUMSTATESGAU/$num_states/" ${Project}_Ref.com
sed -i "s/charge NoSymm/NoSymm/" ${Project}_Ref.com
numxyz=`head -n1 $xyz_name | awk '{ print $1 }'`
head -n $(($numxyz+2)) $xyz_name | tail -n $numxyz >> ${Project}_Ref.com
echo "" >> ${Project}_Ref.com

cp $Templates/Gau_submit.sh gaussian_Ref.sh
sed -i "s/Nombre/${Project}_Ref/" gaussian_Ref.sh
#####################################################################

numjobs=`ls -1 ${Project}_batch_*.com | wc -l`
rm -f jobnumbers
for i in $(seq 1 $numjobs); do
   cp $Templates/Gau_submit.sh gaussian_$i.sh
   sed -i "s/Nombre/${Project}_batch_$i/" gaussian_$i.sh
   sbatch gaussian_$i.sh >> jobnumbers
   sleep 0.2
done
#cp ../rPSB_sal/*.log .
sbatch gaussian_Ref.sh >> jobnumbers

sed -i "s/Calculations started/Calculations submitted/" Infos.dat

if [ -f "jobnumbers" ]; then
   running=10
   while [[ $running != 0 ]]; do
      rm -f temp
      sleep 2
      if [[ ! -f jobnumbers ]]; then
         sed -i "s/Calculations submitted/Calculations deleted/" Infos.dat
         exit 1
      fi
      for i in $(seq 1 $(($numjobs+1))); do
         job=`head -n $i jobnumbers | tail -n1 | awk '{ print $4 }'`
         squeue -u yoelvis | grep " $job " >> temp
      done
      running=`wc -l temp | awk '{ print $1 }'`
   done
fi

rm -f energy_down*
rm -f energy*
rm -f energy_up*
for i in $(seq 1 $numjobs); do
   if [[ $exc_state -ge 2 ]]; then
      grep "Excited State   $(($exc_state-1)):" ${Project}_batch_${i}.log | awk '{ print $(NF-4) "  " $NF }' | sed "s/f=/\ /g" >> energy_down
   fi
   grep "Excited State   $exc_state:" ${Project}_batch_${i}.log | awk '{ print $(NF-4) "  " $NF }' | sed "s/f=/\ /g" >> energy
   grep "Excited State   $(($exc_state+1)):" ${Project}_batch_${i}.log | awk '{ print $(NF-4) "  " $NF }' | sed "s/f=/\ /g" >> energy_up
done

if [[ $exc_state -ge 2 ]]; then
   grep "Excited State   $(($exc_state-1)):" ${Project}_Ref.log | awk '{ print $(NF-4) "  " $NF }' | sed "s/f=/\ /g" >> energy_down_Ref
fi
grep "Excited State   $exc_state:" ${Project}_Ref.log | awk '{ print $(NF-4) "  " $NF }' | sed "s/f=/\ /g" >> energy_Ref
grep "Excited State   $(($exc_state+1)):" ${Project}_Ref.log | awk '{ print $(NF-4) "  " $NF }' | sed "s/f=/\ /g" >> energy_up_Ref


if [[ $exc_state -ge 2 ]]; then
   paste energy_down energy energy_up > Energies
   paste energy_down_Ref energy_Ref energy_up_Ref > Energies_Ref
else
   paste energy energy_up > Energies
   paste energy_Ref energy_up_Ref > Energies_Ref
fi

source /home/yoelvis/virtual_envs/py3_estm/bin/activate
python ESTM.py

cp Result.mol2 $Project.mol2
if [[ $xyz_name != $Project.xyz ]]; then
   cp $xyz_name $Project.xyz
   touch $xyz_name
fi
touch $Project.xyz

sed -i "s/Calculations submitted/Calculations done/" Infos.dat
echo "Copying files back to server, then you will se success"

exit 0

