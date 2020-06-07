#!/bin/bash
#SBATCH -J PHE_batch_3
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -t 20:50:00
#SBATCH --mem=22000MB 
#--------------------------------------------------------------#
NPROCS=`wc -l < $SLURM_JOB_NODELIST`
cd $SLURM_SUBMIT_DIR
#--------------------------------------------------------------#
#  Change the Project!!!
#--------------------------------------------------------------#
export Project=$SLURM_JOB_NAME
export WorkDir=/scratch/$USER/$SLURM_JOB_ID
mkdir -p $WorkDir
export InpDir=$SLURM_SUBMIT_DIR
echo $SLURM_JOB_NODELIST > $InpDir/nodename
echo $SLURM_JOB_ID > $InpDir/jobid
#--------------------------------------------------------------#
# Copy of the files - obsolete
#--------------------------------------------------------------#
#cp $InpDir/$Project.xyz $WorkDir/$Project.xyz
#cp $InpDir/$Project.key $WorkDir/$Project.key
#cp $InpDir/*.prm $WorkDir/
#--------------------------------------------------------------#
# Start job
#--------------------------------------------------------------#

   cd $WorkDir
   mkdir scr
   g03root=/home/yoelvis/bin
   GAUSS_SCRDIR=$WorkDir/scr
   #GAUSS_SCRDIR=$HOME/scr
   export g03root GAUSS_SCRDIR
   source $g03root/g03/bsd/g03.profile
   cp $InpDir/${SLURM_JOB_NAME}.com $WorkDir
   g03 ${SLURM_JOB_NAME}.com
   cp $WorkDir/*.log $InpDir
   rm -r $WorkDir


#cd $WorkDir
#for i in $InpDir/*.com; do
#   mkdir scr
#   g03root=/home/yoelvis/bin
#   GAUSS_SCRDIR=$WorkDir/scr
#   #GAUSS_SCRDIR=$HOME/scr
#   export g03root GAUSS_SCRDIR
#   source $g03root/g03/bsd/g03.profile
#   cp $InpDir/$i $WorkDir
#   g03 $i
#   cp $WorkDir/*.log $InpDir
#   rm -r scr
#done
#rm -r $WorkDir


