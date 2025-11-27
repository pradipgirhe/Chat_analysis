from  urlextract import  URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


exctract = URLExtract()

def fetch_stats(selected_user, df):

    # If a specific user is selected, filter the df
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Count messages
    num_messages = df.shape[0]

    # Count words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # count number of media
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    # count number of links shared
    links = []

    for message in df['message']:
        links.extend(exctract.find_urls(message))


    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):

    x = df['user'].value_counts().head()

    percent_df = (df['user'].value_counts(normalize=True) * 100).round(2)
    percent_df = percent_df.reset_index()
    percent_df.columns = ['name', 'percent']   # clean rename

    return x, percent_df

def create_word_cloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y = []

        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color="white"
    )

    temp['message'] = temp['message'].apply(remove_stopwords)

    df_wc = wc.generate(temp['message'].str.cat(sep=' '))

    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')

    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                emojis.append(c)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline



