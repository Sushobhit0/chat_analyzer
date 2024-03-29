import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import emoji
from wordcloud import WordCloud
st.sidebar.title('whatsapp chat analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')


    selected_user=st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):
        num_messages, words, num_media_messages, num_links =helper.fetch_stats(selected_user,df)

        st.title("Statistics")

        col1,col2,col3,col4 =st.columns(4)


        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)
        with col4:
            st.header('Links Shared')
            st.title(num_links)

        st.title('Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='#00563b')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2= st.columns(2)

        with col1:
            st.header('Most Active day')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Active month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Weekly Heatmap')
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)


        if selected_user == 'Overall':
            st.title('Most Active')
            x,new_df=helper.most_busy(df)
            fig,ax=plt.subplots()

            col1,col2,=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='#98fb98')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        most_common_df=helper.most_common_words(selected_user,df)

        st.dataframe(most_common_df)


        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emojis')

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct='%0.2f')
            st.pyplot(fig)



