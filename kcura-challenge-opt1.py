'''KCura Code Challenge'''
'''Submitted by - Praveen Balasubramanian '''
'''Import required packages '''

import fileinput, string, sys, re
from collections import Counter
from operator import itemgetter
from os.path import exists


#Read input filename, strip pipe delimiters and return a list.
def readfile(filename):
    records = []
    for line in fileinput.input(filename):
        if fileinput.isfirstline():  # first row becomes col names
            columns = line.split('|')  # split on the delimiter

        if not fileinput.isfirstline():
            try:
                line[1]  # only append populated rows
                otherline = line.split('|')  # split on the delimiter
                records.append(otherline)
            except IndexError:
                print "emptyline"
    return records
	
#Data processing step
def dataprocess(records):
    data_clean=[]
    inter_count=[]
    for i in records:
        for j in i:
            data_clean.append(j.strip())
    i=0
    Processed_record=[]
    while i<len(data_clean):
        Processed_record.append(data_clean[i:i+4]) #Combine every record in the list of lists format.
        inter_count.append(data_clean[i+3]) #Combine interstate details of every state into a single list.
        i+=4
    Processed_rec_sorted = sorted(Processed_record, key=lambda x: x[0],reverse=True) #Sort the records based on population
    inter = [c.split(';') for c in inter_count]
    inter2 = reduce(lambda x,y: x+y,inter)
    inter3 = [c.strip('I-') for c in inter2]
    inter4 = map(int,inter3)
    inter5 = map(list,sorted((Counter(inter4)).items(), key=itemgetter(0)))
    inter6 = ['I-'+str(item[0])+ ' '+str(item[1]) for item in inter5] #A sorted list with count of interstate routes.
    return Processed_rec_sorted,inter6

#Convert the list of lists records to a dictionary.	
def conv_to_dict(Processed_rec_sorted):
    dict_of_records = {}
    for i in Processed_rec_sorted:
        if i[0] in dict_of_records:
            dict_of_records[i[0]] = dict_of_records[i[0]] + i[1:4]
        else:
            dict_of_records[i[0]] = i[1:4]
    return dict_of_records

#A function to merge states with same population.	
def combine_same_state_pop(dict_of_records):
    
    combined_list = {}
    for i in dict_of_records:
        count = len(dict_of_records[i])
        if count == 3:
            combined_list[i] = dict_of_records[i]
        else:
            x=0
            temp_list=[]
            lis = dict_of_records[i]
            while x<len(lis):
                temp_list.append(lis[x:x+3])
                x+=3
            sorted_temp_list = sorted(temp_list, key=lambda x: (x[1], x[0])) #Sorting first by states and then by city
            combined_list[i] = sorted_temp_list
    return combined_list

#Function to write the processed records to output file.	
def writefile(combined_list,Inter_count):
    
    f = open("Cities_By_Population.txt", "w")
	#Printing records by highest to lowest population.
    for key in iter(reversed(sorted(combined_list.items(), key=lambda x: int(x[0])))):  
        if len(key[1])==3:
            state_Interstate = key[1]
            f.write("\n")
            f.write(key[0]+ "\n")
            f.write("\n")
            f.write(str(state_Interstate[0]) +','+ ' ' + str(state_Interstate[1]) + "\n")
            interstate = re.split(r"\s*[,;]\s*", state_Interstate[2].strip())
            f.write("Interstates:"+ ' ' + ', '.join(interstate) + "\n")

        else:
            f.write("\n")
            f.write(key[0]+ "\n")
            state_Interstate = key[1]
			#A for loop is added here to print states with same population.
            for states in state_Interstate:
                f.write("\n")
                f.write(str(states[0]) +','+ ' ' + str(states[1]) + "\n")
                interstate = re.split(r"\s*[,;]\s*", states[2].strip())
                f.write("Interstates:" + ' '+ ', '.join(interstate) + "\n")
    f.close()
	#Open a new file to write Interstate details.
    f = open("Interstates_By_City.txt","w")
    for i in Inter_count:
        f.write(i + "\n")
    f.close()
    return

def main():
	
    filename = raw_input("Enter input filename along with '.txt' extension: ")
    try:
		
		read_rec = readfile(filename)
		dp,inter_count = dataprocess(read_rec)
		con_dict = conv_to_dict(dp)
		combine = combine_same_state_pop(con_dict)
		Final = writefile(combine,inter_count)
		print "Success..Please check your working directory for two files named 'Cities_By_Population.txt' and 'Interstates_By_City.txt'"
    except IOError:
		print "File not found. Make sure the input file exists in the working directory and then try executing the program again !!!"
		

if __name__ == '__main__':
    main()
    