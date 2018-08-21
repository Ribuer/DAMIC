from pylab import *                                                                                                     
import matplotlib                                                                                                       
import matplotlib.pyplot as plt    
import time
import shutil
import datetime
#6hr automatic report overview of experiment status
 
def auto_report(time_range, fig_nr, copied_file):                                                                                                          

	print_file = open(copied_file, "r")        
                                                                             
	lines = print_file.readlines()

	temp_list_1 = []                                                                                                        
	temp_list_2 = []                                                                                                        
	press_list = []                                                                                                         
	time_list = []                                                                                                          
	date_list = []                                
                                                                                                                                                                                                   
	interval_val = 60   	#append value for every x seconds
	
	if interval_val % (3600*24) == 0:
		int_in = int(interval_val/(3600*24))
		interval_print = str(int_in)+" d"
	elif interval_val % 3600 == 0:
		int_in = int(interval_val/3600)
		interval_print = str(int_in)+" h"
	elif interval_val % 60 == 0:
		int_in = int(interval_val/60)
		interval_print = str(int_in)+" min"
	else:
		interval_print = str(interval_val)+" s"
                                                                                                                                                                                      
	for i in range(0, int(time_range/interval_val)):                                                                                 
		temp_list_1.append(lines[-1*time_range+i*interval_val-1][2:8])                                                                                  
		temp_list_2.append(lines[-1*time_range+i*interval_val-1][33:39])                                                                                
		press_list.append(lines[-1*time_range+i*interval_val-1][61:69])                                                                                 

	time_list.append(lines[2+i*30][79:87].replace(":","."))                                                                 
	date_list.append(lines[2+i*30][92:].replace("/","."))    
                                                                                                                                                                                   
	plt.figure(fig_nr)                                                                                                           
	plt.plot(temp_list_1, label="Base Plate")                                                                                                   
	plt.plot(temp_list_2, label="Sensor RTD")    
	plt.title("Temperature history \n from "+str(lines[-1*time_range-1][92:102])+", "+str(lines[-1*time_range-1][79:84])+"\n to "+str(lines[-1][92:102])+", "+str(lines[-1][79:84]))                                                                                             
	plt.xlabel("Time ("+interval_print+")")     
	plt.ylabel("Temperature (K)")                     
	plt.grid(True)   
	plt.legend()
	plt.show()

	
	plt.savefig('./Plot_Output/Temperature_History_'+str(lines[-1*time_range][92:102]).replace("/", "_")+"__"+str(lines[-1*time_range-1][79:84]).replace(":","_")+"__"+str(lines[-1][79:84]).replace(":", "_")+'.png')

	plt.figure(fig_nr+1)                                                                                                           
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))                                                            
	plt.plot(press_list)                                                                                                    
	plt.title("Pressure history \n from "+str(lines[-1*time_range-1][92:102])+", "+str(lines[-1*time_range-1][79:84])+"\n to "+str(lines[-1][92:102])+", "+str(lines[-1][79:84]))                                                                                          
	plt.xlabel("Time ("+interval_print+")")     
	plt.ylabel("Pressure (mbar)")    
	plt.grid(True)
	plt.show()                                       
                                                                       
	plt.savefig('./Plot_Output/Pressure_History_'+str(lines[-1*time_range][92:102]).replace("/", "_")+"__"+str(lines[-1*time_range-1][79:84]).replace(":","_")+"__"+str(lines[-1][79:84]).replace(":", "_")+'.png')

	print_file.close()    

fig_nr = 0
sleep = 0

if __name__ == "__main__":
    
    #Start plotting at 6 hr cyclus
	hour, minute = int(datetime.datetime.now().strftime("%I")), int(datetime.datetime.now().strftime("%M"))
	if minute == 0 and hour % 6 == 0:
		run = True
	else:
		sleep += (60-minute)*60
		sleep += ((24-(hour+1)) % 6)*3600
		time.sleep(sleep)
		run = True
    
    #Set correct plot outputs depending on start of cyclus
	if 24/hour > 4:
		check_time = 0
	elif 24/hour > 2:
		check_time = 1
	elif 24/hour > 4./3.:
		check_time = 2
	else:
		check_time = 3
    
	while run:
		shutil.copy2('Temperature_Log_File.txt', './Plot_Output/Temperature_Log_File.txt')
 
		auto_report(21600, fig_nr, "./Plot_Output/Temperature_Log_File.txt")
		fig_nr += 2
		if check_time == 1 or check_time == 3:
			auto_report(43200, fig_nr, "./Plot_Output/Temperature_Log_File.txt")
			fig_nr += 2
	
		if check_time == 3:
			auto_report(86400, fig_nr, "./Plot_Output/Temperature_Log_File.txt")
			check_time = -1
			fig_nr += 2
	
		print("Successful report: \n"+str(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))+"\nNext report in 6h.")
		time.sleep(21600)
		check_time += 1
                                                                                                                                                                   
