import re
import pandas as pd

def pre_processing(data, selected_date_format):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame()
    df['user_msg'] = messages
    df['msg_Date'] = dates

    if selected_date_format == "mm/dd/yy":
        df['msg_Date'] = pd.to_datetime(df['msg_Date'], format='%m/%d/%y, %H:%M - ')

    elif selected_date_format == "dd/mm/yyyy":
        df['msg_Date'] = pd.to_datetime(df['msg_Date'], format='%d/%m/%Y, %H:%M - ')

    elif selected_date_format == "dd/mm/yy":
        df['msg_Date'] = pd.to_datetime(df['msg_Date'], format='%d/%m/%y, %H:%M - ')

    elif selected_date_format == "mm/dd/yyy":
        df['msg_Date'] = pd.to_datetime(df['msg_Date'], format='%m/%d/%Y, %H:%M - ')

    users = []
    messages = []
    for message in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('Group_Notification')
            messages.append(entry[0])

    df['Users'] = users
    df['Messages'] = messages
    df['Year'] = df['msg_Date'].dt.year
    df['Month_num'] = df['msg_Date'].dt.month
    df['Month'] = df['msg_Date'].dt.month_name()
    df['Day'] = df['msg_Date'].dt.day
    df['Day_name'] = df['msg_Date'].dt.day_name()
    df['Hour'] = df['msg_Date'].dt.hour
    df['Minutes'] = df['msg_Date'].dt.minute
    df['Specific_Date'] = df['msg_Date'].dt.date

    period = []
    for hour in df[['Day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['Period'] = period

    df.drop(columns=['user_msg'], inplace=True)
    return df
