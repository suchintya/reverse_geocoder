import csv
import datetime

def main():
	print("hello world")
	lastId = 1
	modaloc = {879398948:list()}
	with open('output.csv') as csvfile:
		batchreader = csv.reader(csvfile)
		lastrow = list()
		for row in batchreader:
			tempId = int(row[6])
			if(tempId == lastId):
				timestr = row[8][:22]+row[8][23:]
				localtime = datetime.datetime.strptime(timestr,'%Y-%m-%d %H:%M:%S%z')
				localhour = int(localtime.strftime("%H"))
				if(localhour > 12 and localhour < 17):
					modaloc[row[0]] = row
			else:
				geoList = []
				print("len ", len(modaloc))
				for k, val in modaloc.items():
					tempHash = str(val[2:3])
					tempHash1 = tempHash[2:9]
					geoList.append(tempHash1)
				if(len(geoList) > 0):
					geoMode = max(geoList, key = geoList.count)
					print("geomode: ",geoMode)
					if(len(geoMode) > 0):
						with open('modeout.csv','w',newline='') as csvout:
							spamwriter = csv.writer(csvout)
							spamwriter.writerow({lastId,geoMode})
				lastId = tempId
				modaloc.clear()
				geoList.clear()


if __name__ == '__main__':
    main()
