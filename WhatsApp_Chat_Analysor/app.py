import streamlit as st
import Preprocessing
import helping_func
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.sidebar.title("WhatsApp Chat Analyzer")

# time_format = ['12 Hour', '24 Hour']
# selected_time = st.sidebar.selectbox("Select Time Format", time_format)

date_format = np.array(["mm/dd/yyyy", "dd/mm/yyyy", "mm/dd/yy", "dd/mm/yy"])
selected_date_format = st.sidebar.selectbox("Select Date Format", date_format)
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = Preprocessing.pre_processing(data, selected_date_format)

    st.dataframe(df)

    user_list = list(df['Users'].unique())
    if 'Group_Notification' in user_list:
        user_list.remove('Group_Notification')

    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t", user_list)

    if st.sidebar.button("Show Analysis"):
        msg_num, length, media_file, links_num = helping_func.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        st.title("Top Statistics")
        with col1:
            st.header("Total Messages")
            st.title(msg_num)

        with col2:
            st.header("Total Words")
            st.title(length)

        with col3:
            st.header("Total media")
            st.title(media_file)

        with col4:
            st.header("Total Links")
            st.title(links_num)

        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = helping_func.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='Green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("Word Cloud")
        wc_img = helping_func.creat_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_img)
        st.pyplot(fig)

        # most common words
        most_common_df = helping_func.most_used_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        # Emojies Analysis
        emoji_df = helping_func.emoji_extraction(selected_user, df)
        # fix, ax = plt.subplots()
        st.title("Emojies Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            flg2, ax2 = plt.subplots()
            ax2.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(flg2)

        col1, cil2 = st.columns(2)

        fig3, ax3 = plt.subplots()
        st.title('EMOJI TREND')
        ax3.bar(emoji_df[0].head(20), emoji_df[1].head(20))
        plt.xticks(rotation='vertical')
        st.title("Most Common Emoji")
        st.pyplot(fig3)

        # timeline
        timeline = helping_func.timeseries_analysis(selected_user, df)
        fig, ax = plt.subplots()
        st.title('MESSAGE TREND')
        ax.plot(timeline['Time'], timeline['Messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily analysis
        timeline = helping_func.daily_analysis(selected_user, df)
        fig, ax = plt.subplots()
        st.title('MESSAGE DAILY TREND')
        ax.plot(timeline['Specific_Date'], timeline['Messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Day Activity trend
        st.title('Activity map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            busy_day = helping_func.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active Month")
            busy_day = helping_func.month_active_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Activity')
        active_heatmap = helping_func.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(active_heatmap)
        st.pyplot(fig)
