__author__ = 'Vivek'

import csv
import os

path = 'C:/dummyfolder/'
files = os.listdir(path)    # gathering all the files in path folder

#removing files if already exist
if 'result_csv.csv' in files:
    os.remove(path+'result_csv.csv')
    files.remove('result_csv.csv')
if 'temp.csv' in files:
    os.remove(path+'temp.csv')
    files.remove('temp.csv')


sourc_file = path+files[0]
result_csv_file = path+'result_csv.csv'

# copy first file to a new create file called result_csv.csv
with open(sourc_file, "rb") as sourc_file_obj:
    reader = csv.reader(sourc_file_obj)
    with open(result_csv_file, "wb") as result_file:
        result_file.truncate()
        writer = csv.writer(result_file)
        for row in reader:
            writer.writerow(row)

#closing the file
sourc_file_obj.close()
result_file.close()

#removing first file from list
files.remove(files[0])

for singlefile in files:        # loop through all the files in list
    with open(path+singlefile, 'rb') as fone:   # open each file
        with open(result_csv_file, "rb") as ftwo:   #open result file
            with open(path +'temp.csv', "w") as f:    #opening temporary file to write
                writer = csv.writer(f,lineterminator='\n')
                readerfirst = csv.reader(fone);
                readersecond = csv.reader(ftwo)
                num_cols = len(readersecond.next())     # get column length
                ftwo.seek(0)

                for i,rows in enumerate(readerfirst):   # iterating throught each row
                        for j,nextrows in enumerate(readersecond):
                            if i == 0 and j==0:     # adding the header to temp list
                                localtemp = []
                                for cells in nextrows:
                                    localtemp.append(cells)
                                localtemp.append(rows[2])
                                writer.writerow(localtemp)
                                flagg = False
                                break

                            if rows[0] == nextrows[0]:  # comparing if bank name matches in result and temp file
                                temp = []
                                for x in nextrows:
                                    temp.append(x)
                                temp.append(rows[2])
                                writer.writerow(temp)
                                ftwo.seek(0)
                                flagg = False
                                break
                        temp = []
                        if(flagg): # true only if bank name was not matched in result_csv file
                            for x in range(0,len(rows)-1):  # appending non-assert cells to temp list
                                temp.append(rows[x])
                            for x2 in range(0,num_cols-2):  # appending 0 to temp list if bank name is not found
                                if nextrows[x2] != 0:
                                    temp.append(0)
                                else:
                                    temp.append(nextrows[x2])
                            temp.append(rows[len(rows)-1])  # appending reading file assert to temp list
                            writer.writerow(temp)
                            ftwo.seek(0)    # reserting for loop to 0
                        flagg = True
                f.close()
                fone.close()
                ftwo.close()

    with open(result_csv_file, "ab") as result_file:    #copying temp.csv data to result_csv file
        with open(path+'temp.csv', 'r') as tempfile:
            result_file.truncate()
            writer = csv.writer(result_file)
            tempreader = csv.reader(tempfile);
            for temprows in tempreader:
                writer.writerow(temprows)
    tempfile.close()
    result_file.close()

# Adding the total sum
with open(result_csv_file, "rb") as ftwo:
    with open(path+'temp.csv', "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        readersecond = csv.reader(ftwo)
        for i, rows in enumerate(readersecond):
            if i==0:
                localtemp = []
                for cells in rows:  # adding all the row cells to temp list
                    localtemp.append(cells)
                localtemp.append('Total Sum')
                writer.writerow(localtemp)
            else:
                tsum = 0    # initializing sum to 0
                totalrows = []
                liss = [0,1]    # skipping column 1 and 2
                for cells in range(0, len(rows)):
                    if cells not in liss:   # checking if the cell data is not first and second
                        tsum += int(rows[cells])    # adding the sum to total sum
                    totalrows.append(rows[cells])
                totalrows.append(tsum)
                writer.writerow(totalrows)  # Writing data to file

f.close()
ftwo.close()
with open(result_csv_file, "ab") as result_file:    # copying temp.csv data to result_csv
    with open(path+'temp.csv', 'r') as tempfile:
        result_file.truncate()
        writer = csv.writer(result_file)
        tempreader = csv.reader(tempfile);
        for temprows in tempreader:
            writer.writerow(temprows)
tempfile.close()
result_file.close()
os.remove(path + 'temp.csv')   # removing temp.csv file