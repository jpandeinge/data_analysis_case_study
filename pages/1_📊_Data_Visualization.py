import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


import preprocess as pp


@st.experimental_singleton
# create a class to create a plots
class Plotting:
    def __init__(self, df):
        self.df = df

    # create  a function to plot the distribution of the age
    def age_distribution(self):
        fig = px.histogram(self.df, x='age', nbins=20,
                           title='Age Distribution')
        fig.update_layout(xaxis_title='Age', yaxis_title='Count', title_x=0.5)
        return fig

    def marital_status(self):
        # plot a donut chart to show the marital status distribution
        fig = go.Figure(data=[go.Pie(labels=self.df['marital'].value_counts(
        ).index, values=self.df['marital'].value_counts().values, hole=.7)])
        fig.update_layout(
            #  title_text="Marital Status",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Marital Status', x=0.50, y=0.5, font_size=20, showarrow=False)])
        return fig

    def month(self):
        fig = px.histogram(self.df, x='month', title='Month Distribution')
        fig.update_layout(xaxis_title='Month', yaxis_title='Count', title_x=0.5)
        return fig

    # create a function to plot the distribution of the housing
    def housing(self):
        fig = go.Figure(data=[go.Pie(labels=self.df['housing'].value_counts(
        ).index, values=self.df['housing'].value_counts().values, hole=.6)])
        fig.update_layout(
            # title_text="Housing Loan",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Housing Loan', x=0.50, y=0.5, font_size=20, showarrow=False)])
        return fig

    # create a function to plot the distribution of the job
    def job(self):
        # plot the job distribution using plotly express
        fig = px.histogram(self.df, x='job', title='Job Distribution', )
        fig.update_layout(xaxis_title='Job', yaxis_title='Count', title_x=0.5)  
        return fig

    def education(self):
        fig = px.bar(self.df, x='education', y='balance', color='education', title='Contrast of Education and Balance')
        fig.update_layout(xaxis_title='Education', yaxis_title='Balance', title_x=0.5)
        return fig

    
    def balance_duration(self):
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Balance Distribution', 'Duration Distribution'))
        fig.add_trace(go.Histogram(x=self.df['balance'], ), row=1, col=1)
        fig.add_trace(go.Histogram(x=self.df['duration']), row=1, col=2)
        fig.update_layout(height=400, width=1600, title_text="Balance and Duration Distribution", title_x=0.5)
        # update the x-axis title
        fig.update_xaxes(title_text="Balance ($)", row=1, col=1)
        fig.update_xaxes(title_text="Duration (Sec)", row=1, col=2)
        # update the y-axis title
        fig.update_yaxes(title_text="Count", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        return fig



data = pp.clean_data(pp.get_data())
    
# ---------------------- SIDEBAR ----------------------
st.sidebar.subheader('Please Filter Here')

age = st.sidebar.slider(
    'Select the age range:', min_value=int(data['age'].min()), max_value=int(data['age'].max()), value=(int(data['age'].min()), int(data['age'].max())))

# balance = st.sidebar.slider(
    # 'Select the balance range:', min_value=int(data['balance'].min()), max_value=int(data['balance'].max()), value=(int(data['balance'].min()), int(data['balance'].max())))

job = st.sidebar.multiselect(
    'Select Job Type:',options=data['job'].unique(), default=data['job'].unique())

marital  = st.sidebar.multiselect(
    'Select Marital Status:',options=data['marital'].unique(), default=data['marital'].unique())

education = st.sidebar.multiselect(
    'Select Education Level:',options=data['education'].unique(), default=data['education'].unique())

default = st.sidebar.multiselect(
    'Select Default Status:',options=data['default'].unique(), default=data['default'].unique())

housing = st.sidebar.multiselect(
    'Select Housing Loan Status:',options=data['housing'].unique(), default=data['housing'].unique())

loan = st.sidebar.multiselect(
    'Select Personal Loan Status:',options=data['loan'].unique(), default=data['loan'].unique())

contact = st.sidebar.multiselect(
    'Select Contact Type:',options=data['contact'].unique(), default=data['contact'].unique())

poutcome = st.sidebar.multiselect(
    'Select Previous Outcome:',options=data['poutcome'].unique(), default=data['poutcome'].unique())


# ---------------------- QUERY ----------------------
# create a query to filter the data
query = f'age >= {age[0]} & age <= {age[1]}   & job in {job} & marital in {marital} & education in {education} & default in {default} & housing in {housing} & loan in {loan} & contact in {contact} & poutcome in {poutcome}'


# ---------------------- MAIN ----------------------

# ---------------------- ROW 1 ----------------------

row1_left_col, row1_mid_col, row1_far_right_col, row1_more_far_right_col, row1_right_col  = st.columns(5)

with row1_left_col:
    total_balance = int(data.query(query)['balance'].loc[data['balance'] >= 0].sum())
    # get the sum of the balance whose value are less than 0
    total_negative_balance = int(data.query(query)['balance'].loc[data['balance'] < 0].sum())
    total_positve_balance = total_balance + total_negative_balance
    st.metric(label="Total Balance", value=f"${total_positve_balance:,}", delta=f"${total_negative_balance:,}", delta_color='inverse')


with row1_mid_col:
    yes_total_investment = int(data.query(query)['Investment'].value_counts()['yes'])
    st.metric(label="Investment Account", value=f'{yes_total_investment:,}', delta=f'-{len(data.query(query)) - yes_total_investment:,} pp')


with row1_far_right_col:
    yes_total_savings = int(data.query(query)['Savings'].value_counts()['yes'])
    st.metric(label="Savings Account", value=f'{len(data.query(query)) - yes_total_savings:,}', delta=f'{yes_total_savings:,} pp')

with row1_more_far_right_col:
    yes_total_cheque = int(data.query(query)['Cheque'].value_counts()['yes'])
    st.metric(label="Cheque Account", value=f'{yes_total_cheque:,}', delta=f'-{len(data.query(query)) - yes_total_cheque:,} pp')

with row1_right_col:
    yes_default = int(data.query(query)['default'].value_counts()['yes'])
    st.metric(label="Default", value=f'{len(data.query(query)) - yes_default:,}', delta=f'-{yes_default:,} pp')
  


# ---------------------- ROW 2 ----------------------
st.markdown('---')
row2_left_col, row2_mid_col, row2_right_col = st.columns(3)

with row2_left_col:
    plot = Plotting(data.query(query))
    st.plotly_chart(plot.education(), use_container_width=True)

with row2_mid_col:
    st.plotly_chart(plot.month(), use_container_width=True)
    

with row2_right_col:
    st.plotly_chart(plot.marital_status(), use_container_width=True)


# ----------------------  ROW 3 ----------------------
st.markdown('---') 
row3_left_col, row3_mid_col, row3_right_col = st.columns(3)

with row3_left_col:
    st.plotly_chart(plot.age_distribution(), use_container_width=True)

with row3_mid_col:
   st.plotly_chart(plot.housing(), use_container_width=True)

with row3_right_col:
    st.plotly_chart(plot.job(), use_container_width=True)


# ----------------------  ROW 4 ----------------------
st.markdown('---')
# row4_left_col, row4_right_col = st.columns(2)

# with row4_left_col:
st.plotly_chart(plot.balance_duration(), use_container_width=True)

   

# ---------------------- FOOTER ----------------------
st.markdown('---')
st.markdown('### About')
st.markdown('This dashboard was created by [**@jpandeinge**](https://github.com/jpandeinge) using [**Streamlit**](https://streamlit.io/) and [**Plotly Express**](https://plotly.com/python/plotly-express/).')