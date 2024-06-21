import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from millify import millify
import time
from PIL import Image



#'C:/Users/ADITI/PycharmProjects/Sales_Dashboard/.venv/all_sales_data_cleaned1.csv'
# streamlit run C:/Users/ADITI/PycharmProjects/Sales_Dashboard/.venv/app.py
# http://localhost:8501
# NetworkURL: http: // 192.168.1.3: 8501

# loading the dataset
df = pd.read_csv('data_all_sales_data_cleaned1.csv')  


# setting the page layout
st.set_page_config(layout='wide', page_title='Sales Analysis')



# converting date columns to relevant data types
df['order_date'] = pd.to_datetime(df['order_date'])
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.time
df['month_name'] = df['date'].dt.strftime('%B')

st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Select a page', ['Overall analysis', 'Analysis by city', 'About the project'])

def home_page():
    import datetime
    st.title('Overall :red[Sales] Analysis')
    st.markdown("<br><br>", unsafe_allow_html=True)
    col3,col4 = st.columns([3, 1])
    with col3:

        tab1,tab2 = st.tabs(['Orders','Quarter Wise Revenue'])
        with tab1:
            st.subheader(':gray[Orders By Date]',divider='gray')
            start_date = st.date_input('Start date',min_value=datetime.date(2019, 1, 1),max_value=datetime.date(2020, 1, 1))
            end_date = st.date_input('End date', min_value=datetime.date(2019, 1, 1),max_value=datetime.date(2020, 1, 1))
            with st.container(height=450):  #table 1
                table1 = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)].groupby('product')[['quantity_ordered','revenue']].sum().reset_index().sort_values(by = 'product')
                st.dataframe(table1,hide_index=True,use_container_width=True)

        with tab2:
            st.subheader(':gray[Quarter Wise Revenue]',divider='gray')
            quarterly_revenue = df.groupby(df['date'].dt.quarter)['revenue'].sum().reset_index()
            quarterly_revenue['quarter_label'] = ['Q1', 'Q2', 'Q3', 'Q4']
            # Create the line chart using Plotly graph objects
            fig8 = go.Figure()

            fig8.add_trace(go.Scatter(
                x=quarterly_revenue['quarter_label'],
                y=quarterly_revenue['revenue'],
                mode='lines+markers',
                name='Revenue', line=dict(color='red')
            ))

            fig8.update_layout(
                title={'text':'Quarter-wise Revenue Growth','xanchor': 'center',
                    'yanchor': 'top','y': 0.9,
                    'x': 0.5,},
                xaxis_title='Quarter',
                yaxis_title='Revenue',
                # xaxis=dict(tickangle=180),
                template='plotly_white'
            )
            with st.container(height=500,border=True):
                st.plotly_chart(fig8)

        # Revenue graph
        st.markdown('<br><br>',unsafe_allow_html=True)
        tab3,tab4 = st.tabs(['Revenue By Category','Orders by Product'])
        with tab3:
            st.subheader(':gray[Revenue By Product Category]', divider='gray')
            state = sorted(df['state'].unique().tolist())
            state.append('All states')
            selected_state = st.selectbox('Select a state', state)

            if selected_state == 'All states':
                temp_c = df.groupby('product_category')['quantity_ordered'].sum().reset_index()
                temp_r = df.groupby('product_category')['revenue'].sum().reset_index()



            elif selected_state != 'All states':
                temp_c = df[df['state']==selected_state].groupby('product_category')['quantity_ordered'].sum().reset_index()
                temp_r = df[df['state']==selected_state].groupby('product_category')['revenue'].sum().reset_index()
                pass
            else:
                pass

            temp_cr = pd.merge(temp_c, temp_r, on='product_category')
            with st.container(height=500):  #graph 2
                bar = go.Bar(
                    x=temp_cr['product_category'],
                    y=temp_cr['revenue'],
                    name='revenue',
                    marker_color='blue'
                )

                # Create the line chart trace
                line = go.Scatter(
                    x=temp_cr['product_category'],
                    y=temp_cr['quantity_ordered'],
                    name='# orders',
                    yaxis='y2',  # Specify that this trace uses the secondary y-axis
                    mode='lines+markers',
                    line=dict(color='red')
                )

                # Create the figure
                fig6 = go.Figure()

                # Add both bar chart and line chart traces to the figure
                fig6.add_trace(bar)
                fig6.add_trace(line)

                # Update layout to beautify the graph
                fig6.update_layout(
                    title={
                        'text': 'Revenue By Product Category',
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Product Category',
                    yaxis_title='Revenue',
                    yaxis2=dict(
                        title='# Orders',
                        overlaying='y',
                        side='right'
                    ),
                    legend=dict(
                        x=0.9,  # Adjust x position towards the center
                        y=1.0,  # Adjust y position to the top
                        xanchor='center',
                        yanchor='top'
                    ),
                    # legend_title='Legend',
                    barmode='group',
                    xaxis_tickangle=90,  # Rotate x-axis labels to 90 degrees
                    xaxis=dict(
                        tickmode='array',
                        ticktext=temp_cr['product_category'],
                        tickvals=temp_cr['product_category']
                    ),
                    font=dict(
                        # family="Arial, sans-serif",
                        size=12,
                        color="black"
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=50, r=50, t=100, b=150)
                )

                st.plotly_chart(fig6)
        with tab4:
            st.subheader(':gray[Sales For A Product]',divider='gray')
            products_list = sorted(df['product'].unique().tolist())
            product = st.selectbox('select a product',products_list)

            temp8 = df[df['product'] == product].groupby('month_name')[
                'quantity_ordered'].sum().reset_index()
            unique_months = df['date'].dt.strftime('%B').unique().tolist()
            month_name_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                                    'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

            temp8['month_num'] = temp8['month_name'].map(month_name_to_number)
            temp8.sort_values(by='month_num', inplace=True)
            temp8.set_index(temp8['month_num'], inplace=True)
            with st.container(height=500):

                fig9 = go.Figure()

                fig9.add_trace(go.Scatter(
                    x=temp8['month_name'],
                    y=temp8['quantity_ordered'],
                    mode='lines+markers',
                    name='# orders', line=dict(color='red')
                ))

                fig9.update_layout(title={
                        'text': 'Product Wise Sales',
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    }
                    ,
                    xaxis_title='Month',
                    yaxis_title='# orders',
                    xaxis=dict(tickangle=90),
                    template='plotly_white'
                )
                st.plotly_chart(fig9)

          #metric ###
        # st.markdown('<br><br>',unsafe_allow_html=True)
        # st.subheader(':gray[Highest|Lowest Selling products State Wise]',divider='gray')
        # col5,col6 = st.columns(2)
        # with col5:
        #     with st.container(height=130, border=True):  # metric 3
        #         # HIghest selling product in a state
        #         if selected_state == 'All':
        #          high = df[df['state'] == selected_state].groupby('product')['quantity_ordered'].sum().sort_values(ascending=False).head(1).index[0]
        #         else:
        #             high = df.groupby('product')['quantity_ordered'].sum().sort_values(ascending=False).head(1).index[0]
        #
        #         st.metric(label="Highest Most Product", value=high)
        #
        # with col6:
        #     with st.container(height=130, border=True):
        #         # Lowest selling product in a state
        #         if selected_state == 'All':
        #             low = df[df['state'] == selected_state].groupby('product')['quantity_ordered'].sum().sort_values(ascending=True).head(1).index[0]
        #         else:
        #             low = df.groupby('product')['quantity_ordered'].sum().sort_values(ascending=True).head(1).index[0]
        #
        #         st.metric(label="Lowest Selling Product", value=low) ###

        # Revenue by State Graph
        st.markdown('<br><br>',unsafe_allow_html=True)
        st.subheader(':gray[Revenue By State]', divider='gray')

        unique_months = df['date'].dt.strftime('%B').unique().tolist()
        month_name_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                                'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                                }
        sorted_months2 = sorted(unique_months, key=lambda month: month_name_to_number[month])
        sorted_months2.append('All')
        month2 = st.selectbox("Select a month", sorted_months2)

        chart_sel = st.selectbox('select a chart',['map','bar'])



        if chart_sel == 'bar':
            if month2 == 'All':
                rev_state = df.groupby('state')['revenue'].mean()
            else:
                rev_state = df[df['month_name'] == month2].groupby('state')['revenue'].mean()

            with st.container(height=450, border=True):  # graph
                bar = go.Bar(
                    x=rev_state.index,
                    y=rev_state.values,
                    name='revenue',
                    marker_color='blue'
                )

                # Create the figure
                fig7 = go.Figure()

                # Add bar chart to the figure
                fig7.add_trace(bar)

                # Update layout to beautify the graph
                fig7.update_layout(
                    title={
                        'text': 'Revenue By State',
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='state',
                    yaxis_title='revenue',
                    legend_title='Legend',
                    barmode='group',
                    xaxis_tickangle=90,  # Rotate x-axis labels to 90 degrees
                    xaxis=dict(
                        tickmode='array',
                        ticktext=rev_state.index,
                        tickvals=rev_state.index
                    ),
                    font=dict(
                        # family="Arial, sans-serif",
                        size=12,
                        color="black"
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=50, r=50, t=100, b=150)
                )
                st.plotly_chart(fig7)
        else:

            if month2 == 'All':
                temp6 = df.groupby('state')['revenue'].mean().reset_index()
            elif month2 != 'All':
                temp6 = df[df['month_name'] == month2].groupby('state')['revenue'].mean().reset_index()


            # Mapping of state names to their abbreviations
            state_abbreviations = {
                'Alabama': 'AL',
                'Alaska': 'AK',
                'Arizona': 'AZ',
                'Arkansas': 'AR',
                'California': 'CA',
                'Colorado': 'CO',
                'Connecticut': 'CT',
                'Delaware': 'DE',
                'Florida': 'FL',
                'Georgia': 'GA',
                'Hawaii': 'HI',
                'Idaho': 'ID',
                'Illinois': 'IL',
                'Indiana': 'IN',
                'Iowa': 'IA',
                'Kansas': 'KS',
                'Kentucky': 'KY',
                'Louisiana': 'LA',
                'Maine': 'ME',
                'Maryland': 'MD',
                'Massachusetts': 'MA',
                'Michigan': 'MI',
                'Minnesota': 'MN',
                'Mississippi': 'MS',
                'Missouri': 'MO',
                'Montana': 'MT',
                'Nebraska': 'NE',
                'Nevada': 'NV',
                'New Hampshire': 'NH',
                'New Jersey': 'NJ',
                'New Mexico': 'NM',
                'New York': 'NY',
                'North Carolina': 'NC',
                'North Dakota': 'ND',
                'Ohio': 'OH',
                'Oklahoma': 'OK',
                'Oregon': 'OR',
                'Pennsylvania': 'PA',
                'Rhode Island': 'RI',
                'South Carolina': 'SC',
                'South Dakota': 'SD',
                'Tennessee': 'TN',
                'Texas': 'TX',
                'Utah': 'UT',
                'Vermont': 'VT',
                'Virginia': 'VA',
                'Washington': 'WA',
                'West Virginia': 'WV',
                'Wisconsin': 'WI',
                'Wyoming': 'WY'
            }

            # Map the state names to their abbreviations
            temp6['state_abbrev'] = temp6['state'].map(state_abbreviations)
            with st.container(height=500):
                fig9 = px.choropleth(temp6,
                                     locations='state_abbrev',
                                     locationmode='USA-states',
                                     color='revenue',
                                     scope='usa',
                                     color_continuous_scale='Blues',
                                     hover_name='state',
                                     hover_data={'state_abbrev': False, 'revenue': True},
                                     labels={'revenue': 'Revenue ($M)'})
                                     # ,title='Revenue by State')
                fig9.update_layout(title={'text':'Revenue By State','x':0.5,'y':0.9,'xanchor':'center','yanchor':'top'})
                st.plotly_chart(fig9)






    qty_by_month = df.groupby('month_name')['quantity_ordered'].sum().sort_values(ascending=False).reset_index()
    unique_months = df['date'].dt.strftime('%B').unique().tolist()
    month_name_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    qty_by_month['month_num'] = qty_by_month['month_name'].map(month_name_to_number)
    qty_by_month.sort_values(by='month_num', inplace=True)
    qty_by_month.set_index(qty_by_month['month_num'], inplace=True)

    growth_percentage = [None]  # First month has no previous month to compare to

    # Calculate growth for each month compared to the previous month
    for i in range(1, len(qty_by_month)):
        prev_qty = qty_by_month.iloc[i - 1]['quantity_ordered']
        current_qty = qty_by_month.iloc[i]['quantity_ordered']
        growth = ((current_qty - prev_qty) / prev_qty) * 100
        growth_percentage.append(growth)

    qty_by_month['growth_percentage'] = growth_percentage

    rev_by_month = df.groupby('month_name')['revenue'].sum().sort_values(ascending=False).reset_index()
    unique_months = df['date'].dt.strftime('%B').unique().tolist()
    month_name_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    rev_by_month['month_num'] = rev_by_month['month_name'].map(month_name_to_number)
    rev_by_month.sort_values(by='month_num', inplace=True)
    rev_by_month.set_index(rev_by_month['month_num'], inplace=True)

    rev_growth_percentage = [None]  # First month has no previous month to compare to

    # Calculate growth for each month compared to the previous month
    for i in range(1, len(rev_by_month)):
        prev_rev = rev_by_month.iloc[i - 1]['revenue']
        current_rev = rev_by_month.iloc[i]['revenue']
        growth2 = ((current_rev - prev_rev) / prev_rev) * 100
        rev_growth_percentage.append(growth2)

    rev_by_month['growth_percentage'] = rev_growth_percentage
    with col4:
        st.subheader(':gray[Metrics]',divider='gray')
        # Filter to choose the month
        filter_month = st.selectbox("Select a month", qty_by_month['month_name'])

        # Get the data for the selected month
        selected_data = qty_by_month[qty_by_month['month_name'] == filter_month].iloc[0]
        with st.container(height=130, border=True):  #metric 1
           # Display the metric
            st.metric(
                label="Quantity Ordered",
                value=f"{millify(selected_data['quantity_ordered'], precision = 2)} units",
                delta=f"{selected_data['growth_percentage']:.2f} %" if selected_data[
                                                                           'growth_percentage'] is not None else "N/A",help=''':red[This metric displays total quantity ordered each month and
                                                                                                                         shows the growth percentage month by month.]''')
        with st.container(height=130, border=True):  #metric 2
            selected_data2 = rev_by_month[rev_by_month['month_name'] == filter_month].iloc[0]
            # Display the metric
            st.metric(
                label="Total Revenue",
                value=f"$ {millify(selected_data2['revenue'],precision = 2)}",
                delta=f"{selected_data2['growth_percentage']:.2f} %" if selected_data2[
                                                                         'growth_percentage'] is not None else "N/A",help=''':red[This metric displays total revenue and shows the growth percentage month by month.]''')

        uni_cust = df.groupby('month_name')['order_id'].nunique().sort_values(ascending=False).reset_index()
        uni_cust['month_num'] = uni_cust['month_name'].map(month_name_to_number)
        uni_cust.sort_values(by='month_num', inplace=True)
        uni_cust.set_index(uni_cust['month_num'], inplace=True)

        cust_growth_percentage = [None]  # First month has no previous month to compare to

        # Calculate growth for each month compared to the previous month
        for i in range(1, len(uni_cust)):
            prev_cust = uni_cust.iloc[i - 1]['order_id']
            current_cust = uni_cust.iloc[i]['order_id']
            growth3 = ((current_cust - prev_cust) / prev_cust) * 100
            cust_growth_percentage.append(growth3)

        uni_cust['growth_percentage'] = cust_growth_percentage

        selected_data = uni_cust[uni_cust['month_name'] == filter_month].iloc[0]
        with st.container(height=130,border=True):
            st.metric(
                label="Unique Customers",
                value=f"{millify(selected_data['order_id'],precision = 2)}",
                delta=f"{selected_data['growth_percentage']:.2f} %" if selected_data[
                                                                           'growth_percentage'] is not None else "N/A",
                help=''':red[This metric displays total number of unique customers each month and shows the growth percentage month by month.]''')









def page1():
    st.title('Analysis By :blue[City]')
    st.sidebar.title('Filter Options')
    cities = sorted(df['city'].unique().tolist())
    cities.append('All cities')
    selected_cities = st.sidebar.selectbox('City', cities)

    unique_months = df['date'].dt.strftime('%B').unique().tolist()
    month_name_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                            }
    sorted_months = sorted(unique_months, key=lambda month: month_name_to_number[month])
    sorted_months.append('All')
    # filter3 = st.sidebar.multiselect('Month', sorted_months)

    st.markdown("<br><br>",unsafe_allow_html=True)
    st.subheader(':gray[MoM Revenue Growth]',divider='gray')

    if selected_cities == 'All cities':
        temp = df.groupby(df['date'].dt.strftime('%B'))['revenue'].sum().reset_index()
    else:
        temp = df[df['city'].str.contains(selected_cities)].groupby(df['date'].dt.strftime('%B'))['revenue'].sum().reset_index()

    temp['month_number'] = temp['date'].map(month_name_to_number)
    temp = temp.sort_values('month_number')

    with st.container(height=500,border=True):
        bar = go.Bar(x=temp['date'], y=temp['revenue'], name='Revenue', marker_color='blue')
        line = go.Scatter(x=temp['date'], y=temp['revenue'], name='Revenue Trend', mode='lines+markers', marker_color='red')
        fig1 = go.Figure()
        fig1.add_trace(bar)
        fig1.add_trace(line)
        fig1.update_layout(
            title={'text':'Monthly Sales Revenue ({})'.format(selected_cities),'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Month',
            yaxis_title='Revenue',
            legend_title='Legend',
            barmode='group',xaxis_tickangle=90,
        )
        st.plotly_chart(fig1)

    st.markdown("<br><br>", unsafe_allow_html=True)  # Add spacing
    st.subheader(':gray[Orders According To Time]',divider='gray')
    #Adding a month filter to the graphs
    selected_month2 = st.selectbox('Month', sorted_months)

    if selected_cities == 'All cities' and selected_month2 != 'All':
        temp1 = df[df['month_name']== selected_month2].groupby(df['time_category'])['order_id'].count()
    elif selected_cities == 'All cities' and selected_month2 == 'All':
        temp1 = df.groupby(df['time_category'])['order_id'].count()
    elif selected_cities != 'All cities' and selected_month2 != 'All':
        temp1 = df[(df['city'] == selected_cities) & (df['month_name']== selected_month2)].groupby(df['time_category'])['order_id'].count()
    elif selected_cities != 'All cities' and selected_month2 == 'All':
        temp1 = df[df['city'] == selected_cities].groupby(df['time_category'])['order_id'].count()
    else:
        pass
        # temp1 = df[df['city'].str.contains(selected_cities)].groupby(df['time_category'])['order_id'].count()

    col1,col2 = st.columns([2,1])

    with col1:
        if selected_cities == 'All cities' and selected_month2 != 'All':
            t = df[df['month_name'] == selected_month2].groupby(df['order_date'].dt.hour)['order_id'].count()
        elif selected_cities == 'All cities' and selected_month2 == 'All':
            t = df.groupby(df['order_date'].dt.hour)['order_id'].count()
        elif selected_cities != 'All cities' and selected_month2 != 'All':
            t = df[(df['city'] == selected_cities) & (df['month_name'] == selected_month2)].groupby(
                df['order_date'].dt.hour)['order_id'].count()
        elif selected_cities != 'All cities' and selected_month2 == 'All':
            t = df[df['city'] == selected_cities].groupby(df['order_date'].dt.hour)['order_id'].count()
        else:
            pass
            # t = df[df['city'].str.contains(selected_cities)].groupby(df['order_date'].dt.hour)['order_id'].count()
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(x=t.index, y=t.values, name='Revenue Trend', mode='lines+markers', marker_color='red'))
        fig2.update_layout(
            title={
                'text': '#Orders Vs Time ({})'.format(
                    'All Cities' if selected_cities == 'All cities' else selected_cities),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Time (Hour)',
            yaxis_title='# Orders',
            legend_title='Legend',
            barmode='group'
        )
        st.plotly_chart(fig2)

        colors = ['#0096FF', '#00008B', 'blue', '#0F52BA'] ######
        # Calculate the pull values to highlight the highest percentage piece
        pull_values = [0.1 if v == max(temp1.values) else 0 for v in temp1.values]
        # Create the pie chart trace
        fig3 = go.Figure(data=[go.Pie(values=temp1.values, labels=temp1.index, hole=0.4,pull=pull_values)])

        # Update the layout to beautify the chart
        fig3.update_layout(
            title={
                'text': 'Orders According To Time ({})'.format(selected_cities),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
                },
                legend_title='Legend',
                showlegend=True,
                annotations=[
                    dict(
                        text='Orders',
                        x=0.5,
                        y=0.5,
                        font_size=20,
                        showarrow=False
                    )
                ],
                font=dict(
                    size=14,
                    color='black'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=50, r=50, t=100, b=50)
            )

        # Customize the pie chart
        fig3.update_traces(
                hoverinfo='label+percent+name',
                textinfo='label+percent',
                textfont_size=14,
                marker=dict(
                    colors=colors,  # Use the defined blue-red color theme
                    line=dict(color='#FFFFFF', width=2)
                )
            )

        # Show the chart
        st.plotly_chart(fig3) #########

    with col2:

            #Creating a peak time metric
            if selected_cities == 'All cities' and selected_month2 != 'All':
                time = str(df[df['month_name'] == selected_month2].groupby(df['order_date'].dt.hour)['order_id'].count().sort_values(ascending=False).head(1).index[0])

            elif selected_cities == 'All cities' and selected_month2 == 'All':
                time = str(df.groupby(df['order_date'].dt.hour)['order_id'].count().sort_values(ascending=False).head(1).index[0])

            elif selected_cities != 'All cities' and selected_month2 != 'All':
                time = str(df[(df['city'] == selected_cities) & (df['month_name'] == selected_month2)].groupby(df['order_date'].dt.hour)['order_id'].count().sort_values(ascending=False).head(1).index[0])

            elif selected_cities != 'All cities' and selected_month2 == 'All':
                time = str(df[df['city'] == selected_cities].groupby(df['order_date'].dt.hour)['order_id'].count().sort_values(ascending=False).head(1).index[0])
            else:
                pass
            peak_time = time + ":00 {}".format('pm' if int(time) >= 12 else 'am')

            st.markdown('<br><br>',unsafe_allow_html=True)
            with st.container(height=100, border=True):
                    st.metric(':gray-background[:red[Peak Time]]',value=peak_time)

    st.markdown("<br><br>", unsafe_allow_html=True)  # Add spacing
    tab5,tab6 = st.tabs(['Pairs Of Products','Products'])
    with tab5:
        st.subheader(':gray[Most Ordered Pairs Of Products]',divider='gray')
        if selected_cities == 'All cities':
            temp = df[df.duplicated(subset=['order_id'], keep=False)]
        else:
            temp = df[df['city'] == selected_cities][df.duplicated(subset=['order_id'], keep=False)]
        temp['pairs'] = temp.groupby('order_id')['product'].transform(lambda x: ','.join(x))
        temp.drop_duplicates(subset=['order_id'], inplace=True)

        from itertools import combinations
        from collections import Counter

        count = Counter()
        for row in temp['pairs']:
            row_list = row.split(',')
            count.update(Counter(combinations(row_list, 2)))

        top_10_pairs = count.most_common(10)
        d = pd.DataFrame(top_10_pairs, columns=['Pair', 'Count'])
        d['Pair'] = d['Pair'].apply(lambda x: ','.join(x))

        with st.container(height=500,border=True):
            bar = go.Bar(x=d['Pair'], y=d['Count'], name='#orders per pair', marker_color='blue')
            fig4 = go.Figure()
            fig4.add_trace(bar)
            fig4.update_layout(
                title={
                    'text': 'Items Bought Together ({})'.format('All cities' if selected_cities == 'All cities' else selected_cities),
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title='Products',
                yaxis_title='# Orders',
                legend_title='Legend',
                barmode='group',
                xaxis_tickangle=90,
                xaxis=dict(tickmode='array', ticktext=d['Pair'], tickvals=d['Pair']),
                font=dict(family="Arial, sans-serif", size=10, color="black"),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=30, r=30, t=50, b=100),
                height=600,
            )
            st.plotly_chart(fig4)
        with tab6:
            st.subheader(':gray[Most Ordered Product]',divider='gray')
            if selected_cities == 'All cities':
                temp10 = df.groupby('product')['quantity_ordered'].sum().sort_values(ascending=False)
            else:
                temp10 = df[df['city']==selected_cities].groupby('product')['quantity_ordered'].sum().sort_values(ascending=False)

            with st.container(height=500):
                bar = go.Bar(
                    x=temp10.index,
                    y=temp10.values,
                    name='#orders',
                    marker_color='blue'
                )

                # Create the figure
                fig10 = go.Figure()

                # Add bar chart to the figure
                fig10.add_trace(bar)

                # Update layout to beautify the graph
                fig10.update_layout(
                    title={
                        'text': '#Orders Product Wise ({})'.format(selected_cities),
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title='Product',
                    yaxis_title='# Orders',
                    legend_title='Legend',
                    barmode='group',
                    xaxis_tickangle=90,  # Rotate x-axis labels to 90 degrees
                    xaxis=dict(
                        tickmode='array',
                        ticktext=temp10.index,
                        tickvals=temp10.index
                    ),
                    font=dict(
                        # family="Arial, sans-serif",
                        size=12,
                        color="black"
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=50, r=50, t=100, b=150)
                )
                st.plotly_chart(fig10)


    #Most bought product categories

    st.markdown("<br><br>", unsafe_allow_html=True)  # Add spacing
    # st.markdown(html_code, "<br><br>", unsafe_allow_html=True)
    st.subheader(':gray[Number Of Orders Vs Price]',divider='gray')
    # Adding a month filter to the graph
    unique_months = df['date'].dt.strftime('%B').unique().tolist()
    # Map month names to month numbers
    month_name_to_number = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                            }
    # Sort month names based on their corresponding month numbers
    sorted_months = sorted(unique_months, key=lambda month: month_name_to_number[month])
    sorted_months.append('All')
    selected_month = st.selectbox('Select a month', sorted_months)

    if selected_cities == 'All cities' and selected_month != 'All':
        t1 = df[df['month_name']==selected_month].groupby('product_category')['product_category'].value_counts().reset_index()
        t2 = df[df['month_name']==selected_month].groupby('product_category')['price_each'].mean().reset_index()
        temp_df = pd.merge(t1, t2, on='product_category')
    elif selected_cities == 'All cities' and selected_month == 'All':
        t1 = df.groupby('product_category')['product_category'].value_counts().reset_index()
        t2 = df.groupby('product_category')['price_each'].mean().reset_index()
        temp_df = pd.merge(t1, t2, on='product_category')


    elif selected_cities != 'All cities' and selected_month != 'All':
        t1 = df[(df['city']== selected_cities) & (df['month_name']==selected_month)].groupby('product_category')['product_category'].value_counts().reset_index()
        t2 = df[(df['city']== selected_cities) & (df['month_name']==selected_month)].groupby('product_category')['price_each'].mean().reset_index()
        temp_df = pd.merge(t1, t2, on='product_category')

    elif selected_cities != 'All cities' and selected_month == 'All':
        t1 = df[df['city'] == selected_cities].groupby('product_category')['product_category'].value_counts().reset_index()
        t2 = df[df['city'] == selected_cities].groupby('product_category')['price_each'].mean().reset_index()
        temp_df = pd.merge(t1, t2, on='product_category')
    else:
        pass
    with st.container(height=500,border=True):
        bar = go.Bar(
            x=temp_df['product_category'],
            y=temp_df['count'],
            name='# orders',
            marker_color='blue'
        )

        # Create the line chart trace
        line = go.Scatter(
            x=temp_df['product_category'],
            y=temp_df['price_each'],
            name='Price',
            yaxis='y2',  # Specify that this trace uses the secondary y-axis
            mode='lines+markers',
            line=dict(color='red')
        )

        # Create the figure
        fig5 = go.Figure()

        # Add both bar chart and line chart traces to the figure
        fig5.add_trace(bar)
        fig5.add_trace(line)

        # Update layout to beautify the graph
        fig5.update_layout(
            title={
                'text': 'Most Bought Product Category ({})'.format('All Cities' if selected_cities=='All cities' else selected_cities),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Product Category',
            yaxis_title='# Orders',
            yaxis2=dict(
                title='Price',
                overlaying='y',
                side='right'
            ),####
            legend=dict(
                x=1.0,  # Adjust x position towards the center
                y=1.3,  # Adjust y position to the top
                xanchor='center',
                yanchor='top'
            ),
            legend_title='Legend',
            barmode='group',
            xaxis_tickangle=90,  # Rotate x-axis labels to 90 degrees
            xaxis=dict(
                tickmode='array',
                ticktext=temp_df['product_category'],
                tickvals=temp_df['product_category']
            ),
            font=dict(
                # family="Arial, sans-serif",
                size=12,
                color="black"
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=50, t=100, b=150)
        )
        st.plotly_chart(fig5)


def page2():
    st.title(':green[About] The Project')
    st.markdown('<br><br>', unsafe_allow_html=True)

    st.subheader(':gray[Welcome!]',divider='gray')
    st.markdown('''Welcome to my Sales Data Analysis Project, a comprehensive platform built using Streamlit and Python. This project is designed to provide insightful analysis and metrics from the 2019 USA sales data on a 
        month-by-month basis. My aim is to transform raw sales data into meaningful visualizations and analytics
        that can help businesses and analysts make informed decisions.''')
    st.markdown('<br><br>',unsafe_allow_html=True)

    st.subheader(':gray[Project Overview]',divider='gray')
    st.markdown("""This project leverages the powerful capabilities of Streamlit, a user-friendly framework for creating web 
    applications in Python, to present a detailed examination of the sales trends throughout 2019. By utilizing a rich dataset 
    that encompasses sales figures from various regions across the USA, I offer a range of analytical tools and visualizations 
    to uncover trends, patterns, and key insights.""")
    st.markdown('<br><br>', unsafe_allow_html=True)

    st.subheader(':gray[Features and Analysis]',divider='gray')
    st.markdown("""
        - **Interactive Visualizations:** Dive into a variety of charts and graphs that illustrate monthly sales performance, regional comparisons, and product category trends.
        - **Key Metrics:** Explore essential metrics such as total sales, average sales per month, and growth rates to understand the overall sales landscape.
        - **Regional Analysis:** Gain insights into sales distribution across different states and cities, highlighting top-performing areas and potential markets.
        - **Time Series Analysis:** Examine sales trends over time with line graphs and other temporal visualizations to identify seasonal effects and anomalies.
        - **Product Insights:** Analyze the performance of different product categories to determine which products are driving sales and which may need strategic adjustments.
        """)
    st.markdown('<br><br>', unsafe_allow_html=True)

    st.subheader(':gray[Tools and Technologies]',divider='gray')
    st.markdown("""
        This project is powered by:
        - **Streamlit:** For creating a highly interactive and user-friendly web application.
        - **Python:** Utilizing its robust libraries such as Pandas for data manipulation, Plotly for visualizations, and NumPy for numerical operations.
        - **Data Source:** A comprehensive dataset of USA sales data for the year 2019, meticulously compiled on a monthly basis.
        """)
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.subheader(":gray[How to Use]",divider='gray')
    st.markdown("""
        My platform is designed to be intuitive and easy to navigate. Users can select different months, regions, and product categories to tailor the analysis to their specific needs. Each visualization and metric is accompanied by interactive controls, allowing users to filter and drill down into the data effortlessly.
        """)
    st.markdown('<br><br>', unsafe_allow_html=True)

    st.subheader(":gray[Purpose and Goals]",divider='gray')
    st.markdown("""
        The primary goal of this project is to provide a clear and accessible way to explore and understand sales data. Whether you are a business owner, data analyst, or researcher, my platform aims to facilitate data-driven decision-making and uncover actionable insights from the 2019 sales data.
        """)

    st.markdown("""
        Thank you for visiting my Sales Data Analysis Project. I hope you find the analysis insightful and the visualizations engaging. If you have any feedback or suggestions, please feel free to reach out to me.
        """)

    #st.sidebar.markdown('<br><br>', unsafe_allow_html=True)
    #st.sidebar.markdown('<br><br>', unsafe_allow_html=True)
    st.sidebar.header('Connect with me!')

    url = 'https://www.linkedin.com/in/aditi-gupta-73363a1b2?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app'

    st.sidebar.link_button(':blue[My linkedin profile]', url=url) #':round_pushpin:',






if page == 'Analysis by city':
    with st.spinner('loading...'):
        time.sleep(5)
    page1()
elif page == 'About the project':
    page2()
elif page == 'Overall analysis':
    home_page()








