
from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import pandas as pd
from collections import Counter
import emoji
from emoji import unicode_codes
import seaborn as sns

def fetch_stats(selected_user, df):

    if selected_user != "Overall":


        df = df[df['Users']== selected_user]
    # Fetch number of messages
    num_msg = df.shape[0]

    # Fetch no. of words of messages
    words = []
    for msg in df["Messages"]:
        words.extend((msg.split(" ")))


    # Fetch number of media messages
    num_media = df[df['Messages']=='<Media omitted>\n'].shape[0]

    # Fetch number of links shared
    extractor = URLExtract()
    links = []
    for message in df['Messages']:
        links.extend(extractor.find_urls(message))

    return num_msg, len(words), num_media, len(links)

def most_active_users(df):
    x = df['Users'].value_counts().head()

    df = round((df['Users'].value_counts() / df.shape[0])*100,2).reset_index().rename(
        columns = {'index': 'name', 'Users':'Percent'})
    return x, df


def creat_wordcloud(selected_user, df):

    e_stopwords = stopwords.words('english')

    # hinglish Stopword
    hinglish = open('Hinglish_Stop_Words.txt', 'r', encoding='utf-8')
    h_stopwords = list(hinglish.read().split("\n"))

    all_stopwords = e_stopwords + h_stopwords

    if selected_user != "Overall":
        df = df[df['Users']== selected_user]

    temp = df[df['Users']!='Group_Notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    def remove_stop_words(msg):
        y = []

        for word in msg.lower().split():
            if word not in all_stopwords:
                y.append(word)
        return " ".join(y)



    wc = WordCloud(width = 500, height = 500, min_font_size=10, background_color= 'white')
    temp['Messages'] = temp['Messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Messages'].str.cat(sep=" "))
    return df_wc

#

def emoji_extraction(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users']==selected_user]

    emojies = []
    for sentense in df['Messages']:
        for emo in emoji.distinct_emoji_list(sentense):
            emojies.append(emo)
    return pd.DataFrame(Counter(emojies).most_common(len(Counter(emojies))))




def timeseries_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users']== selected_user]

    timeseries = []

    df['Month_num'] = df['msg_Date'].dt.month

    time_data = df.groupby(['Year', 'Month_num', 'Month']).count()['Messages'].reset_index()

    time = []
    for i in range(time_data.shape[0]):
        time.append(time_data['Month'][i] + ": " + str(time_data['Year'][i]))

    time_data['Time'] = time


    return time_data

def daily_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    daily_timeline = df.groupby("Specific_Date").count()['Messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    return df['Day_name'].value_counts()

def month_active_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user  != 'Overall':
        df = df[df['Users']== selected_user]

    active_heatmap = df.pivot_table(index = 'Day_name', columns='Period', values = 'Messages', aggfunc = 'count').fillna(0)
    return active_heatmap

def most_used_words(selected_user, df):
    if selected_user!= "Overall":
        df=df[df['Users']==selected_user]

    # Removing Group Notification text from Messages words
    temp_word = df[df['Messages'] != "Group_Notification" ]

    # Removing Media omitted text from Messages words
    temp_word = temp_word[temp_word['Messages'] != "Media omitted\n"]

    # Removing Hinglish and English Stopwords
    # English Stopword
    e_stopwords = stopwords.words('english')

#     # hinglish Stopword
    hinglish = open('Hinglish_Stop_Words.txt', 'r',encoding = 'utf-8')
    h_stopwords = list(hinglish.read().split("\n"))

    all_stopwords = e_stopwords + h_stopwords

    filter_words = []

    for msg in temp_word['Messages']:
        for word in msg.lower().split():
            if word not in all_stopwords:
                filter_words.append(word)


    return_df = pd. DataFrame(Counter(filter_words).most_common(20))

    return return_df

