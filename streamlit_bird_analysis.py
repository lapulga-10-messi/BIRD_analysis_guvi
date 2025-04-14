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
        forest_query = """SELECT * FROM forest_data LIMIT 8546"""
        grassland_query = """SELECT * FROM grassland_data LIMIT 6826"""
        
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
TEXT_COLOR = '#2C1D4C'  
BACKGROUND_COLOR = '#F0F2F6'
WHITE = '#FFFFFF'

# Set matplotlib style
plt.style.use('ggplot')

forest = forest_data_df
grassland = grassland_data_df

# Main title 
st.title(":blue[Bird Species Analysis]")

# Sidebar options
selectors = st.sidebar.radio('Analaysis Type:', [':blue[Temporal Analysis]',':blue[Species Analysis]',':blue[Environmental Conditions]',':blue[Distance & Behavior]',':blue[Observer Trends]', ':blue[Conservation Insights]'])

# # Sidebar Filters
# st.sidebar.header("Filters")
# selected_monthf = st.sidebar.multiselect("Select Months for Forest", forest["Month"].unique(), default=forest["Month"].unique())
# selected_monthg = st.sidebar.multiselect("Select Months for Grassland", grassland["Month"].unique(), default=grassland["Month"].unique())
# selected_skyf= st.sidebar.multiselect("Select the sky conditions for forest ", forest["Sky"].unique(), default=forest["Sky"].unique())
# selected_skyg= st.sidebar.multiselect("Select the sky conditions for grassland", grassland["Sky"].unique(), default=grassland["Sky"].unique())
# selected_windf = st.sidebar.multiselect("Select the wind conditions for forest", forest["Wind"].unique(), default=forest["Wind"].unique())
# selected_windg = st.sidebar.multiselect("Select the wind conditions for grassland", grassland["Wind"].unique(), default=grassland["Wind"].unique())
# selected_sexf = st.sidebar.multiselect("Select sex of observed bird for forest", forest["Sex"].unique(), default=forest["Sex"].unique())
# selected_sexg = st.sidebar.multiselect("Select sex of observed bird for grassland", grassland["Sex"].unique(), default=grassland["Sex"].unique())
# selected_intervalf = st.sidebar.multiselect("Select the Observation Time Interval for forest ", forest["Interval_Length"].unique(), default=forest["Interval_Length"].unique())
# selected_intervalg = st.sidebar.multiselect("Select the Observation Time Interval for grassland ", grassland["Interval_Length"].unique(), default=grassland["Interval_Length"].unique())

# # Handle empty filters
# selected_intervalf = selected_intervalf or forest["Interval_Length"].unique()
# selected_intervalg = selected_intervalg or grassland["Interval_Length"].unique()
# selected_monthf = selected_monthf or forest["Month"].unique()
# selected_monthg = selected_monthg or grassland["Month"].unique()
# selected_skyf = selected_skyf or forest["Sky"].unique()
# selected_skyg = selected_skyg or grassland["Sky"].unique()
# selected_windf = selected_windf or forest["Wind"].unique()
# selected_windg = selected_windg or grassland["Wind"].unique()
# selected_sexf = selected_sexf or forest["Sex"].unique()
# selected_sexg = selected_sexg or grassland["Sex"].unique()

# forest_df = forest[(forest["Month"].isin(selected_monthf)) & (forest["Interval_Length"].isin(selected_intervalf)) & (forest["Sky"].isin(selected_skyf)) & (forest["Wind"].isin(selected_windf)) & (forest["Sex"].isin(selected_sexf))]
# grassland_df = grassland[(grassland["Month"].isin(selected_monthg)) & (grassland["Interval_Length"].isin(selected_intervalg)) & (grassland["Sky"].isin(selected_skyg)) & (grassland["Wind"].isin(selected_windg)) & (grassland["Sex"].isin(selected_sexg))]

# Sidebar Filters #
st.sidebar.header("Filters")

# Checkbox for month Filter Selection and month filter for forest
apply_month_filterf = st.sidebar.checkbox("Apply Month Filter for forest", value=True)
selected_monthf = st.sidebar.multiselect("Select Months for Forest", forest["Month"].unique(), default=forest["Month"].unique())

# Checkbox for month Filter Selection and month filter for grassland
apply_month_filterg = st.sidebar.checkbox("Apply Month Filter for grassland", value=True)
selected_monthg = st.sidebar.multiselect("Select Months for Grassland", grassland["Month"].unique(), default=grassland["Month"].unique())

# Checkbox for interval Filter Selection and interval filter for forest
apply_interval_filterf = st.sidebar.checkbox("Apply Interval Filter for forest", value=False)
selected_intervalf = st.sidebar.multiselect("Select the Observation Time Interval for forest ", forest["Interval_Length"].unique(), default=forest["Interval_Length"].unique())

# Checkbox for interval Filter Selection and interval filter for grassland
apply_interval_filterg = st.sidebar.checkbox("Apply Interval Filter for grassland", value=False)
selected_intervalg = st.sidebar.multiselect("Select the Observation Time Interval for grassland ", grassland["Interval_Length"].unique(), default=grassland["Interval_Length"].unique())

# Checkbox for sky Filter Selection and sky filter for forest
apply_sky_filterf = st.sidebar.checkbox("Apply Sky Filter for forest", value=False)
selected_skyf = st.sidebar.multiselect("Select the sky conditions for forest ", forest["Sky"].unique(), default=forest["Sky"].unique())

# Checkbox for sky Filter Selection and sky filter for grassland
apply_sky_filterg = st.sidebar.checkbox("Apply Sky Filter for grassland", value=False)
selected_skyg = st.sidebar.multiselect("Select the sky conditions for grassland", grassland["Sky"].unique(), default=grassland["Sky"].unique())

# Checkbox for wind Filter Selection and wind filter for forest
apply_wind_filterf = st.sidebar.checkbox("Apply Wind Filter for forest", value=False)
selected_windf = st.sidebar.multiselect("Select the wind conditions for forest", forest["Wind"].unique(), default=forest["Wind"].unique())

# Checkbox for wind Filter Selection and wind filter for grassland
apply_wind_filterg = st.sidebar.checkbox("Apply Wind Filter for grassland", value=False)
selected_windg = st.sidebar.multiselect("Select the wind conditions for grassland", grassland["Wind"].unique(), default=grassland["Wind"].unique())

# Checkbox for sex Filter Selection and sex filter for forest
apply_sex_filterf = st.sidebar.checkbox("Apply Sex Filter for forest", value=False)
selected_sexf = st.sidebar.multiselect("Select sex of observed bird for forest", forest["Sex"].unique(), default=forest["Sex"].unique())

# Checkbox for sex Filter Selection and sex filter for grassland
apply_sex_filterg = st.sidebar.checkbox("Apply Sex Filter for grassland", value=False)
selected_sexg = st.sidebar.multiselect("Select sex of observed bird for grassland", grassland["Sex"].unique(), default=grassland["Sex"].unique())

# Handle empty filters
selected_intervalf = selected_intervalf or None
selected_intervalg = selected_intervalg or None
selected_monthf = selected_monthf or forest["Month"].unique()
selected_monthg = selected_monthg or grassland["Month"].unique()
selected_skyf = selected_skyf or None
selected_skyg = selected_skyg or None
selected_windf = selected_windf or None
selected_windg = selected_windg or None
selected_sexf = selected_sexf or None
selected_sexg = selected_sexg or None

# Define function to apply filters dynamically
def apply_filters(df, month_filter, interval_filter=None, sky_filter=None, wind_filter=None, sex_filter=None, apply_month=True, apply_interval=False, apply_sky=False, apply_wind=False, apply_sex=False):
    conditions = []
    
    if apply_month:
        conditions.append(df["Month"].isin(month_filter))
        
    if apply_interval and interval_filter:
        conditions.append(df["Interval_Length"].isin(interval_filter))
        
    if apply_sky and sky_filter:
        conditions.append(df["Sky"].isin(sky_filter))
        
    if apply_wind and wind_filter:
        conditions.append(df["Wind"].isin(wind_filter))
        
    if apply_sex and sex_filter:
        conditions.append(df["Sex"].isin(sex_filter))
        
    # Combine conditions with &
    if conditions:
        filter_condition = conditions[0]
        for condition in conditions[1:]:
            filter_condition &= condition
        return df[filter_condition]
    else:
        return df

# Apply filters dynamically based on checkboxes and selections
forest_df = apply_filters(forest, selected_monthf, selected_intervalf, selected_skyf, selected_windf, selected_sexf, apply_month = apply_month_filterf, apply_interval=apply_interval_filterf, apply_sky = apply_sky_filterf, apply_wind = apply_wind_filterf , apply_sex = apply_sex_filterf)
grassland_df = apply_filters(grassland, selected_monthg, selected_intervalg, selected_skyg, selected_windg, selected_sexg, apply_month = apply_month_filterg, apply_interval = apply_interval_filterg, apply_sky = apply_sky_filterg , apply_wind=apply_wind_filterg , apply_sex = apply_sex_filterg)


def Temporal_Analysis():
    ## For Forest ##
    st.write('<span style="font-size:35px; font-weight:bold; color:#C8920B;">\u2022 Seasonal Trends in Forests</span>', unsafe_allow_html=True)
    
    forest_count = forest_df.groupby("Date")["Common_Name"].count().reset_index()
    forest_count.columns = ["Date", "Observation Count"]
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forest_count["Date"], forest_count["Observation Count"], marker='o', color='#C8920B', linewidth=2.5, markersize=8,markerfacecolor='white', markeredgewidth=1.5)
    
    # Formatting
    ax.set_title("Monthly Bird Sightings in Forest", fontsize=16, pad=20, weight='bold')
    ax.set_xlabel("Date", fontsize=12, weight='bold')
    ax.set_ylabel("Observation Count", fontsize=12, weight='bold')
    ax.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    max_monthf = forest_count.loc[forest_count["Observation Count"].idxmax()]
    min_monthf = forest_count.loc[forest_count["Observation Count"].idxmin()]
    
    st.write(f'<span style="font-size:15px; font-weight:bold; color:#FFFFFF;">The month with the highest bird observations in forests is {max_monthf["Date"].strftime("%B %Y")} with {max_monthf["Observation Count"]} sightings.</span>', unsafe_allow_html=True)
    st.write(f'<span style="font-size:15px; font-weight:bold; color:#FFFFFF;">The month with the lowest bird observations in forests is {min_monthf["Date"].strftime("%B %Y")} with {min_monthf["Observation Count"]} sightings.</span>', unsafe_allow_html=True)
    #########################################################################################################
    
    ## For Grassland##
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write('<span style="font-size:35px; font-weight:bold; color:#FFB233;">\u2022 Seasonal Trends in Grasslands</span>', unsafe_allow_html=True)
    
    grassland_count = grassland_df.groupby("Date")["Common_Name"].count().reset_index()
    grassland_count.columns = ["Date", "Observation Count"]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(grassland_count["Date"], grassland_count["Observation Count"], marker='o', color='#FFB233', linewidth=2, markersize=8)
    ax.set_title("Bird Sightings by Month in Grassland", fontsize=16, pad=20)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    max_monthg = grassland_count.loc[grassland_count["Observation Count"].idxmax()]
    min_monthg = grassland_count.loc[grassland_count["Observation Count"].idxmin()]
    
    st.write(f'<span style="font-size:15px; font-weight:bold; color:#FFFFFF;">The month with the highest bird observations in grasslands is {max_monthg["Date"].strftime("%B %Y")} with {max_monthg["Observation Count"]} sightings.</span>', unsafe_allow_html=True)
    st.write(f'<span style="font-size:15px; font-weight:bold; color:#FFFFFF;">The month with the lowest bird observations in grasslands is {min_monthg["Date"].strftime("%B %Y")} with {min_monthg["Observation Count"]} sightings.</span>', unsafe_allow_html=True)

def species_analysis():
    # Forest species
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Species Distribution in Forests</span>', unsafe_allow_html=True)
    
    forest_species = forest_df["Common_Name"].value_counts().reset_index()
    forest_species.columns = ["Species", "Count"]
    
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.bar(forest_species["Species"], forest_species["Count"], color=FOREST_COLOR)
    ax.set_title("Top Observed Bird Species in Forest", fontsize=14, pad=20)
    ax.set_xlabel("Species", fontsize=10)
    ax.set_ylabel("Count", fontsize=12)
    plt.xticks(rotation=90, ha='left')
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    max_species_forest = forest_species.iloc[0]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:{WHITE};"> The most observed bird species in forests is {max_species_forest['Species']} with {max_species_forest['Count']} sightings.</span>', unsafe_allow_html=True)

    # Grassland species
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Species Distribution in Grasslands</span>', unsafe_allow_html=True)
    
    grassland_species = grassland_df["Common_Name"].value_counts().reset_index()
    grassland_species.columns = ["Species", "Count"]  
    
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.bar(grassland_species["Species"], grassland_species["Count"], color=GRASSLAND_COLOR)
    ax.set_title("Top Observed Bird Species in Grassland", fontsize=14, pad=20)
    ax.set_xlabel("Species", fontsize=10)
    ax.set_ylabel("Count", fontsize=12)
    plt.xticks(rotation=90, ha='left')
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    max_species_grassland = grassland_species.iloc[0]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:{WHITE};"> The most observed bird species in grasslands is {max_species_grassland['Species']} with {max_species_grassland['Count']} sightings.</span>', unsafe_allow_html=True)

def environmental_conditions():
    # Forest environmental factors
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Environmental Impact in Forests</span>', unsafe_allow_html=True)
    
    # temperature in forests
    st.markdown(f'<span style="font-size:25px; font-weight:bold; color:{FOREST_COLOR};">Temperature Impact in Forests</span>', unsafe_allow_html=True)
    
    fig, (ax1) = plt.subplots(1, figsize=(15, 15))
    ax1.scatter(forest_df["Temperature"], forest_df["Common_Name"], color=FOREST_COLOR, alpha=0.7)
    ax1.set_title("Temperature Impact (Forest)", fontsize=14)
    ax1.set_xlabel("Temperature")
    ax1.set_ylabel("Species",fontsize=10)
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE};"> Best Temperature for bird sightings in forests is between 15°C and 30 °C  </span>', unsafe_allow_html=True)
    
    # humidity in forests 
    st.markdown(f'<span style="font-size:25px; font-weight:bold; color:{FOREST_COLOR};">Humidity Impact in Forests</span>', unsafe_allow_html=True)
    
    fig, (ax2) = plt.subplots( figsize=(15, 15))
    ax2.scatter(forest_df["Humidity"], forest_df["Common_Name"], color=FOREST_COLOR, alpha=0.7)
    ax2.set_title("Humidity Impact (Forest)", fontsize=14)
    ax2.set_xlabel("Humidity")
    ax2.set_ylabel("Species")
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE};"> Best humidity for bird sightings in forests is between 60 and 90  </span>', unsafe_allow_html=True)

    # Grassland environmental factors
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Environmental Impact in Grasslands</span>', unsafe_allow_html=True)

    # temperature in grasslands
    st.markdown(f'<span style="font-size:25px; font-weight:bold; color:{GRASSLAND_COLOR};"> Temperature Impact in Grasslands</span>', unsafe_allow_html=True)

    fig, (ax1) = plt.subplots(1, figsize=(15, 15))
    ax1.scatter(grassland_df["Temperature"], grassland_df["Common_Name"], color=GRASSLAND_COLOR, alpha=0.7)
    ax1.set_title("Temperature Impact (Grassland)", fontsize=14)
    ax1.set_xlabel("Temperature")
    ax1.set_ylabel("Species",fontsize=10)
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE} ;"> Best Temperature for bird sightings in forests is between 15°C and 30 °C  </span>', unsafe_allow_html=True)

    # humidity in grasslands
    st.markdown(f'<span style="font-size:25px; font-weight:bold; color:{GRASSLAND_COLOR};"> Humidity Impact in Grasslands</span>', unsafe_allow_html=True)

    fig, (ax2) = plt.subplots( figsize=(15, 15))
    ax2.scatter(grassland_df["Humidity"], grassland_df["Common_Name"], color=GRASSLAND_COLOR, alpha=0.7)
    ax2.set_title("Humidity Impact (Grassland)", fontsize=14)
    ax2.set_xlabel("Humidity")
    ax2.set_ylabel("Species")
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE};">Best humidity for bird sightings in forests is between 60 and 90  </span>', unsafe_allow_html=True)

def distance_behavior():
    # Forest distance and behavior
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Distance and Behavior in Forests</span>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    distance_count_f = forest_df["Distance"].value_counts().reset_index()
    distance_count_f.columns = ["Distance", "Count"]  # Corrected column names
    ax1.bar(distance_count_f["Distance"], distance_count_f["Count"], color=FOREST_COLOR)
    ax1.set_title("Sightings by Distance (Forest)", fontsize=14)
    ax1.set_xlabel("Distance")
    ax1.set_ylabel("Count")
    
    flyover_f = forest_df["Flyover_Observed"].value_counts()
    ax2.pie(flyover_f, labels=flyover_f.index, autopct='%1.1f%%', colors=[FOREST_COLOR, GRASSLAND_COLOR], startangle=90)
    ax2.set_title("Flyover Observations (Forest)", fontsize=14)
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE};"> When the distance is less than 50 meters more birds are frequently recorded. Flyover observations are very low.</span>', unsafe_allow_html=True)

    # Grassland distance and behavior
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Distance and Behavior in Grasslands</span>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    distance_count_g = grassland_df["Distance"].value_counts().reset_index()
    distance_count_g.columns = ["Distance", "Count"] 
    ax1.bar(distance_count_g["Distance"], distance_count_g["Count"], color=GRASSLAND_COLOR)
    ax1.set_title("Sightings by Distance (Grassland)", fontsize=14)
    ax1.set_xlabel("Distance")
    ax1.set_ylabel("Count")
    
    flyover_g = grassland_df["Flyover_Observed"].value_counts()
    ax2.pie(flyover_g, labels=flyover_g.index, autopct='%1.1f%%',colors=[GRASSLAND_COLOR, FOREST_COLOR], startangle=90)
    ax2.set_title("Flyover Observations (Grassland)", fontsize=14)
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE};"> When the distance is between 50-100 meters more birds are frequently recorded. Flyover observations are low.</span>', unsafe_allow_html=True)

def observer_trends():
    # Forest observers
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">\u2022 Observer Trends in Forests</span>', unsafe_allow_html=True)
    
    observer_count_forest = forest_df["Observer"].value_counts().reset_index()
    observer_count_forest.columns = ["Observer", "Count"] 
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(observer_count_forest["Observer"], observer_count_forest["Count"], color=FOREST_COLOR)
    ax.set_title("Observer Contributions in Forest", fontsize=14, pad=20)
    ax.set_xlabel("Observer", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    max_observer_forest = observer_count_forest.iloc[0]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:{WHITE};"> The most active observer in forests is {max_observer_forest['Observer']} with {max_observer_forest['Count']} observations.</span>', unsafe_allow_html=True)

    # Grassland observers
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{GRASSLAND_COLOR};">\u2022 Observer Trends in Grasslands</span>', unsafe_allow_html=True)
    
    observer_count_grassland = grassland_df["Observer"].value_counts().reset_index()
    observer_count_grassland.columns = ["Observer", "Count"]  
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(observer_count_grassland["Observer"], observer_count_grassland["Count"], color=GRASSLAND_COLOR)
    ax.set_title("Observer Contributions in Grassland", fontsize=14, pad=20)
    ax.set_xlabel("Observer", fontsize=12)
    ax.set_ylabel("Observation Count", fontsize=12)
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close()

    max_observer_grassland = observer_count_grassland.iloc[0]
    st.write(f'<span style="font-size:18px; font-weight:bold; color:color:{WHITE};"> The most active observer in grasslands is {max_observer_grassland['Observer']} with {max_observer_grassland['Count']} observations.</span>', unsafe_allow_html=True)

def Conservation_Insights():
    
    st.markdown(f'<span style="font-size:30px; font-weight:bold; color:{FOREST_COLOR};">Conservation Status</span>', unsafe_allow_html=True)
    
    st.write(f'<span style="font-size:25px; font-weight:bold;color:{FOREST_COLOR};"> Forests status </span>', unsafe_allow_html=True)

    #each species has only one unique status combination
    species_statusf = forest_df.groupby("Common_Name")[["PIF_Watchlist_Status", "Regional_Stewardship_Status"]].first().reset_index()

    # mapping tuples to groups
    group_map = {(True, True): "A",(True, False): "B",(False, True): "C",(False, False): "D"}

    species_statusf["Group"] = species_statusf.apply(lambda x: group_map[(x["PIF_Watchlist_Status"], x["Regional_Stewardship_Status"])],
    axis=1)

    # Counting species in each group
    group_countsf = species_statusf["Group"].value_counts().reset_index()
    group_countsf.columns = ["Group", "Species_Count"]

    #plotiing pie chart

    mycolors = ["pink", "cyan", "yellow", "orange"]
    myexplode = [0.2, 0.2, 0.2, 0.2]

    fig, ax = plt.subplots(figsize=(10, 10))
    # Ensure the data and labels are aligned
    ax.pie(group_countsf["Species_Count"],labels=None,colors=mycolors,explode=myexplode,autopct='%1.1f%%',shadow=True)
    ax.legend(title='Conservation Status',labels=['Lower conservation priority.','Regionally important but not globally at-risk',
            'Globally and regionally critical','Globally at-risk but not a regional priority'],loc='upper right')
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold;color:{WHITE};">Blue-winged Warbler ,Cerulean Warbler ,Red-headed Woodpecker are the most endangered species in forests </span>', unsafe_allow_html=True)

    ########### grassland conservation status##########

    st.write(f'<span style="font-size:25px; font-weight:bold; color:{GRASSLAND_COLOR};"> Grassland Status </span>', unsafe_allow_html=True)

    #each species has only one unique status combination
    species_statusg = grassland_df.groupby("Common_Name")[["PIF_Watchlist_Status", "Regional_Stewardship_Status"]].first().reset_index()

    species_statusg["Group"] = species_statusg.apply(lambda x: group_map[(x["PIF_Watchlist_Status"], x["Regional_Stewardship_Status"])],axis=1)

    # Counting species in each group
    group_countsg = species_statusg["Group"].value_counts().reset_index()
    group_countsg.columns = ["Group", "Species_Count"]

    #Plotiing pie chart

    mycolors = ["pink", "cyan", "yellow", "orange"]
    myexplode = [0.2, 0.2, 0.2, 0.2]

    fig, ax = plt.subplots(figsize=(10, 10))
    # Ensure the data and labels are aligned
    ax.pie(group_countsg["Species_Count"],labels=None,colors=mycolors,explode=myexplode,autopct='%1.1f%%',shadow=True)
    ax.legend(title='Conservation Status',labels=['Lower conservation priority.','Regionally important but not globally at-risk','Globally and regionally critical','Globally at-risk but not a regional priority'],loc='upper right')
    st.pyplot(fig)
    plt.close()

    st.write(f'<span style="font-size:18px; font-weight:bold; color:{WHITE};">Willow Flycatcher is the most endangered specie in grasslands </span>', unsafe_allow_html=True)
    
# Routing 
if selectors == ':blue[Temporal Analysis]':
    Temporal_Analysis()
elif selectors == ':blue[Species Analysis]':
    species_analysis()
elif selectors == ':blue[Environmental Conditions]':
    environmental_conditions()
elif selectors == ':blue[Distance & Behavior]':
    distance_behavior()
elif selectors == ':blue[Observer Trends]':
    observer_trends()
elif selectors == ':blue[Conservation Insights]':
    Conservation_Insights()
