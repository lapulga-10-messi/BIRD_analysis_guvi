import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np

# Database configuration
config = {
    'host': 'mysql-3cfdc572-avamsi2k11-4e7b.h.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_ozTCcwHYoNvj53twyRY',
    'port': 22799
}

# Global variables
forest_data_df = None
grassland_data_df = None

def fetch_data(conn, sql_query):
    """Fetch data from MySQL using a given connection"""
    try:
        cursor = conn.cursor()
        cursor.execute("USE project_guvi_bird_analysis")
        cursor.execute(sql_query)
        
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        
        cursor.close()
        
        df = pd.DataFrame(rows, columns=columns)
        return df
    
    except Error as e:
        print(f"Error fetching data: {e}")
        return None

def create_connection():
    """Create a database connection"""
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize():
    global forest_data_df, grassland_data_df  # Declare as global
    
    # Create connection
    conn = create_connection()
    if conn is None:
        return
    
    try:
        # Queries
        forest_query = """SELECT * FROM forest_data"""
        grassland_query = """SELECT * FROM grassland_data"""
        
        forest_data_df = fetch_data(conn, forest_query)
        grassland_data_df = fetch_data(conn, grassland_query)
    
    finally:
        if conn.is_connected():
            conn.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    initialize()




import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set color scheme
FOREST_COLOR = '#C8920B'
GRASSLAND_COLOR = '#FFB233'
TEXT_COLOR = '#2C1D4C'  # Corrected color code
BACKGROUND_COLOR = '#F0F2F6'

# Set matplotlib style
plt.style.use('ggplot')

forest = forest_data_df
grassland = grassland_data_df

# Main title 
st.title(":blue[Bird Species Analysis]")

# Sidebar options
selectors = st.sidebar.radio('Choose an Data:', [':blue[Seasonal Trends]',':blue[Species Distribution]',':blue[Observer Trends]',':blue[Environmental Impact]',':blue[Distance & Behavior]'])

# Sidebar Filters
st.sidebar.header("Filters")
selected_monthf = st.sidebar.multiselect("Select Months for Forest", forest["Month"].unique(), default=forest["Month"].unique())
selected_monthg = st.sidebar.multiselect("Select Months for Grassland", grassland["Month"].unique(), default=grassland["Month"].unique())
selected_interval = st.sidebar.multiselect("Select the Time Interval", forest["Interval_Length"].unique(), default=forest["Interval_Length"].unique())

# Handle empty filters
selected_interval = selected_interval or forest["Interval_Length"].unique()
selected_monthf = selected_monthf or forest["Month"].unique()
selected_monthg = selected_monthg or grassland["Month"].unique()

forest_df = forest[(forest["Month"].isin(selected_monthf)) & (forest["Interval_Length"].isin(selected_interval))]
grassland_df = grassland[(grassland["Month"].isin(selected_monthg)) & (grassland["Interval_Length"].isin(selected_interval))]

# Create date columns from individual components
def create_date(df):
    try:
        # Convert month names to numbers if needed
        month_map = {month: idx+1 for idx, month in enumerate(['January', 'February', 'March', 'April', 'May', 'June',
                                                              'July', 'August', 'September', 'October', 'November', 'December'])}
        df['Month_Num'] = df['Month'].map(month_map)
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + pd.to_timedelta(df['Month_Num'] - 1, unit='M'))
        df['Date'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    except:
        # Fallback if months are already numeric
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    return df

forest_df = create_date(forest_df)
grassland_df = create_date(grassland_df)

def seasonal_trends():
    # Forest trends
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Seasonal Trends in Forest</span>', unsafe_allow_html=True)
    
    forest_monthly = forest_df.groupby(pd.Grouper(key='Date', freq='M'))['Common_Name'].count().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(forest_monthly["Date"], forest_monthly["Observation Count"], marker='o', color=FOREST_COLOR, linewidth=2)
    ax.set_title("Monthly Bird Sightings in Forest", fontsize=14, pad=20)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45,ha='right')
    st.pyplot(fig)
    plt.close()


    # Grassland trends
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Seasonal Trends in Grassland</span>', unsafe_allow_html=True)
    
    grassland_monthly = grassland_df.groupby(pd.Grouper(key='Date',freq='M'))['Common_Name'].count().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(grassland_monthly["Date"], grassland_monthly["Observation Count"],marker='o', color=GRASSLAND_COLOR, linewidth=2)        
    ax.set_title("Monthly Bird Sightings in Grassland", fontsize=14, pad=20)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45,ha='right')
    st.pyplot(fig)
    plt.close()

def species_distribution():
    # Forest species
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Species Distribution in Forest</span>', unsafe_allow_html=True)
    
    forest_species = forest_df["Common_Name"].value_counts().reset_index()
    forest_species.columns = ["Common_Name", "Count"]  # Corrected column names
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(forest_species["Common_Name"], forest_species["Count"], color=FOREST_COLOR)
    ax.set_title("Top Observed Bird Species in Forest", fontsize=14, pad=20)
    ax.set_xlabel("Species", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close()

    # Grassland species
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Species Distribution in Grassland</span>', unsafe_allow_html=True)
    
    grassland_species = grassland_df["Common_Name"].value_counts().reset_index()
    grassland_species.columns = ["Common_Name", "Count"]  # Corrected column names
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(grassland_species["Common_Name"], grassland_species["Count"], color=GRASSLAND_COLOR)
    ax.set_title("Top Observed Bird Species in Grassland", fontsize=14, pad=20)
    ax.set_xlabel("Species", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close()

def observer_trends():
    # Forest observers
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Observer Trends in Forest</span>', unsafe_allow_html=True)
    
    observer_count_f = forest_df["Observer"].value_counts().reset_index()
    observer_count_f.columns = ["Observer", "Count"]  # Corrected column names
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(observer_count_f["Observer"], observer_count_f["Count"], color=FOREST_COLOR)
    ax.set_title("Observer Contributions in Forest", fontsize=14, pad=20)
    ax.set_xlabel("Observer", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    st.pyplot(fig)
    plt.close()

    # Grassland observers
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Observer Trends in Grassland</span>', unsafe_allow_html=True)
    
    observer_count_g = grassland_df["Observer"].value_counts().reset_index()
    observer_count_g.columns = ["Observer", "Count"]  # Corrected column names
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(observer_count_g["Observer"], observer_count_g["Count"], color=GRASSLAND_COLOR)
    ax.set_title("Observer Contributions in Grassland", fontsize=14, pad=20)
    ax.set_xlabel("Observer", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    st.pyplot(fig)
    plt.close()

def environmental_impact():
    # Forest environmental factors
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Environmental Impact in Forest</span>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    ax1.scatter(forest_df["Temperature"], forest_df["Common_Name"], color=FOREST_COLOR, alpha=0.7)
    ax1.set_title("Temperature Impact (Forest)", fontsize=14)
    ax1.set_xlabel("Temperature")
    ax1.set_ylabel("Species")
    
    ax2.scatter(forest_df["Humidity"], forest_df["Common_Name"], color=FOREST_COLOR, alpha=0.7)
    ax2.set_title("Humidity Impact (Forest)", fontsize=14)
    ax2.set_xlabel("Humidity")
    ax2.set_ylabel("Species")
    st.pyplot(fig)
    plt.close()

    # Grassland environmental factors
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Environmental Impact in Grassland</span>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    ax1.scatter(grassland_df["Temperature"], grassland_df["Common_Name"], color=GRASSLAND_COLOR, alpha=0.7)
    ax1.set_title("Temperature Impact (Grassland)", fontsize=14)
    ax1.set_xlabel("Temperature")
    ax1.set_ylabel("Species")
    
    ax2.scatter(grassland_df["Humidity"], grassland_df["Common_Name"], color=GRASSLAND_COLOR, alpha=0.7)
    ax2.set_title("Humidity Impact (Grassland)", fontsize=14)
    ax2.set_xlabel("Humidity")
    ax2.set_ylabel("Species")
    st.pyplot(fig)
    plt.close()

def distance_behavior():
    # Forest distance and behavior
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Distance and Behavior in Forest</span>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    distance_count_f = forest_df["Distance"].value_counts().reset_index()
    distance_count_f.columns = ["Distance", "Count"]  # Corrected column names
    ax1.bar(distance_count_f["Distance"], distance_count_f["Count"], color=FOREST_COLOR)
    ax1.set_title("Sightings by Distance (Forest)", fontsize=14)
    ax1.set_xlabel("Distance")
    ax1.set_ylabel("Count")
    
    flyover_f = forest_df["Flyover_Observed"].value_counts()
    ax2.pie(flyover_f, labels=flyover_f.index, autopct='%1.1f%%', 
            colors=[FOREST_COLOR, GRASSLAND_COLOR], startangle=90)
    ax2.set_title("Flyover Observations (Forest)", fontsize=14)
    st.pyplot(fig)
    plt.close()

    # Grassland distance and behavior
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Distance and Behavior in Grassland</span>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    distance_count_g = grassland_df["Distance"].value_counts().reset_index()
    distance_count_g.columns = ["Distance", "Count"]  # Corrected column names
    ax1.bar(distance_count_g["Distance"], distance_count_g["Count"], color=GRASSLAND_COLOR)
    ax1.set_title("Sightings by Distance (Grassland)", fontsize=14)
    ax1.set_xlabel("Distance")
    ax1.set_ylabel("Count")
    
    flyover_g = grassland_df["Flyover_Observed"].value_counts()
    ax2.pie(flyover_g, labels=flyover_g.index, autopct='%1.1f%%', 
            colors=[GRASSLAND_COLOR, FOREST_COLOR], startangle=90)
    ax2.set_title("Flyover Observations (Grassland)", fontsize=14)
    st.pyplot(fig)
    plt.close()

# Rest of the functions remain similar but use the new date column where needed
# ... (other functions stay the same with date column now available)

# Routing logic
if selectors == ':blue[Seasonal Trends]':
    seasonal_trends()
elif selectors == ':blue[Species Distribution]':
    species_distribution()
elif selectors == ':blue[Observer Trends]':
    observer_trends()
elif selectors == ':blue[Environmental Impact]':
    environmental_impact()
elif selectors == ':blue[Distance & Behavior]':
    distance_behavior()