def timedate_process(data_input):
    data_timelist=data_input['localtime']
        time_weekday=[]
    dict_time={}
    time_list=[]
    holiday_list=[]
    weather_list=[]
    timeblock_list=[]
    topic_list=[]
    event_asian_list=[]
    event_mall_list=[]
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
        weather=0
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
            print(weather)
        weather_list.append(weather)
        
    
        #times
        hour=int(time.strftime('%H'))
        minute=int(time.strftime('%M'))
        time_temp=hour*(60/time_size)+math.floor(minute/time_size)
        timeblock_list.append(time_temp)
    
        #topic   1 -> CHILDREN'S FESTIVAL: SMALL BIG DREAMERS 2018
        #2-> (RE)COLLECT: THE MAKING OF OUR ART COLLECTION
        temp_topic=[]
        if int(holiday_test) > 160 and int(holiday_test)<252:
            temp_topic.append(1)
        if int(holiday_test) > 131 and int(holiday_test)<231:
            temp_topic.append(2)
        #print(temp_topic)
        topic_list.append(temp_topic)
    
        #event-Asian Civilisations Museum
        temp_event_asian=0
        if int(holiday_test) == 104 or 107 or 110 or 117 or 118 or 122 or 128 or 131 or 145 or 146 or 159 or 166 or 173 or 181 or 182 or 186 or 187 or 209 or 226 or 237:
            temp_event_asian=1
        event_asian_list.append(temp_event_asian)
    
        #event-Peninsula Shopping Centre Singapore
        temp_event_mall=0
        if int(holiday_test) == 129 or 176 or 206 or 220:
            temp_event_mall=1
        event_mall_list.append(temp_event_mall)
    dict_time['timeblock']=timeblock_list     
    dict_time['weather']=weather_list      
    dict_time['holiday']=holiday_list
    dict_time['weekday']=time_weekday
    dict_time['time']=time_list
    dict_time['topic']=topic_list
    dict_time['event_asian']=event_asian_list
    dict_time['event_mall']=event_mall_list
    #print(dict_time)
    return dict_time