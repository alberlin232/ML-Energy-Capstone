

from lib.framework.MISO.query import *
import datetime

ind = 1
while ind == 1:
    print('\nPlease enter the start date and duration of the desired data set.')
    month = int(input('Month: '))
    day = int(input('Day: '))
    year = int(input('Year (4-digit format): '))
    try:
        datetime.datetime(year=year, month=month, day=day)
        ind = 0
    except:
        print('\nWARNING: The Date Does NOT Exist. Please Try Again!!')

duration = int(input('Duration (in days): '))

start = pd.Timestamp(year, month, day).date()

end = start + pd.Timedelta(days=duration)

datelist = []
while start < end:
    datelist.append(start)
    start += pd.Timedelta(days=1)

date = []
for d in datelist:
    date.append(str(d.year) + '{:02d}'.format(d.month) + '{:02d}'.format(d.day))

data_type = int(input('\nWhat type of data? (Answer 1, 2, or 3)\n'
                      '(1) Historical Locational Marginal Prices (LMP)\n'
                      '(2) Historical Marginal Clearing Prices (MCP)\n'
                      '(3) Summary Reports\n'))

#UPDATE THIS
if data_type == 3:
    fh = open("data/Ercot/2020Load.csv")
    transmissions = {}
    s = fh.readline()
    while(fh.readline()):
        s = fh.readline()
        curr = s.split(',')
        transmissions[curr[1]] = curr[2]
    # Iterate over the keys in dictionary, access value & print line by line
    for key in transmissions:
        if key != '' and key[] != '*':
            print(key, ' : ', transmissions[key], end='')
    print()

else:
    print("No data available.")


print('\nYour data has been successfully downloaded!\n'
      'Check your directory \'data/ERCOT\'\n')
