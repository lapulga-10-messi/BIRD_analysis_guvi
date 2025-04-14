# BIRD_analysis_guvi

PROJECT OBJECTIVES -- Problem Statement:
The project aims to analyze the distribution and diversity of bird species in two distinct ecosystems: forests and grasslands. By examining bird species observations across these habitats, the goal is to understand how environmental factors, such as vegetation type, climate, and terrain, influence bird populations and their behavior. The study will involve working on the provided observational data of bird species present in both ecosystems, identifying patterns of habitat preference, and assessing the impact of these habitats on bird diversity. The findings can provide valuable insights into habitat conservation, biodiversity management, and the effects of environmental changes on avian communities.

Setup instructions--

Bird_Monitoring_Data_FOREST.XLSX and Bird_Monitoring_Data_GRASSLAND.XLSX are datsets for this project .

In the files bird_data_determing_which_column_to_drop_forest.ipynb and bird_data_determing_which_column_to_drop_grassland.ipynb I must analyzed which columns to drop to get a rough idea to start as it is a big dataset .

Bird_data_analysis_forest_DT.ipynb and Bird_data_analysis_grasslands_DT.ipynb deal with data cleaning and filling missing values after studing the data.

_Cleaned_Forest_df_.csv and _Cleaned_GRASSLAND_df_.csv  are cleaned files 

Next run SQL_CONNECTION.ipynb , Once executed, this will create a connection to database on a online cloud mysql database server hosted by aiven.io Details of the server are here as follows

Host mysql-3cfdc572-avamsi2k11-4e7b.h.aivencloud.com

Port 22799

User avnadmin

Password AVNS_ozTCcwHYoNvj53twyRY

Once the connection is established  attach these files in github along with streamlit_bird_analysis.py and Requirements.txt, which are used to deploy on streamlit page as it allows to create a app from github repository 

As I have already deployed this app you can access this using the url in the url.txt
