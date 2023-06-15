# Imports
# -----------------------------------------------------------
from scipy.sparse import data
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamlitDjango.settings')
application = get_wsgi_application()


def run_authentication(username, password):
    user = authenticate(
        username = username, password = password
    )
    if user is not None: # user exists
        st.session_state['user_authenticated'] = True
        # make sure not to store passwords
        del username
        del password
    else:
        st.session_state['user_authenticated'] = False
    # Using the currently experimental rerun function to re-render the page
    try:
        st.experimental_rerun()
    except Exception as e:
        print("Experimental rerun error:", e)


def render_auth_form():
    with st.form('AuthForm'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button(label="Login")
    if login_button:
        run_authentication(username, password)
        del username
        del passwords


def render_main_app():
    # sns.set_theme()
    # -----------------------------------------------------------

    # Helper functions
    # -----------------------------------------------------------
    # Load data from external source
    @st.cache_data
    def load_data():
        df = pd.read_csv(
            "https://raw.githubusercontent.com/ThuwarakeshM/PracticalML-KMeans-Election/master/voters_demo_sample.csv"
        )
        return df


    df = load_data()


    def run_kmeans(df, n_clusters=2):
        kmeans = KMeans(n_clusters, random_state=0, n_init=10).fit(df[["Age", "Income"]])

        fig, ax = plt.subplots(figsize=(16, 9))

        ax.grid(False)
        ax.set_facecolor("#FFF")
        ax.spines[["left", "bottom"]].set_visible(True)
        ax.spines[["left", "bottom"]].set_color("#4a4a4a")
        ax.tick_params(labelcolor="#4a4a4a")
        ax.yaxis.label.set(color="#4a4a4a", fontsize=20)
        ax.xaxis.label.set(color="#4a4a4a", fontsize=20)
        # --------------------------------------------------

        # Create scatterplot
        ax = sns.scatterplot(
            ax=ax,
            x=df.Age,
            y=df.Income,
            hue=kmeans.labels_,
            palette=sns.color_palette("colorblind", n_colors=n_clusters),
            legend=None,
        )

        # Annotate cluster centroids
        for ix, [age, income] in enumerate(kmeans.cluster_centers_):
            ax.scatter(age, income, s=200, c="#a8323e")
            ax.annotate(
                f"Cluster #{ix+1}",
                (age, income),
                fontsize=25,
                color="#a8323e",
                xytext=(age + 5, income + 3),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#a8323e", lw=2),
                ha="center",
                va="center",
            )

        return fig


    # -----------------------------------------------------------

    # SIDEBAR
    # -----------------------------------------------------------
    sidebar = st.sidebar
    df_display = sidebar.checkbox("Display Raw Data", value=True)

    n_clusters = sidebar.slider(
        "Select Number of Clusters",
        min_value=2,
        max_value=10,
    )

    sidebar.write(
        """
        Hey friend!It seems we have lots of common interests. 

        I'd love to connect with you on 
        - [LinkedIn](https://linkedin.com/in/thuwarakesh/)
        - [Twitter](https://www.twitter.com/thuwarakesh/)

        And please follow me on [Medium](https://thuwarakesh.medium.com/), because I write about data science.
        """
    )
    # -----------------------------------------------------------


    # Main
    # -----------------------------------------------------------
    # Create a title for your app
    st.title("Interactive K-Means Clustering")
    """
    An illustration by [Thuwarakesh Murallie](https://thuwarakesh.medium.com) for the Streamlit introduction article on Medium.
    """


    # Show cluster scatter plot
    st.write(run_kmeans(df, n_clusters=n_clusters))

    if df_display:
        st.write(df)
    # -----------------------------------------------------------


if "user_authenticated" in st.session_state: # Prior authentication attempt has been made
    
    if st.session_state["user_authenticated"]: # Authentication successful
        render_main_app()

    else: # Authentication failed
        render_auth_form()
        st.error("Incorrect authentication details")

else: # Prior authentication has not been attempted
    render_auth_form()