
import pandas as pd # import panda
from lib.framework.MISO.query import *
import datetime

ind = 1
while ind == 1:
    print('\nPlease enter the start date and duration of the desired data set. ')
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
curr = start
end = start + pd.Timedelta(days=duration)

numberOfDaysInFinalYear = 0
datelist = []
while curr < end:
    datelist.append(curr)
    curr += pd.Timedelta(days=1)
    if curr.year == end.year:
        numberOfDaysInFinalYear +=1

date = []
for d in datelist:
    date.append(str(d.year) + '{:02d}'.format(d.month) + '{:02d}'.format(d.day))

data_type = int(input('\nWhat type of data? (Answer 1, 2, or 3)\n'
                      '(1) Market Information \n'
                      '(2) Grid Infroamtion\n'
                      '(2) Ancillary Services\n'
                      '(4) Summary Reports\n'))

#UPDATE THIS
print(datelist)   #for debugging
if data_type == 1:
    menuType = int(input('\nWhat type of data? (Answer 1)\n'
                      '(1) Clearing Prices for Capacity (Day-Ahead-Market) \n'
                      '(2) Load Zone And Hub Prices (Day-Ahead-Market) \n'
                      '(3) Load Zone And Hub Prices (Real-Time-Market) \n'))
    if menuType == 1:
        fileName = {2010 : 'rpt.00013091.0000000000000000.20121019.154814.DAMASMCPC_2010.csv',2011 : 'rpt.00013091.0000000000000000.20121019.154832.DAMASMCPC_2011.csv',2012 : 'rpt.00013091.0000000000000000.20130101080004.DAMASMCPC_2012.csv', 
                    2013 : 'rpt.00013091.0000000000000000.20140101080003.DAMASMCPC_2013.csv', 2014 : 'rpt.00013091.0000000000000000.20150101080004.DAMASMCPC_2014.csv', 2015 : 'rpt.00013091.0000000000000000.20160101080005.DAMASMCPC_2015.csv',
                    2016 : 'rpt.00013091.0000000000000000.20170101080004.DAMASMCPC_2016.csv', 2017 : 'rpt.00013091.0000000000000000.20180101080005.DAMASMCPC_2017.csv', 2018 : 'rpt.00013091.0000000000000000.20190101080004.DAMASMCPC_2018.csv',
                    2019 : 'rpt.00013091.0000000000000000.20200101080005.DAMASMCPC_2019.csv', 2020 : 'rpt.00013091.0000000000000000.20210101080006.DAMASMCPC_2020.csv', 2021 : 'rpt.00013091.0000000000000000.20220101080017.DAMASMCPC_2021.csv',
                    2022 : 'rpt.00013091.0000000000000000.20220403080011.DAMASMCPC_2022.csv'}
        fileAddress = 'raw_data/ERCOT/DAMClearingPricesForCap/' + fileName[start.year]  #specify year
        df = pd.read_csv(fileAddress)

        currYear = start.year
        # print("START YEAR: " + str(currYear))
        # print("END YEAR: " + str(end.year))
        while(currYear <= end.year):
            currdf = pd.read_csv( ('raw_data/ERCOT/DAMClearingPricesForCap/' + fileName[currYear]) )
            if currYear != end.year:     #add all entries
                df = pd.concat([df, currdf])
            else:  #add row = number of days in finalYear * 24
                df = pd.concat([df, currdf[0: numberOfDaysInFinalYear *24]])
            currYear += 1
        print(df.to_string())

        savedFile = 'data/ERCOT/DAM' + str(start) + '-' + str(end)
        df.to_csv(savedFile, index=False)  # save file

    elif menuType == 2:
        zone = 0
        while 1:
            zone = int(input('\nWhat settlement point? [1,14] \n'
                      '(1) HB_BUSAVG \n'
                      '(2) HB_HOUSTON) \n'
                      '(3) HB_HUBAVG \n'
                      '(4) HB_NORTH \n'
                      '(5) HB_South) \n'
                      '(6) HB_WEST \n'
                      '(7) LZ_AEN \n'
                      '(8) LZ_CPS) \n'
                      '(9) LZ_HOUSTON \n'
                      '(10) LZ_LCRA \n'
                      '(11) LZ_NORTH) \n'
                      '(12) LZ_RAYBN \n'
                      '(13) LZ_SOUTH) \n'
                      '(14) LZ_WEST \n'))
            if zone > 0 and zone < 15:
                break
        zones = { 1: 'HB_BUSAVG', 2 : 'HB_HOUSTON', 3: 'HB_HUBAVG', 4: 'HB_NORTH', 5: 'HB_South', 6 :'HB_WEST', 7 : 'LZ_AEN' , 8: 'LZ_CPS' ,
                     9: 'LZ_HOUSTON', 10: 'LZ_LCRA', 11 : 'LZ_NORTH', 12: 'LZ_RAYBN ', 13 : 'LZ_SOUTH' , 14 : 'LZ_WEST'} 
        fileName = {2010 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2010.csv', 2011 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2011.csv', 2012 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2012.csv', 
                    2013 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2013.csv', 2014 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2014.csv', 2015 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2015.csv',
                    2016 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2016.csv', 2017 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2017.csv', 2018 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2018.csv',
                    2019 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2019.csv', 2020 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2020.csv', 2021 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2021.csv',
                    2022 : 'rpt.00013060.0000000000000000.DAMLZHBSPP_2022.csv'}
        fileAddress = 'raw_data/ERCOT/DAMLoadZoneAndHubPrices/' + fileName[start.year]  #specify year
        df = pd.read_csv(fileAddress, header=1) 
        print(df.head())

        currYear = start.year
        while(currYear <= end.year):
            currdf = pd.read_csv('raw_data/ERCOT/DAMLoadZoneAndHubPrices/' + fileName[currYear])
            if currYear != end.year:     #add all entries
                df = pd.concat([df, currdf])
            else:  #add row = number of days in finalYear * 24
                df = pd.concat([df, currdf[0: numberOfDaysInFinalYear * 24 * 14], ])
            df = df.loc[df["Settlement Point"] == zones[zone]] # keep only correct time zone
            currYear += 1
            savedFile = 'data/ERCOT/DAM' + str(start) + '-' + str(end)
            df.to_csv(savedFile, index=False)  # save file



elif data_type == 4:
    fh = open("data/Ercot/2020Load.csv")
    transmissions = {}
    s = fh.readline()
    while(fh.readline()):
        s = fh.readline()
        curr = s.split(',')
        transmissions[curr[1]] = curr[2]
    # Iterate over the keys in dictionary, access value & print line by line
    for key in transmissions:
        if key != '' and key != '*':
            print(key, ' : ', transmissions[key], end='')
    print()
else:
    print("No data available.")


print('\nYour data has been successfully downloaded!\n'
      'Check your directory \'data/ERCOT\'\n')
