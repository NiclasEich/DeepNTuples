#!/usr/bin/env python2

# read stdout from each job to get job status (cmsRun success or not)
# use log files to evaluate batch status
# get job ids from file list
# 
# print number of suvvessful jobs
#


# usage: check.py singledir


#for each job in 
import os
import glob
from argparse import ArgumentParser

parser = ArgumentParser('check the status of the jobs on the batch queue, pass a directory and an action. Action can be: none, remove, resubmit. The action remove removes failed output. After that, the failed jobs can be resubmitted with resubmit')
parser.add_argument('dir')
parser.add_argument('action')
args = parser.parse_args()
dir=args.dir

stdoutfiles=glob.glob(dir+"/batch/con_*.out")

#print (stdoutfiles)

failedjobs=[]
succjobs=[]
runjobs=[]
#exit()

for filename in stdoutfiles:
    #print (filename)
    if 'JOBSUB::FAIL' in open(filename).read():
        failedjobs.append(filename)
    elif 'JOBSUB::SUCC' in open(filename).read():
        succjobs.append(filename)
    elif 'JOBSUB::RUN' in open(filename).read():
        runjobs.append(filename)


nidle=len(stdoutfiles)-len(failedjobs)-len(succjobs)-len(runjobs)
print ('idle: '    + str(nidle))
print ('failed: '  + str(len(failedjobs)))
print ('success: ' + str(len(succjobs)))
print ('running: ' + str(len(runjobs)))

nJobs=nidle+len(failedjobs)+len(succjobs)+len(runjobs)
ntupleOutDir=os.path.abspath(dir+'/output/')

for f in failedjobs:
    print('failed job, see: ' + f)
    jobno=os.path.basename(f).split('.')[1]
    
    # remove the failed output
    if args.action == 'remove':
        outputFile=dir+'_'+jobno
        fulloutfile=os.path.join(ntupleOutDir,outputFile+'.root')
        if os.path.exists(fulloutfile):
             os.remove(fulloutfile)
             print ('removed '+fulloutfile)

    if args.action == 'resubmit':

        print('resubmitting...')
        #remove old output files
        for outlog in glob.glob(dir+'/batch/con_*'+jobno+'.*'):
            os.remove(outlog)
        os.system('cd ' + dir + ' && condor_submit batch/condor_'+ jobno+'.sub && touch batch/con_out.'+ jobno +'.out')
       

succoutfile=' '
if args.action == 'merge' or len(succjobs)==nJobs:
     if len(succjobs)>0:
         for f in succjobs:
             jobno=os.path.basename(f).split('.')[1]
             outputFile=dir+'_'+jobno
             fulloutfile=os.path.join(ntupleOutDir,outputFile+'.root')
             succoutfile = succoutfile+ ' ' + fulloutfile
         
         print('merging output to '+dir+'.root')
         outputroot=ntupleOutDir+'/'+dir+'.root'
         os.system('hadd '+outputroot+ succoutfile)
         
         
         
         
         
         
         
         
     