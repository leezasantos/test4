#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:27:09 2020

@author: leeza
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

#----------Loading Dataset----------  
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()
hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']

#----------Header----------  

st.title('Analysis of New York Inpatient and Outpatient Facilities 2015 Patient Data')

st.subheader('By: Leeza A. Santos')

st.subheader('Last Updated: 12/20/2020')
 
st.header('This dashboard displays reported patient discharges, patient experience, and payment data of New York inpatient and outpatient hospital facilities utilizing Python programming language and deployed by Streamlit.')


st.subheader("Dataset Directory")
st.markdown("""
            This dashboard utilzes three types of datasets. The first dataset is NY Hospital Experience. 
            This dataset is derived from a nationwide dataset assessing emergency services, meaningful use of electronic 
            health records,hospital overall rating, safety of care, readmission rates, patient experience, and timeliness of care of
            hospital facilitis across the United States. This dataset compares NY hospital facility scores against nationwide scores.  
             
            The second dataset is a list of inpatient facilities in NY. This dataset includes the diagnosis-related group
            and payments among NY inpatient facilities.
             
             Lastly, the third dataset is a list of outpatient facilities in NY, their services, and payments. 
             """)


selectbar = st.selectbox('Select Dataset', ("Hospital Experience", "Inpatient", "Outpatient"))

def get_dataset(selectbar):
    if selectbar == 'Hospital Experience':
        st.write(hospitals_ny)
    if selectbar == 'Inpatient':
        st.write(inpatient_ny)
    if selectbar == 'Outpatient':
        st.write(outpatient_ny)
        
st.write(get_dataset(selectbar))

## selectbar https://youtu.be/Klqn--Mu2pE
    
#----------Overview of NY Hospitals----------        

st.header('Overview')

 
st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


# Create a list of possible values and multiselect menu with them in it.
county = hospitals_ny['country_name'].unique()
county_selected = st.multiselect('Select County', county)

# Mask to filter dataframe
mask_county = hospitals_ny['county_name'].isin(county_selected)

county_selbar = hospitals_ny[mask_county]



#----------Pie Chart----------  
bar4 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.subheader('Pie Chart of NY Hospital Type')
fig = px.pie(bar4, values='hospital_type', names='index')
st.plotly_chart(fig)


#Timeliness of Care
st.subheader('NY Hospitals: Timelieness of Care')
bar5 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar5, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on the chart above, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')


#----------Hospital Performance---------- 


## finding their row #: df_hospital_2[df_hospital_2['hospital_name'].str.contains('NORTHWELL')]

st.header('Hospital Performance New York, Nassau, Suffolk')
st.markdown("""
            We will be examining the hospital performance of three NY counties: New York - Manhattan, Nassau, and Suffolk County.
            For each county, we will be looking at mortality rate, safety of care, and patient experience compared to nationwide data.
            Furthermore, we will examine and compare three hospitals, one from each county, NYU Langone located in Manhattan,
            Northwell Hospital located in Nassau County, and Stony Brook University hospital located in Suffolk County.
             """)

st.markdown("""
            We will be examining the hospital performance of three NY counties: New York - Manhattan, Nassau, and Suffolk County.
            For each county, we will be looking at mortality rate, safety of care, and patient experience compared to nationwide data.
            Furthermore, we will examine and compare three hospitals, one from each county, NYU Langone located in Manhattan,
            Northwell Hospital located in Nassau County, and Stony Brook University hospital located in Suffolk County.
             """)
 
    
 
#-------Performance by County-------

st.header('Hospital Performance by County')

## Prepare data, we will extract data by COUNTY_NAME fron hospitals_ny dataset
ny = hospitals_ny[hospitals_ny['county_name']=='NEW YORK']
nassau = hospitals_ny[hospitals_ny['county_name']=='NASSAU']
suffolk = hospitals_ny[hospitals_ny['county_name']=='SUFFOLK']

#---------Manhattan--------

st.subheader('New York - Manhattan')

st.markdown('<font color=‘black’>NEW YORK COUNTY MORTALITY</font>', unsafe_allow_html=True)
ny_mortality = ny['mortality_national_comparison'].value_counts().reset_index()
ny_mor_pie = px.pie(ny_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(ny_mor_pie)

st.markdown("""
            We cannot conclude accurate assumptions based on this chart because mortality averages are not 
           available for 50% of our sample. However, based on the 50% that we do have available, we can conclude over 1/3rd or 
           37.5% of New York county hospitals have higher mortality rates than average. 
            """)


st.markdown('<font color=‘black’>NEW YORK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
ny_safety = ny['safety_of_care_national_comparison'].value_counts().reset_index()
ny_safety_pie = px.pie(ny_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(ny_safety_pie)

st.markdown("""
            This chart suggests that 31.3% of New York county hospitals have lower safety of care than 
            the national average while 18.8% of New York county hospitals performs above national average
            in safety of care. 
            """)

st.markdown('<font color=‘black’>NEW YORK PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
ny_patient = ny['patient_experience_national_comparison'].value_counts().reset_index()
ny_patient_exp = px.pie(ny_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(ny_patient_exp)

st.markdown("""
            This chart suggests that nearly half of New York county hospitals perform below national average on 
            patient experience while only 12.5% performs same as average, and 6.25% performs above national average.
            """)
            
st.markdown("""
            The charts above suggests that New York county hospitals perform poorly on safety of care and patient experience.
            """)

#---------Nassau--------

st.subheader('Nassau')

st.markdown('<font color=‘black’>NASSAU COUNTY MORTALITY</font>', unsafe_allow_html=True)
nassau_mortality = nassau['mortality_national_comparison'].value_counts().reset_index()
nassau_mor_pie = px.pie(nassau_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(ny_mor_pie)

st.markdown("""
           We cannot conclude accurate assumptions based on this chart because mortality averages are not 
           available for 50% of our sample. However, based on the 50% that we do have available, we can conclude over 1/3rd or 
           37.5% of Nassau county hospitals have higher mortality rates than average. 
            """)

st.markdown('<font color=‘black’>NASSAU COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
nassau_safety = nassau['safety_of_care_national_comparison'].value_counts().reset_index()
nassau_safety_pie = px.pie(nassau_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(nassau_safety_pie)

st.markdown("""
            This chart suggests that Nassau county hospitals perform below national average in safety of care,
            with more than 2/3rds or 77.8% of their hospitals scoring below average on safety of care.
            """)

st.markdown('<font color=‘black’>NASSAU PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
nassau_patient = nassau['patient_experience_national_comparison'].value_counts().reset_index()
nassau_patient_exp = px.pie(nassau_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(nassau_patient_exp)

st.markdown("""
            From this chart, we can conclude that Nassau county hospitals performs poorly on patient experience, 
            with roughly 66.7% of Nassau county falling below national average. 
            """)
            
            
st.markdown("""
           Based on our charts, we can assume that Nassau county hospitals measures lower in safety or care and
           patient experience than national average.
            """)            

#---------Suffolk--------

st.subheader('Suffolk')

st.markdown('<font color=‘black’>SUFFOLK COUNTY MORTALITY</font>', unsafe_allow_html=True)
suffolk_mortality = suffolk['mortality_national_comparison'].value_counts().reset_index()
suffolk_mor_pie = px.pie(suffolk_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(suffolk_mor_pie)

st.markdown("""
            From this chart, we can assume that roughly 35.7% of Suffolk county hospitals
            have higher mortality rates when compared nationwide. However, this data cannot be considered reliable as
            we do not have available data for nearly one third of our sample. 
             """)
 

st.markdown('<font color=‘black’>SUFFOLK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
suffolk_safety = suffolk['safety_of_care_national_comparison'].value_counts().reset_index()
suffolk_safety_pie = px.pie(suffolk_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(suffolk_safety_pie)

st.markdown("""
            From this chart, 28.6% of Suffolk county hospitals perform above national safety of care average
            while 28.6% performs below average. This chart cannot conclude accurate safety of care opinion on
            Suffolk county hospitals as we do not have data for 35.7% of Suffolk county hospitals.
            """)


st.markdown('<font color=‘black’>SUFFOLK COUNTY PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
suffolk_patient_exp = suffolk['patient_experience_national_comparison'].value_counts().reset_index()
suffolk_pt_pie = px.pie(suffolk_patient_exp, values='patient_experience_national_comparison', names='index')
st.plotly_chart(suffolk_pt_pie)

st.markdown("""
            From this chart, roughly 42.9% of Suffolk county hospitals perform below national average on patient experience
            while the remaining 21.4% only performs the same as national average.
            """)


st.markdown("""
            From the charts above, we can assume that Suffolk county hospitals perform poorly compared to national averages.
            """)


#----------Comparison---------- 

st.subheader('Comparison of Hospitals by County')

st.markdown('Lets extract one random hospital from each country. In this case, we selected NYU Langone, Northwell Health, and Stony Brook University Hospital.')
 

performance = df_hospital_2.iloc[[3230, 2487, 2139],:]
performance = performance[['hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(performance)

st.markdown("""
            Based on the table above, we can conclude that all three hospitals are acute care hospitals.
            However, they begin to differ by quality.
            
            Lets first compare mortality rates. From this table, we see that NYU Langone and Stony Brook
            University hospital both have higher mortality rates than national average while Northwell
            rates about the same as national average. 
            
            Next, lets compare safety of care. Both Northwell and Stony Brook University Hospital
            performs above the national average while NYU Langone performs below national average.
            
            Lastly, we have patient experience. Both NYU Langone and Northwell positive patient experience
            are the same as national average while Stony Brook performs below average.
            """)


#----------Inpatient---------- 
st.header('Inpatient')



inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.subheader('Total Count of Discharges from Inpatient Captured: ' )
st.subheader( str(total_inpatient_count) )

st.subheader('Top 10 Highest Discharge Rates and Outpatient Services')
st.markdown('The bar charts below displays inpatient hospitals with the highest discharge rates and outpatient facilities with the highest services in NY.')

df_bar1 = inpatient_ny[['provider_name','total_discharges']]
sorted = df_bar1.sort_values('total_discharges')  ##sort
source1 = sorted[11247:11257]
 
bar1 = alt.Chart(source1).mark_bar().encode(
    x='provider_name',
    y='total_discharges'
    )
st.altair_chart(bar1, use_container_width=True)



#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')

st.subheader('Inpatient: Medicare Payments')

costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']

#-----Medicare------

bar6 = px.bar(costs_sum, x='provider_name', y='average_medicare_payments')
st.plotly_chart(bar6)
st.subheader("Average Medicare Payments")
st.dataframe(costs_sum)

#-----Total------

st.subheader('Inpatient: Average Total Payments')

bar6 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar6)
st.subheader("Average Total Payments")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.subheader("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)


st.markdown("""
           The top 5 inpatient facilities with the highest average total payments were
           New-York Presbyterian, Westchester Medical Center, Mount Sinai Hospital, Montefiore Medical Center, and Strong
            """) 





#----------Outpatient---------- 

st.header('Outpatient')


st.subheader('Top 10 Outpatient Services')
df_bar2 = outpatient_ny[['provider_name','outpatient_services']]
sorted2 = df_bar2.sort_values('outpatient_services')  ##sort
source2 = sorted2[1624:1632]

bar2 = alt.Chart(source2).mark_bar().encode(
    x='provider_name',
    y='outpatient_services'
    )
st.altair_chart(bar2, use_container_width=True)



common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.subheader('DRGs')
st.dataframe(common_discharges)

st.markdown("""
           From the table above, we can conclude that most discharges in our sample 
           are due to septicemia/severe sepsis, major joint replacement/reattachment of extremity,
           heart failure, and digestive disorders.
            """) 

col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)






# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered)