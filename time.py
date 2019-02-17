def timedate_process(data_input):
    data_timelist=data_input['localtime']
    time_weekday=[]
    dict_time={}
    time_list=[]
    holiday_list=[]
    weather_list=[]
    timeblock_list=[]
    #count=0

    ######set the time block size(min)
    time_size=30
    #############

    #weather data load
    weather_data=pd.read_csv("DAILYDATA_S108_201808.csv")


    for i in data_timelist:
        data_test=i
        n=0
        #count=count+1
        #print(count)
        for j in range(0,len(data_test)):
            if data_test[j]=='.':
                n=j
            else:
                n=19
        #print(n)
        data_test=data_test[0:n] #delete . and after 
        #print(data_test)
        time=datetime.datetime.strptime(data_test, "%Y-%m-%d %H:%M:%S")
    
        #weekday
        time_weekday.append(time.weekday())  # 0-6->monday-sunday
        time_list.append(time)
    
    
        #holiday
        holiday_test=time.strftime('%j')
        if time_weekday==5 or time_weekday==6 or holiday_test=='089' or holiday_test=='121' or holiday_test=='149' or holiday_test=='166' or holiday_test=='221' or holiday_test=='234' or holiday_test=='310' or holiday_test=='359':
            holiday_list.append(1)
        else:
            holiday_list.append(0)
    

        #weather 
        if int(holiday_test) > 212 and int(holiday_test) < 243:
            rainfall_total=weather_data['Daily Rainfall Total (mm)'][holiday_test-213]
            if rainfall_total<5:
                weather=0
            elif rainfall_total <15:
                weather=1
            elif rainfall_total <25:
                weather=2
            else:
                weather=3
            #print(weather)
        weather_list.append(weather)
        
    
        #times
        hour=int(time.strftime('%H'))
        minute=int(time.strftime('%M'))
        time_temp=hour*(60/time_size)+math.floor(minute/time_size)
        timeblock_list.append(time_temp)
    
        
    dict_time['timeblock']=timeblock_list     
    dict_time['weather']=weather_list      
    dict_time['holiday']=holiday_list
    dict_time['weekday']=time_weekday
    dict_time['time']=time_list
    return dict_time