import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Hello World! Welcome !!")
st.markdown("## Kiran's First Streamlit Dashboard")
st.title ("Sentiment Analysis of Tweets About US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets About US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze Sentiment of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze Sentiment of Tweets 🐦")

##Creating function to load dataset
DATA_URL = ("/home/rhyme/Desktop/Project/Tweets.csv")## file dataset on desktop

@st.cache(persist=True)## we dont want computation every time
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader('Show random tweets')
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
## displaying as markdown text by querying df by passing randome tweets from airline sentiments
## string comparision done; to be able to access variable- @ is put before random Tweets
## to return value we put "text" col.we only display some 'sample',so panda's sample function used
## we want to display first indexed tweet
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiments")
##dropdown list
select = st.sidebar.selectbox('Visualization type', ['Histogram','Pie Chart'], key='1')

sentiment_count = data['airline_sentiment'].value_counts()
##actual sentiments' df is prepared; tweets are stored in 'Tweets'
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
##Plotting
if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of tweets by sentiments")
    if select == "Histogram":
        fig = px.bar(sentiment_count,x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names = 'Sentiment')
        st.plotly_chart(fig)
## visualizing map
#st.map(data)
## when and where tweets being done?
st.sidebar.subheader("When and Where are users twetting from?")
hour = st.sidebar.slider("Hour of day",0, 23)
modified_data = data[data['tweet created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("###Tweets locations based in the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

## No of tweets by sentiments for each airline
st.sidebar.subheader("Breakdown airline tweets by sentiments")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United','American','Southwest','Delta','Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
    facet_col = 'airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600,width=800)
    st.plotly_chart(fig_choice)

## for wordcloud
st.sidebar.header("word cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiments?', ('positive','neutral','negative'))

if not st.sidebar.checkbox("close", True, key='3'):
    st.header('Word Cloud for %s Sentiment' % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color='white', height=640, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
