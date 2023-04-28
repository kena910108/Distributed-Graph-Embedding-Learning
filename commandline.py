import os
import shutil

partition = 5
landmark = 200

cmd = "python partition.py " + str(partition) +" "+str(landmark)
os.system(cmd)
sample = 20000/partition

for i in range(0,partition):
	print("progress partition",str(partition),i,str(i),sample,str(int(sample)))
	cmd = "line.exe -train graph_"+str(i)+".txt -output local_"+str(i)+".txt -binary 1 -size 128 -order 1 -negative 5 -samples "+str(int(sample))+" -threads 80"
	os.system(cmd)
cmd = "line.exe -train basis_graph.txt -output local_landmark.txt -binary 1 -size 128 -order 1 -negative 5 -samples 5000 -threads 80"
os.system(cmd)

cmd = "python lasso.py "+str(partition)
os.system(cmd)
os.chdir(r"C:\Users\ken\Desktop\Coursework\LINE-master\windows\evaluate")

shutil.rmtree(r"C:\Users\ken\Desktop\Coursework\LINE-master\windows\evaluate\workspace")
os.mkdir(r"C:\Users\ken\Desktop\Coursework\LINE-master\windows\evaluate\workspace")

cmd = "run.bat ..\test_positive.txt result"+str(partition)+".txt"
os.system(cmd)
cmd = "python score.py result"+str(partition)+".txt"
os.system(cmd)
os.chdir(r"C:\Users\ken\Desktop\Coursework\LINE-master\windows")