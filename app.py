import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    show_analysis = st.sidebar.checkbox("Show Analysis")
    if show_analysis:

        # Stats Area
        num_messages, words, num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #busy user
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

     #emoji
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        # Message Search Feature
        st.title("🔍 Search Messages")

        search_query = st.text_input("Enter keyword or phrase to search:")

        if search_query:
                st.write(f"Showing results for: *{search_query}*")
                filtered_df = df[df['message'].str.contains(search_query, case=False, na=False)]

                if not filtered_df.empty:
                    st.dataframe(filtered_df[['date', 'user', 'message']])
                else:
                    st.warning("No messages found with the given keyword.")

        # Sentiment Analysis
        st.title("Sentiment Analysis")
        sentiments = helper.sentiment_analysis(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentiment Counts")
            st.write(f"**Positive Messages:** {len(sentiments['Positive'])}")
            st.write(f"**Negative Messages:** {len(sentiments['Negative'])}")
            st.write(f"**Neutral Messages:** {len(sentiments['Neutral'])}")

        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                [len(sentiments['Positive']), len(sentiments['Negative']), len(sentiments['Neutral'])],
                labels=["Positive", "Negative", "Neutral"],
                autopct="%0.2f%%",
                colors=["lightgreen", "salmon", "lightgray"]
            )
            st.pyplot(fig)

        with st.expander("✅ View Positive Messages"):
            for msg in sentiments['Positive'][:50]:
                st.markdown(f"✔️ {msg}")

        with st.expander("❌ View Negative Messages"):
            for msg in sentiments['Negative'][:50]:
                st.markdown(f"❗ {msg}")

        with st.expander("🔹 View Neutral Messages"):
            for msg in sentiments['Neutral'][:50]:
                st.markdown(f"▫️ {msg}")




