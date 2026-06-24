import pandas as pd
import geopandas as gpd
import libpysal.weights as weights
from esda.moran import Moran
import matplotlib.pyplot as plt
import pysal.lib as lib
from pysal.explore import esda
import esda	
from esda.moran import Moran_Local
import libpysal

# load csv files
file1_path = '/content/year2019.csv'
file2_path = '/content/year2020.csv'
file3_path = '/content/year2021.csv'

# Read the CSV files into DataFrames
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
df3 = pd.read_csv(file3_path)

# Merge the DataFrames using the common key (assuming 'common_key' is the column name)
# You can use pd.merge or pd.concat based on your specific merging requirements.
# Example using pd.merge for an inner join:
merged_df = pd.merge(df1, df2, on='NAME_1')
merged_df = pd.merge(merged_df, df3, on='NAME_1')

# Save the merged DataFrame to a new CSV file
# Replace 'path/to/merged_data.csv' with the desired path and filename for the merged CSV file.
output_path = '/content/merged_data.csv'
merged_df.to_csv(output_path, index=False)
merged_df


 
# Replace 'path/to/map_file.shp' with the actual path to your map file (shapefile)
map_file = '/content/drive/MyDrive/IND_adm1.shp'

# Read the map file using geopandas
map_data = gpd.read_file(map_file)
# Replace 'path/to/csv_file.csv' with the actual path to your CSV file
csv_file = '/content/merged_data.csv'

# Read the CSV file using pandas
csv_data = pd.read_csv(csv_file)
# Assuming 'common_key' is the common column between the CSV data and the map data
merged_data = map_data.merge(csv_data, on='NAME_1', how='left')
# Replace 'column_to_visualize' with the column from the CSV data you want to visualize on the map
column_to_visualize = 'NAME_1'

# Plot the map with the column_to_visualize
fig, ax = plt.subplots(figsize=(10, 8))
merged_data.plot(column=column_to_visualize, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Add a title
plt.title('Map Visualization with Merged Data')

# Display the plot
plt.show()

 

# Replace 'path/to/india_map.shp' with the actual path to your India map shapefile
india_map_shapefile = '/content/drive/MyDrive/IND_adm1.shp'

# Replace 'path/to/cancer_dataset.csv' with the actual path to your cancer dataset CSV file
cancer_data_csv = '/content/merged_data.csv'

# Read the India map shapefile
india_map = gpd.read_file(india_map_shapefile)

# Read the cancer dataset CSV file
cancer_data = pd.read_csv(cancer_data_csv)

# Calculate Moran's I, p-value, and z-score for each year's column
def calculate_morans_i(column_name):
    w = lib.weights.Queen.from_dataframe(india_map, silence_warnings=True)
    moran_loc = esda.Moran_Local(cancer_data[column_name].values, w, transformation='r', permutations=999)
    cancer_data['moran_i_' + column_name] = moran_loc.Is
    cancer_data['p_value_' + column_name] = moran_loc.p_sim
    cancer_data['z_score_' + column_name] = moran_loc.z_sim

# Calculate Moran's I, p-value, and z-score for each year's column
calculate_morans_i('Total2019')
calculate_morans_i('Total2020')
calculate_morans_i('Total2021')

# Merge the calculated Moran's I values with the India map data based on the state name
india_map = india_map.merge(cancer_data[['NAME_1', 'moran_i_Total2019', 'p_value_Total2019', 'z_score_Total2019',
                                         'moran_i_Total2020', 'p_value_Total2020', 'z_score_Total2020',
                                         'moran_i_Total2021', 'p_value_Total2021', 'z_score_Total2021']],
                            on='NAME_1', how='left')

# Plot the Moran's I values for each year on the map
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
india_map.plot(column='moran_i_Total2019', cmap='RdYlBu', linewidth=0.8, ax=axes[0], edgecolor='0.8', legend=True)
india_map.plot(column='moran_i_Total2020', cmap='RdYlBu', linewidth=0.8, ax=axes[1], edgecolor='0.8', legend=True)
india_map.plot(column='moran_i_Total2021', cmap='RdYlBu', linewidth=0.8, ax=axes[2], edgecolor='0.8', legend=True)

# Add titles
axes[0].set_title("Moran's I - Year 2019")
axes[1].set_title("Moran's I - Year 2020")
axes[2].set_title("Moran's I - Year 2021")

# Display the plots
plt.show()

 

# Load the datasets for each year (replace with your actual CSV files)
year19_data = pd.read_csv('/content/drive/MyDrive/2019.csv')
year20_data = pd.read_csv('/content/drive/MyDrive/2020.csv')
year21_data = pd.read_csv('/content/drive/MyDrive/2021.csv')

# Create separate GeoDataFrames for each year using latitude and longitude as geometry
gdf19 = gpd.GeoDataFrame(year19_data, geometry=gpd.points_from_xy(year19_data.Longitude, year19_data.Latitude))
gdf20 = gpd.GeoDataFrame(year20_data, geometry=gpd.points_from_xy(year20_data.Longitude, year20_data.Latitude))
gdf21 = gpd.GeoDataFrame(year21_data, geometry=gpd.points_from_xy(year21_data.Longitude, year21_data.Latitude))

# Create a spatial weights matrix (using K-nearest neighbors with k=5 as an example)
# Replace 'geometry' with the actual geometry column name in your GeoDataFrames
k = 5
w19 = weights.KNN.from_dataframe(gdf19, k=k, ids=gdf19.index)
w20 = weights.KNN.from_dataframe(gdf20, k=k, ids=gdf20.index)
w21 = weights.KNN.from_dataframe(gdf21, k=k, ids=gdf21.index)

# Calculate Moran's I for breast cancer cases for each year
morans_i_results = {}
for year, w, data in [(19, w19, year19_data), (20, w20, year20_data), (21, w21, year21_data)]:
    y_breast_cancer = data['Breastcancer' + str(year)].values
    moran_breast_cancer = Moran(y_breast_cancer, w)

    y_cervix_uteri = data['CervixUteri' + str(year)].values
    moran_cervix_uteri = Moran(y_cervix_uteri, w)

    # Store the results in the dictionary
    morans_i_results[year] = {
        "Breast Cancer - Moran's I": moran_breast_cancer.I,
        "Breast Cancer - p-value": moran_breast_cancer.p_sim,
        "Breast Cancer - Z-score": moran_breast_cancer.z_sim,
        "Cervix Uteri - Moran's I": moran_cervix_uteri.I,
        "Cervix Uteri - p-value": moran_cervix_uteri.p_sim,
        "Cervix Uteri - Z-score": moran_cervix_uteri.z_sim,
    }

# Print the results for each year
for year, result in morans_i_results.items():
    print(f"Year: {year}")
    print("Breast Cancer - Moran's I:", result["Breast Cancer - Moran's I"])
    print("Breast Cancer - p-value:", result["Breast Cancer - p-value"])
    print("Breast Cancer - Z-score:", result["Breast Cancer - Z-score"])
    print("Cervix Uteri - Moran's I:", result["Cervix Uteri - Moran's I"])
    print("Cervix Uteri - p-value:", result["Cervix Uteri - p-value"])
    print("Cervix Uteri - Z-score:", result["Cervix Uteri - Z-score"])
    print("-----------------------")

 

# Assuming you have a GeoDataFrame called 'cancer_gdf' containing data for each year (2019, 2020, 2021) and state-wise
# Replace '2019casescolumn', '2020casescolumn', and '2021casescolumn' with the column names containing the number of cases for the respective years
# Load the datasets for each year (replace with your actual CSV files)
year19_data = pd.read_csv('/content/drive/MyDrive/2019.csv')
year20_data = pd.read_csv('/content/drive/MyDrive/2020.csv')
year21_data = pd.read_csv('/content/drive/MyDrive/2021.csv')

india_map=gpd.read_file('/content/drive/MyDrive/IND_adm1.shp')
merged_df = pd.merge(year19_data, year20_data, on='NAME_1')
merged_data = pd.merge(merged_df, year21_data, on='NAME_1')

# Extract data for the years 2019, 2020, and 2021
year_data = merged_data[['NAME_1', 'Total2019', 'Total2020', 'Total2021', 'Latitude', 'Longitude']]

# Create a spatial weights matrix using K-nearest neighbors with latitude and longitude columns for all years
k = 5  # Number of nearest neighbors to consider
w_2019 = weights.KNN.from_array(year_data[['Latitude', 'Longitude']].values, k=k)
w_2020 = weights.KNN.from_array(year_data[['Latitude', 'Longitude']].values, k=k)
w_2021 = weights.KNN.from_array(year_data[['Latitude', 'Longitude']].values, k=k)

# Calculate Moran's I for all years
moran_2019 = Moran(year_data['Total2019'].values, w_2019)
moran_2020 = Moran(year_data['Total2020'].values, w_2020)
moran_2021 = Moran(year_data['Total2021'].values, w_2021)

# Create a DataFrame to store the results
results_df = pd.DataFrame({
    'Year': ['2019', '2020', '2021'],
    "Moran's I": [moran_2019.I, moran_2020.I, moran_2021.I]
})

# Plot the Moran's I index as a line plot
plt.figure(figsize=(8, 6))
plt.plot(results_df['Year'], results_df["Moran's I"], marker='o', color='skyblue')
plt.xlabel('Year')
plt.ylabel("Moran's I")
plt.title("Spatial Autocorrelation (Moran's I) for 2019, 2020, and 2021 Cases")
plt.grid(True)
plt.show()



 

# Assuming you have a GeoDataFrame called 'cancer_gdf' containing data for each year (2019, 2020, 2021) and state-wise
# Replace '2019casescolumn', '2020casescolumn', and '2021casescolumn' with the column names containing the number of cases for the respective years

# Extract data for the years 2019, 2020, and 2021
year_data = merged_data[['NAME_1', 'Total2019', 'Total2020','Total2021','Latitude', 'Longitude']]

# Extract the number of cases for each year
y_2019 = year_data['Total2019'].values
y_2020 = year_data['Total2020'].values
y_2021 = year_data['Total2021'].values

# Create a spatial weights matrix using K-nearest neighbors with latitude and longitude columns for all years
k = 5  # Number of nearest neighbors to consider
w_2019 = weights.KNN.from_array(year_data[['Latitude', 'Longitude']].values, k=k)
w_2020 = weights.KNN.from_array(year_data[['Latitude', 'Longitude']].values, k=k)
w_2021 = weights.KNN.from_array(year_data[['Latitude', 'Longitude']].values, k=k)

# Calculate Moran's I for all years
moran_2019 = Moran(y_2019, w_2019)
moran_2020 = Moran(y_2020, w_2020)
moran_2021 = Moran(y_2021, w_2021)

# Create a DataFrame to store the results
results_df = pd.DataFrame({
    'Year': ['2019', '2020', '2021'],
    "Moran's I": [moran_2019.I, moran_2020.I, moran_2021.I],
    "p-value": [moran_2019.p_sim, moran_2020.p_sim, moran_2021.p_sim],
    "Z-score": [moran_2019.z_sim, moran_2020.z_sim, moran_2021.z_sim]
})

# Plot the Moran's I index, p-value, and z-score in a line plot
plt.figure(figsize=(10, 6))
plt.plot(results_df['Year'], results_df["Moran's I"], label="Moran's I", marker='o', color='skyblue')
plt.plot(results_df['Year'], results_df["p-value"], label="p-value", marker='o', color='orange')
plt.plot(results_df['Year'], results_df["Z-score"], label="Z-score", marker='o', color='green')
plt.xlabel('Year')
plt.ylabel("Value")
plt.title("Spatial Autocorrelation (Moran's I) for 2019, 2020, and 2021 Cases")
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

# Print the results
print("Results for 2019:")
print(f"Moran's I Value: {moran_2019.I:.4f}")
print(f"P-Value: {moran_2019.p_sim:.4f}")
print(f"Z-Score: {moran_2019.z_sim:.4f}")
print("\n")

print("Results for 2020:")
print(f"Moran's I Value: {moran_2020.I:.4f}")
print(f"P-Value: {moran_2020.p_sim:.4f}")
print(f"Z-Score: {moran_2020.z_sim:.4f}")
print("\n")

print("Results for 2021:")
print(f"Moran's I Value: {moran_2021.I:.4f}")
print(f"P-Value: {moran_2021.p_sim:.4f}")
print(f"Z-Score: {moran_2021.z_sim:.4f}")

 

# Step 1: Read and preprocess the death cases data
# Replace 'path_to_your_death_cases_data.csv' with the actual path to your death cases data CSV file
death_cases_file = '/content/merged_data.csv'
death_cases_df = pd.read_csv(death_cases_file)

# Step 2: Read the India map shapefile
# Replace 'path_to_your_india_shapefile.shp' with the actual path to your India shapefile
india_map_shapefile = '/content/drive/MyDrive/IND_adm1.shp'
india_map_gdf = gpd.read_file(india_map_shapefile)

# Step 3: Merge death cases data with India map based on the 'State' column
merged_gdf = pd.merge(india_map_gdf, death_cases_df, on='NAME_1')

# Step 3: Perform Local Moran's I analysis to identify hotspots
cancer_cases = merged_gdf['activecases19'].values
k = 5  # Number of nearest neighbors to consider
w = weights.KNN.from_dataframe(merged_gdf, k=k)
moran_local = Moran_Local(cancer_cases, w)

# Step 4: Classify hotspots based on the Local Moran's I results
hotspots = moran_local.q == 1  # Regions with positive and significant Local Moran's I values

# Step 5: Add hotspot classification to the GeoDataFrame
merged_gdf['Hotspot'] = 'Not Hotspot'  # Default value
merged_gdf.loc[hotspots, 'Hotspot'] = 'Hotspot'

# Step 6: Plot hotspots on the India map
plt.figure(figsize=(10, 8))
merged_gdf.plot(column="Hotspot", cmap='coolwarm', linewidth=0.8, edgecolor='0.8', legend=True)
plt.title("Hotspots Analysis (Local Moran's I) for Activecases")
plt.show()



 

# Step 3: Perform Local Moran's I analysis to identify hotspots
cancer_cases = merged_gdf['Breastcancer19'].values
k = 5  # Number of nearest neighbors to consider
w = weights.KNN.from_dataframe(merged_gdf, k=k)
moran_local = Moran_Local(cancer_cases, w)

# Step 4: Classify hotspots based on the Local Moran's I results
hotspots = moran_local.q == 1  # Regions with positive and significant Local Moran's I values

# Step 5: Add hotspot classification to the GeoDataFrame
merged_gdf['Hotspot'] = 'Not Hotspot'  # Default value
merged_gdf.loc[hotspots, 'Hotspot'] = 'Hotspot'

# Step 6: Plot hotspots on the India map
plt.figure(figsize=(10, 8))
merged_gdf.plot(column="Hotspot", cmap='copper', linewidth=0.8, edgecolor='0.8', legend=True)
plt.title("Hotspots Analysis (Local Moran's I) for Breastcancer")
plt.show()

 

# Step 3: Perform Local Moran's I analysis to identify hotspots
cancer_cases = merged_gdf['CervixUteri21'].values
k = 5  # Number of nearest neighbors to consider
w = weights.KNN.from_dataframe(merged_gdf, k=k)
moran_local = Moran_Local(cancer_cases, w)

# Step 4: Classify hotspots based on the Local Moran's I results
hotspots = moran_local.q == 1  # Regions with positive and significant Local Moran's I values

# Step 5: Add hotspot classification to the GeoDataFrame
merged_gdf['Hotspot'] = 'Not Hotspot'  # Default value
merged_gdf.loc[hotspots, 'Hotspot'] = 'Hotspot'

# Step 6: Plot hotspots on the India map
plt.figure(figsize=(10, 8))
merged_gdf.plot(column="Hotspot", cmap='cividis', linewidth=0.8, edgecolor='0.8', legend=True)
plt.title("Hotspots Analysis (Local Moran's I) for CervixUteri cases")
plt.show()

 
Model Implementation:

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Step 1: Load your cancer dataset (assuming it's already preprocessed and contains 'year', 'activecases', 'deathcases', 'breast', and 'cervixuteri' columns)
cancer_data = pd.read_csv('/content/merged_data.csv')

# Step 2: Split the data into features (X) and target (y)
X = cancer_data[['Year19','Year20','Year21','activecases19','activecases20','activecases21','Breastcancer19','Breastcancer20','Breastcancer21',
                      'CervixUteri19','CervixUteri20','CervixUteri21','deathcases19','deathcases20','deathcases21']]
y = cancer_data['deathcases21']

# Step 3: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Create and train the models
rf_model = RandomForestRegressor()
gb_model = GradientBoostingRegressor()

rf_model.fit(X_train, y_train)
gb_model.fit(X_train, y_train)

# Step 5: Make predictions on the test set
y_pred_rf = rf_model.predict(X_test)
y_pred_gb = gb_model.predict(X_test)
y_pred_ridge = ridge_model.predict(X_test)
y_pred_lasso = lasso_model.predict(X_test)

# Step 6: Evaluate the models using metrics
mse_rf = mean_squared_error(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

mse_gb = mean_squared_error(y_test, y_pred_gb)
mae_gb = mean_absolute_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

# Step 7: Print the evaluation metrics
print("Random Forest Regressor:")
print("MSE:", mse_rf)
print("MAE:", mae_rf)
print("R-squared:", r2_rf)

print("\nGradient Boosting Regressor:")
print("MSE:", mse_gb)
print("MAE:", mae_gb)
print("R-squared:", r2_gb)


 

# Step 8: Create subplots for each model
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
axs = axs.ravel()

# Plot actual vs predicted for Random Forest Regressor
axs[0].scatter(y_test, y_pred_rf, alpha=0.5)
axs[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
axs[0].set_xlabel('Actual')
axs[0].set_ylabel('Predicted')
axs[0].set_title('Random Forest Regressor')

# Plot actual vs predicted for Gradient Boosting Regressor
axs[1].scatter(y_test, y_pred_gb, alpha=0.5)
axs[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
axs[1].set_xlabel('Actual')
axs[1].set_ylabel('Predicted')
axs[1].set_title('Gradient Boosting Regressor')
plt.tight_layout()
plt.show()

 
# Step 9: Compare the actual and predicted values on random forest
predictions_df = pd.DataFrame({'Actual Cases': y_test, 'Predicted Cases': y_pred_rf})
print(predictions_df)

 
# Step 10: actual and predicted values on Random Forest based on any year
comparison_df = pd.DataFrame({'Year': X_test['Year21'], 'Actual Death Cases': y_test, 'Predicted Death Cases': y_pred_rf})
print(comparison_df)
 
# Step 11: compare actual and predicted values on gradientBoosting on any year
comparison_df = pd.DataFrame({'Year': X_test['Year21'], 'Actual Death Cases': y_test, 'Predicted Death Cases': y_pred_gb})
print(comparison_df)

 
import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have a DataFrame named 'cancer_data' containing statewise cancer cases data
# with columns 'NAME_1', 'activecase', 'Breastcanc', 'CervixUter', and 'deathcases'

# Calculate the total cases for each state
state_total_cases = cancer_data.groupby('NAME_1')[['activecases19','activecases20','activecases21','Breastcancer19','Breastcancer20','Breastcancer21',
                      'CervixUteri19','CervixUteri20','CervixUteri21','deathcases19','deathcases20','deathcases21']].sum()

# Create a pie chart
plt.figure(figsize=(10, 6))
plt.pie(state_total_cases.sum(), labels=state_total_cases.columns, autopct='%1.1f%%')
plt.title('Percentage of Cancer Cases based on year wise on states')
plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.

# Show the pie chart
plt.show()

 
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Cancer analysis") \
    .getOrCreate()

# Read the CSV file into a DataFrame
csv_file_path = "/content/merged_data.csv"
df = spark.read.option("header", "true").csv(csv_file_path)

# Show the DataFrame's schema
df.printSchema()

# Display the first few rows of the DataFrame
df.show()

 
