# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pyodbc
import os
from pathlib import Path
import logging

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 12


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("la_health_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Set up database connection
def connect_to_database():
    """
    Connect to our SQL Server database.

    Returns:
        connection: A connection to the SQL Server database or None if connection fails
    """
    logger.info("Connecting to the database...")

    # Database connection details
    server = 'DESKTOP-7A92MUU'  # Your server name
    database = 'LAHealthDisparities'  # Your database name

    # Try Windows Authentication first (more secure)
    try:
        # Windows Authentication connection string
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes'
        connection = pyodbc.connect(connection_string)
        logger.info("Successfully connected to the database using Windows Authentication!")
        return connection
    except Exception as e:
        logger.warning(f"Windows Authentication failed: {e}")

        # If Windows Authentication fails, try checking available drivers
        try:
            logger.info(f"Available ODBC drivers: {pyodbc.drivers()}")

            # Try with a different driver if "SQL Server" is not available
            if "ODBC Driver 17 for SQL Server" in pyodbc.drivers():
                driver = "ODBC Driver 17 for SQL Server"
            elif "ODBC Driver 18 for SQL Server" in pyodbc.drivers():
                driver = "ODBC Driver 18 for SQL Server"
            elif "SQL Server" in pyodbc.drivers():
                driver = "SQL Server"
            else:
                driver = pyodbc.drivers()[0]  # Use first available driver

            connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes'
            connection = pyodbc.connect(connection_string)
            logger.info(f"Successfully connected to the database using {driver}!")
            return connection
        except Exception as e:
            logger.error(f"All connection attempts failed: {e}")
            return None


# Function to fetch data for analysis
def fetch_data_for_analysis(connection):
    """
    Fetch data from our SQL Server database for analysis.

    Args:
        connection: Database connection

    Returns:
        dict: Dictionary containing different DataFrames for analysis
    """
    print("Fetching data for analysis...")

    try:
        # Use the CommunityHealthView view to get the combined data
        query = "SELECT * FROM CommunityHealthView"
        community_health_df = pd.read_sql(query, connection)

        # Fetch healthcare facilities data
        facilities_query = "SELECT * FROM HealthcareFacilities"
        facilities_df = pd.read_sql(facilities_query, connection)

        # Count facilities by ZIP code
        facility_counts = facilities_df.groupby(['ZIPCode', 'FacilityType']).size().unstack(fill_value=0)
        if 'Hospital' not in facility_counts.columns:
            facility_counts['Hospital'] = 0
        if 'Clinic' not in facility_counts.columns:
            facility_counts['Clinic'] = 0
        if 'Community Health Center' not in facility_counts.columns:
            facility_counts['Community Health Center'] = 0

        facility_counts['TotalFacilities'] = facility_counts.sum(axis=1)

        # Add facility counts to the main dataset
        community_health_with_facilities = community_health_df.merge(
            facility_counts, on='ZIPCode', how='left'
        )

        # Handle missing values
        community_health_with_facilities = community_health_with_facilities.fillna({
            'Hospital': 0,
            'Clinic': 0,
            'Community Health Center': 0,
            'TotalFacilities': 0
        })

        # Calculate per capita facility rates (per 10,000 residents)
        community_health_with_facilities['FacilitiesPer10k'] = (
                community_health_with_facilities['TotalFacilities'] /
                community_health_with_facilities['TotalPopulation'] * 10000
        )

        # Return all the data
        data_dict = {
            'community_health': community_health_with_facilities,
            'facilities': facilities_df
        }

        print(f"Successfully fetched data for {len(community_health_with_facilities)} ZIP codes.")
        return data_dict

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


# This should be at the left margin, no leading spaces or tabs
def identify_healthcare_disparities(df):
    """
    Identify healthcare disparities across LA County communities.

    Args:
        df: DataFrame with community health data

    Returns:
        DataFrame: Dataset with disparity metrics
    """
    # Function body indented by 4 spaces
    print("Identifying healthcare disparities...")

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Create a healthcare disparity index
    # Normalize factors to 0-100 scale (higher = worse disparity)

    # Health outcomes (higher = worse)
    health_factors = [
        'DiabetesPrevalence',
        'HeartDiseasePrevalence',
        'AsthmaPrevalence',
        'HypertensionPrevalence',
        'ObesityPrevalence',
        'MentalHealthDisordersPrevalence'
    ]

    # Access barriers (higher = worse)
    access_factors = [
        'PercentNoRegularCheckup',
        'PercentDelayedCare',
        'PercentNoTransportation',
        'AvgDistanceToHospital',
        'AvgDistanceToClinic'
    ]

    # Environmental factors (higher = worse, except WaterQualityIndex and GreenSpaceAccess)
    env_factors = [
        'AirPollutionIndex',
        'FoodDesertScore',
        'CalEnviroScreenScore'
    ]

    # Protective factors (higher = better)
    protective_factors = [
        'WaterQualityIndex',
        'GreenSpaceAccess',
        'FacilitiesPer10k',
        'PublicTransitAccessScore'
    ]

    # Create normalized versions of each metric
    scaler = StandardScaler()

    # For factors where higher values indicate worse outcomes
    for factors in [health_factors, access_factors, env_factors]:
        factor_cols = [col for col in factors if col in df.columns]
        if factor_cols:
            normalized_vals = scaler.fit_transform(df[factor_cols])
            for i, col in enumerate(factor_cols):
                df[f"{col}_normalized"] = normalized_vals[:, i]

    # For factors where higher values indicate better outcomes (invert the scale)
    protective_cols = [col for col in protective_factors if col in df.columns]
    if protective_cols:
        normalized_vals = -1 * scaler.fit_transform(df[protective_cols])
        for i, col in enumerate(protective_cols):
            df[f"{col}_normalized"] = normalized_vals[:, i]

    # Calculate a composite healthcare disparity index
    # Weighted average of all normalized factors
    health_norm_cols = [f"{col}_normalized" for col in health_factors if col in df.columns]
    access_norm_cols = [f"{col}_normalized" for col in access_factors if col in df.columns]
    env_norm_cols = [f"{col}_normalized" for col in env_factors if col in df.columns]
    protective_norm_cols = [f"{col}_normalized" for col in protective_factors if col in df.columns]

    df['HealthDisparityIndex'] = (
        # Health outcomes (40% weight)
            df[health_norm_cols].mean(axis=1) * 0.4 +
            # Access barriers (35% weight)
            df[access_norm_cols].mean(axis=1) * 0.35 +
            # Environmental factors (15% weight)
            df[env_norm_cols].mean(axis=1) * 0.15 +
            # Protective factors (10% weight)
            df[protective_norm_cols].mean(axis=1) * 0.1
    )

    # Normalize the index to a 0-100 scale for easier interpretation
    min_val = df['HealthDisparityIndex'].min()
    max_val = df['HealthDisparityIndex'].max()
    df['HealthDisparityIndex'] = ((df['HealthDisparityIndex'] - min_val) / (max_val - min_val)) * 100

    # Classify communities by disparity level
    df['DisparityLevel'] = pd.qcut(
        df['HealthDisparityIndex'],
        q=5,
        labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High']
    )

    print("Successfully identified healthcare disparities.")
    return df


# Function to perform clustering analysis
def cluster_communities(data):
    """
    Cluster communities by health and socioeconomic factors.

    Args:
        data: DataFrame with community health metrics

    Returns:
        DataFrame: Dataset with cluster assignments
    """
    print("Clustering communities by health and socioeconomic factors...")

    df = data.copy()

    # Select features for clustering
    feature_cols = [
        'MedianIncome', 'PercentMinority', 'PercentPoverty', 'PercentUninsured',
        'DiabetesPrevalence', 'HeartDiseasePrevalence', 'AsthmaPrevalence',
        'ObesityPrevalence', 'LifeExpectancy', 'AirPollutionIndex',
        'FoodDesertScore', 'FacilitiesPer10k'
    ]

    # Ensure all features are present
    feature_cols = [col for col in feature_cols if col in df.columns]

    # Prepare data for clustering
    X = df[feature_cols].copy()

    # Handle any missing values
    X = X.fillna(X.mean())

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Determine optimal number of clusters using the elbow method
    inertia = []
    k_range = range(2, 11)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    # Choose k=5 for simplicity in this example
    # In a real analysis, you would analyze the elbow curve
    k = 5

    # Perform k-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # Interpret clusters
    cluster_profiles = pd.DataFrame()
    for col in feature_cols:
        cluster_profiles[col] = df.groupby('Cluster')[col].mean()

    # Assign descriptive labels to clusters based on their characteristics
    cluster_labels = {}

    for cluster in range(k):
        profile = cluster_profiles.loc[cluster]

        # High income, good health outcomes
        if profile['MedianIncome'] > cluster_profiles['MedianIncome'].median() and profile['LifeExpectancy'] > \
                cluster_profiles['LifeExpectancy'].median():
            label = "High Resource / Good Health"

        # Low income, high minority, poor health outcomes
        elif profile['MedianIncome'] < cluster_profiles['MedianIncome'].median() and profile['PercentMinority'] > \
                cluster_profiles['PercentMinority'].median() and profile['DiabetesPrevalence'] > cluster_profiles[
            'DiabetesPrevalence'].median():
            label = "Underserved / Poor Health"

        # Low income, high environmental concerns
        elif profile['MedianIncome'] < cluster_profiles['MedianIncome'].median() and profile['AirPollutionIndex'] > \
                cluster_profiles['AirPollutionIndex'].median():
            label = "Environmental Justice Concerns"

        # Moderate income, food access issues
        elif profile['MedianIncome'] > cluster_profiles['MedianIncome'].min() and profile['FoodDesertScore'] > \
                cluster_profiles['FoodDesertScore'].median():
            label = "Food Access Challenges"

        # Other communities
        else:
            label = "Mixed Resources / Average Health"

        cluster_labels[cluster] = label

    # Add descriptive labels to the dataset
    df['CommunityProfile'] = df['Cluster'].map(cluster_labels)

    print("Successfully clustered communities.")
    return df, cluster_profiles


# Function to generate key insights
def generate_insights(data):
    """
    Generate key insights from the analysis.

    Args:
        data: DataFrame with analysis results

    Returns:
        list: List of key insights as text
    """
    print("Generating insights from the analysis...")

    insights = []

    # Most underserved areas
    high_disparity = data[data['DisparityLevel'] == 'Very High'].sort_values('HealthDisparityIndex', ascending=False)
    if not high_disparity.empty:
        top_3_underserved = high_disparity.head(3)
        insight = "Most underserved communities: " + ", ".join(top_3_underserved['CommunityName'])
        insights.append(insight)

    # Relationship between income and health outcomes
    income_groups = pd.qcut(data['MedianIncome'], q=4,
                            labels=['Low Income', 'Lower-Middle Income', 'Upper-Middle Income', 'High Income'])
    data['IncomeGroup'] = income_groups

    income_health = data.groupby('IncomeGroup')[
        ['DiabetesPrevalence', 'HeartDiseasePrevalence', 'LifeExpectancy']].mean()

    diabetes_diff = income_health.loc['Low Income', 'DiabetesPrevalence'] - income_health.loc[
        'High Income', 'DiabetesPrevalence']
    heart_diff = income_health.loc['Low Income', 'HeartDiseasePrevalence'] - income_health.loc[
        'High Income', 'HeartDiseasePrevalence']
    life_exp_diff = income_health.loc['High Income', 'LifeExpectancy'] - income_health.loc[
        'Low Income', 'LifeExpectancy']

    insight = f"Income-related health disparities: Low-income communities have {diabetes_diff:.1f}% higher diabetes rates, {heart_diff:.1f}% higher heart disease rates, and {life_exp_diff:.1f} years shorter life expectancy compared to high-income areas."
    insights.append(insight)

    # Facility distribution insights
    data['FacilityAccessScore'] = (10000 / data['TotalPopulation']) * data['TotalFacilities']

    facility_by_income = data.groupby('IncomeGroup')['FacilityAccessScore'].mean()
    high_vs_low = facility_by_income['High Income'] / facility_by_income['Low Income']

    insight = f"Healthcare facility distribution: High-income areas have {high_vs_low:.1f}x more healthcare facilities per capita than low-income areas."
    insights.append(insight)

    # Environmental health insights
    env_by_income = data.groupby('IncomeGroup')[['AirPollutionIndex', 'FoodDesertScore']].mean()

    air_diff = env_by_income.loc['Low Income', 'AirPollutionIndex'] - env_by_income.loc[
        'High Income', 'AirPollutionIndex']
    food_diff = env_by_income.loc['Low Income', 'FoodDesertScore'] - env_by_income.loc['High Income', 'FoodDesertScore']

    insight = f"Environmental justice concerns: Low-income communities face {air_diff:.1f}% higher air pollution levels and {food_diff:.1f}% worse food access compared to high-income areas."
    insights.append(insight)

    # Healthcare access insights
    access_by_income = data.groupby('IncomeGroup')[
        ['PercentNoRegularCheckup', 'PercentDelayedCare', 'AvgDistanceToHospital']].mean()

    checkup_diff = access_by_income.loc['Low Income', 'PercentNoRegularCheckup'] - access_by_income.loc[
        'High Income', 'PercentNoRegularCheckup']
    delay_diff = access_by_income.loc['Low Income', 'PercentDelayedCare'] - access_by_income.loc[
        'High Income', 'PercentDelayedCare']

    insight = f"Healthcare access barriers: Residents in low-income areas are {checkup_diff:.1f}% more likely to skip regular checkups and {delay_diff:.1f}% more likely to delay needed care compared to high-income areas."
    insights.append(insight)

    print("Successfully generated insights.")
    return insights


# Function to create visualizations for analysis
def create_visualizations(data, output_dir):
    """
    Create visualizations for health disparities analysis.

    Args:
        data: DataFrame with analysis results
        output_dir: Directory to save visualizations
    """
    print("Creating visualizations...")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # 1. Health Disparity Index by Income
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=data,
        x='MedianIncome',
        y='HealthDisparityIndex',
        hue='DisparityLevel',
        size='TotalPopulation',
        sizes=(50, 500),
        alpha=0.7
    )
    plt.title('Health Disparity Index vs. Median Income')
    plt.xlabel('Median Income ($)')
    plt.ylabel('Health Disparity Index (Higher = Worse)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_disparity_by_income.png'), dpi=300)
    plt.close()

    # 2. Chronic Disease Rates by Community Profile
    plt.figure(figsize=(14, 10))
    disease_vars = ['DiabetesPrevalence', 'HeartDiseasePrevalence', 'AsthmaPrevalence', 'HypertensionPrevalence',
                    'ObesityPrevalence']
    disease_data = data.groupby('CommunityProfile')[disease_vars].mean().reset_index()

    disease_data_melted = pd.melt(
        disease_data,
        id_vars=['CommunityProfile'],
        value_vars=disease_vars,
        var_name='Disease',
        value_name='Prevalence'
    )

    # Clean up disease names for display
    disease_data_melted['Disease'] = disease_data_melted['Disease'].str.replace('Prevalence', '')

    sns.barplot(
        data=disease_data_melted,
        x='CommunityProfile',
        y='Prevalence',
        hue='Disease'
    )
    plt.title('Chronic Disease Rates by Community Profile')
    plt.xlabel('Community Profile')
    plt.ylabel('Prevalence (%)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Disease')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_disease_by_profile.png'), dpi=300)
    plt.close()

    # 3. Healthcare Access Barriers by Community Profile
    plt.figure(figsize=(14, 10))
    access_vars = ['PercentNoRegularCheckup', 'PercentDelayedCare', 'PercentNoTransportation', 'AvgDistanceToHospital']
    access_data = data.groupby('CommunityProfile')[access_vars].mean().reset_index()

    access_data_melted = pd.melt(
        access_data,
        id_vars=['CommunityProfile'],
        value_vars=access_vars,
        var_name='Barrier',
        value_name='Value'
    )

    # Clean up barrier names for display
    barrier_mapping = {
        'PercentNoRegularCheckup': 'No Regular Checkup (%)',
        'PercentDelayedCare': 'Delayed Care (%)',
        'PercentNoTransportation': 'No Transportation (%)',
        'AvgDistanceToHospital': 'Avg. Distance to Hospital (mi)'
    }
    access_data_melted['Barrier'] = access_data_melted['Barrier'].map(barrier_mapping)

    sns.barplot(
        data=access_data_melted,
        x='CommunityProfile',
        y='Value',
        hue='Barrier'
    )
    plt.title('Healthcare Access Barriers by Community Profile')
    plt.xlabel('Community Profile')
    plt.ylabel('Value')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Barrier')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '3_access_barriers.png'), dpi=300)
    plt.close()

    # 4. Life Expectancy vs. Healthcare Facilities
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=data,
        x='FacilitiesPer10k',
        y='LifeExpectancy',
        hue='IncomeGroup',
        size='TotalPopulation',
        sizes=(50, 500),
        alpha=0.7
    )
    plt.title('Life Expectancy vs. Healthcare Facilities Per 10,000 Residents')
    plt.xlabel('Healthcare Facilities Per 10,000 Residents')
    plt.ylabel('Life Expectancy (Years)')
    plt.grid(True, alpha=0.3)

    # Add regression line
    sns.regplot(
        data=data,
        x='FacilitiesPer10k',
        y='LifeExpectancy',
        scatter=False,
        line_kws={'color': 'red', 'linestyle': '--'}
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '4_life_expectancy_facilities.png'), dpi=300)
    plt.close()

    # 5. Environmental Factors by Income Group
    plt.figure(figsize=(12, 8))
    env_vars = ['AirPollutionIndex', 'WaterQualityIndex', 'FoodDesertScore', 'GreenSpaceAccess']
    env_data = data.groupby('IncomeGroup')[env_vars].mean().reset_index()

    env_data_melted = pd.melt(
        env_data,
        id_vars=['IncomeGroup'],
        value_vars=env_vars,
        var_name='Environmental Factor',
        value_name='Score'
    )

    # Adjust order of income groups
    income_order = ['Low Income', 'Lower-Middle Income', 'Upper-Middle Income', 'High Income']
    env_data_melted['IncomeGroup'] = pd.Categorical(
        env_data_melted['IncomeGroup'],
        categories=income_order,
        ordered=True
    )

    sns.barplot(
        data=env_data_melted,
        x='IncomeGroup',
        y='Score',
        hue='Environmental Factor'
    )
    plt.title('Environmental Factors by Income Group')
    plt.xlabel('Income Group')
    plt.ylabel('Score')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_environmental_factors.png'), dpi=300)
    plt.close()

    print(f"Successfully created visualizations in {output_dir}.")


# Main function to run the analysis
def main():
    """
    Main function to orchestrate the health disparities analysis.
    """
    print("Starting LA County Health Disparities analysis...")

    # Add this line to check what functions are available
    print("Available functions:",
          [name for name in globals() if callable(globals()[name]) and name.startswith('identify')])

    # Step 1: Connect to the database
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to the database. Exiting...")
        return

    try:
        # Step 2: Fetch data for analysis
        data_dict = fetch_data_for_analysis(connection)
        if not data_dict:
            print("Failed to fetch data. Exiting...")
            return

        # Check if we got any data
        if len(data_dict['community_health']) == 0:
            print("No community health data found in database. Check your database tables.")
            return

        # Step 3: Identify healthcare disparities
        # Fixed: pass the DataFrame directly, not as a key in a dictionary
        disparity_data = identify_healthcare_disparities(data_dict['community_health'])

        # Step 4: Cluster communities
        clustered_data, cluster_profiles = cluster_communities(disparity_data)

        # Step 5: Generate insights
        insights = generate_insights(clustered_data)

        # Print insights
        print("\nKey Insights from Analysis:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")

        # Step 6: Create visualizations
        output_dir = 'visualizations'
        create_visualizations(clustered_data, output_dir)

        # Step 7: Save processed data for PowerBI
        # Create a directory for PowerBI data if it doesn't exist
        powerbi_dir = 'powerbi_data'
        os.makedirs(powerbi_dir, exist_ok=True)

        # Save the processed data for PowerBI
        clustered_data.to_csv(os.path.join(powerbi_dir, 'la_health_disparities_analysis.csv'), index=False)
        data_dict['facilities'].to_csv(os.path.join(powerbi_dir, 'healthcare_facilities.csv'), index=False)

        print("\nAnalysis complete! Data has been processed and saved for PowerBI visualization.")
        print(f"PowerBI data is available in the '{powerbi_dir}' directory.")
        print(f"Visualizations are available in the '{output_dir}' directory.")

    finally:
        # Close the database connection
        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()