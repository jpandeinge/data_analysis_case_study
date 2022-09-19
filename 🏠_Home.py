import pandas as pd
import streamlit as st

import preprocess as pp




def main_page():
    st.set_page_config(
        layout="wide",
        page_title="## Costa Rica Bank Dashboard",
        page_icon=":# Home 🏠",
        initial_sidebar_state="expanded",
    )

    # create four columns
    col1, col2, = st.columns(2)

    # put the data in the first column
    with col1:
        # display the image
        st.image("logo.png", width=250)

    with col2:
        # displat the page title
        st.title("## Costa Rica Bank Dashboard")

     # Set page subtitle
    st.markdown(
        """
        This dashboard shows the data drom `Costa Rica Bank`. The dashboard will show the data from the bank.
        We made an assumption that the target variable is the `default` column. 
        """
        # The modeling will be done using two models, `XGBoost` and `Random Forest`.
        # The model will be evaluated using `ROC AUC` and `Accuracy`.
    )

    st.write("#### Data")

    
    # load the data from the preprocess.py file
    df = pp.get_data()
    st.dataframe(df.head())


    # create another two columns
    col3, col4, col5 = st.columns(3)

    with col3:
        st.write("#### Data Description")
         # write the descrbbrion of all the columns in the data
        st.dataframe(df.describe())

    with col4:
        st.write("#### Data Information")
        # write the information of all the columns in the data
        st.markdown(
            """
            - `age`:	Age of a person
            - `job`:	Type of job 
            - `marital`:	Marital status
            - `education`:	Education
            - `default`:	Has credit in arrears? 
            - `balance`:	Customer credit balance
            - `housing`:	Has housing loan? 
            - `loan`:	Has personal loan? 
            - `contact`:	Contact communication type
            - `day`:	Last contact month of year
            - `month`:	Last contact day of the week 
            """
        )


    with col5:
        st.write()
        # write the information of all the columns in the data
        st.markdown(
            """
            - `duration`:	Last contact duration, in seconds 
            - `campaign`:	Number of contacts performed during this campaign and for this client 
            - `pdays`:	Number of days that passed by after the client was last contacted from a previous campaign
            - `previous`:	Number of contacts performed before
            - `poutcome`:	Outcome of the previous marketing campaign 
            - `Investment`: 	Has an investment?
            - `Savings` 	Has a savings product?
            - `Cheque` 	Has a cheque account? 
            """
        )



def data_visualization():
    st.markdown("## Data Visualization 📊")
    st.sidebar.markdown("# Data Visualization 📊")

    # add a selectbox to the sidebar for the userto select the page
    page_names_to_funcs = {
        "Home": main_page,
        "Data Visualization": data_visualization,
        
    }

    selected_page = st.sidebar.selectbox("Menu", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()


page_names_to_funcs = {
    "Home": main_page,
    "Data Visualization": data_visualization,
}


if __name__ == "__main__":
    main_page()

    # selected_page = st.sidebar.selectbox("Menu", page_names_to_funcs.keys())
    # page_names_to_funcs[selected_page]()
