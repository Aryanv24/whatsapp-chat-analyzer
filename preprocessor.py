import re
import pandas as pd


def preprocess(data):
    pattern = r"\[\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2}\s?(?:AM|PM)?\]"

    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    cleaned_dates = [date.replace("\u202f", " ") for date in dates]

    cleaned_dates = [date.strip("[]") for date in cleaned_dates]

    # Convert to datetime with correct format
    df = pd.DataFrame({'user_message': messages, 'message_date': cleaned_dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p', errors='coerce')

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    df.head()

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:  # Valid split
            users.append(entry[1])  # Username
            messages.append(entry[2])  # Message content
        else:
            users.append('group_notification')  # System message
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df.head()

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
