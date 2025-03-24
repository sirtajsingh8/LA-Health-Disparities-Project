# Import
import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import logging
import traceback
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("la_health_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Database Connection
def connect_to_database():
    """
    Connect to our SQL Server database.

    Returns:
        connection: A connection to the SQL Server database or None if connection fails
    """
    logger.info("Connecting to the database...")

    # Database connection details
    server = 'DESKTOP-7A92MUU'
    database = 'LAHealthDisparities'

    #Windows Authentication
    try:
        # Windows Authentication connection string
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes'
        connection = pyodbc.connect(connection_string)
        logger.info("Successfully connected to the database using Windows Authentication!")
        return connection
    except Exception as e:
        logger.warning(f"Windows Authentication failed: {e}")

        # If Windows Authentication fails, check for other available drivers
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
                driver = pyodbc.drivers()[0]

            connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes'
            connection = pyodbc.connect(connection_string)
            logger.info(f"Successfully connected to the database using {driver}!")
            return connection
        except Exception as e:
            logger.error(f"All connection attempts failed: {e}")
            return None


# Function to generate synthetic health data
def generate_health_data():
    """
    Generate synthetic health data for LA County ZIP codes.

    Returns:
        pandas.DataFrame: DataFrame containing health indicators by ZIP code
    """
    logger.info("Generating synthetic health data...")

    # LA County ZIP codes
    zip_codes = ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90010',
                 # ... zip codes continue ...
                 '93591']

    communities = [
        'Florence-Graham', 'Watts', 'South Central LA', 'Koreatown', 'Westlake', 'Pico-Union',
        # ... communities continue ...
        'Palmdale', 'Valyermo', 'Palmdale'
    ]

    #DataFrame with synthetic health data
    np.random.seed(42)  # For reproducibility

    health_data = pd.DataFrame({
        'ZIPCode': zip_codes,
        'CommunityName': communities,
        'DiabetesPrevalence': np.random.uniform(5, 25, len(zip_codes)),
        'HeartDiseasePrevalence': np.random.uniform(3, 15, len(zip_codes)),
        'AsthmaPrevalence': np.random.uniform(8, 22, len(zip_codes)),
        'HypertensionPrevalence': np.random.uniform(15, 40, len(zip_codes)),
        'ObesityPrevalence': np.random.uniform(10, 35, len(zip_codes)),
        'MentalHealthDisordersPrevalence': np.random.uniform(10, 30, len(zip_codes)),
        'PreventableHospitalizations': np.random.uniform(100, 500, len(zip_codes)),
        'LifeExpectancy': np.random.uniform(75, 90, len(zip_codes)),
    })

    logger.info(f"Successfully generated health data for {len(health_data)} ZIP codes.")
    return health_data


# Function to generate demographic data
def generate_demographic_data():
    """
    Generate synthetic demographic data for LA County ZIP codes.

    Returns:
        pandas.DataFrame: DataFrame containing demographic information by ZIP code
    """

    logger.info("Generating demographic data...")

    # Use the same ZIP codes as in the health data function
    zip_codes = ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90010',
                 '90011', '90012', '90013', '90014', '90015', '90016', '90017', '90018', '90019',
                 '90020', '90021', '90022', '90023', '90024', '90025', '90026', '90027', '90028',
                 '90029', '90031', '90032', '90033', '90034', '90035', '90036', '90037', '90038',
                 '90039', '90040', '90041', '90042', '90043', '90044', '90045', '90046', '90047',
                 '90048', '90049', '90056', '90057', '90058', '90059', '90061', '90062', '90063',
                 '90064', '90065', '90066', '90067', '90068', '90069', '90071', '90077', '90089',
                 '90090', '90094', '90210', '90211', '90212', '90230', '90232', '90245', '90247',
                 '90248', '90272', '90290', '90291', '90292', '90293', '90301', '90302', '90303',
                 '90304', '90305', '90401', '90402', '90403', '90404', '90405', '90501', '90502',
                 '90710', '90717', '90731', '90732', '90744', '90745', '90810', '90813', '91001',
                 '91006', '91007', '91010', '91011', '91016', '91020', '91024', '91030', '91040',
                 '91042', '91105', '91106', '91108', '91201', '91202', '91203', '91204', '91205',
                 '91206', '91207', '91208', '91210', '91214', '91303', '91304', '91306', '91307',
                 '91311', '91316', '91324', '91325', '91331', '91335', '91340', '91342', '91343',
                 '91344', '91345', '91352', '91356', '91364', '91367', '91371', '91401', '91402',
                 '91403', '91405', '91406', '91411', '91423', '91436', '91501', '91502', '91504',
                 '91505', '91506', '91601', '91602', '91604', '91605', '91606', '91607', '93510',
                 '93532', '93534', '93535', '93536', '93543', '93550', '93551', '93552', '93563',
                 '93591']

    # Generate synthetic demographic data
    np.random.seed(42)  # For reproducibility

    # Correlations between income, poverty, and uninsured rates
    base_income = np.random.uniform(30000, 200000, len(zip_codes))

    # Sorted incomes to create realistic patterns
    sorted_indices = np.argsort(base_income)

    # Inverse patterns for poverty and uninsured rates
    poverty_rates = 30 - (base_income / 10000)
    poverty_rates = np.clip(poverty_rates, 1, 40)

    uninsured_rates = 25 - (base_income / 15000)
    uninsured_rates = np.clip(uninsured_rates, 1, 30)

    # Correlation between minority percentage and income
    # Note: This is synthetic data and not meant to represent actual demographic patterns
    minority_percentages = np.random.uniform(20, 95, len(zip_codes))

    # Adjust social vulnerability index based on other factors
    svi_base = (poverty_rates / 40) * 0.4 + (uninsured_rates / 30) * 0.3 + (minority_percentages / 100) * 0.3
    svi = svi_base * 10  # Scale to 0-10

    demographic_data = pd.DataFrame({
        'ZIPCode': zip_codes,
        'TotalPopulation': np.random.randint(10000, 70000, len(zip_codes)),
        'MedianIncome': base_income,
        'PercentMinority': minority_percentages,
        'PercentPoverty': poverty_rates,
        'PercentUninsured': uninsured_rates,
        'SocialVulnerabilityIndex': svi
    })

    logger.info(f"Successfully generated demographic data for {len(demographic_data)} ZIP codes.")
    return demographic_data


# Function to generate healthcare access data
def generate_healthcare_access_data():
    """
    Generate synthetic healthcare access data.

    Returns:
        pandas.DataFrame: DataFrame containing healthcare access metrics by ZIP code
    """
    logger.info("Generating healthcare access data...")

    # Use the same ZIP codes as before
    zip_codes = ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90010',
                 '90011', '90012', '90013', '90014', '90015', '90016', '90017', '90018', '90019',
                 '90020', '90021', '90022', '90023', '90024', '90025', '90026', '90027', '90028',
                 '90029', '90031', '90032', '90033', '90034', '90035', '90036', '90037', '90038',
                 '90039', '90040', '90041', '90042', '90043', '90044', '90045', '90046', '90047',
                 '90048', '90049', '90056', '90057', '90058', '90059', '90061', '90062', '90063',
                 '90064', '90065', '90066', '90067', '90068', '90069', '90071', '90077', '90089',
                 '90090', '90094', '90210', '90211', '90212', '90230', '90232', '90245', '90247',
                 '90248', '90272', '90290', '90291', '90292', '90293', '90301', '90302', '90303',
                 '90304', '90305', '90401', '90402', '90403', '90404', '90405', '90501', '90502',
                 '90710', '90717', '90731', '90732', '90744', '90745', '90810', '90813', '91001',
                 '91006', '91007', '91010', '91011', '91016', '91020', '91024', '91030', '91040',
                 '91042', '91105', '91106', '91108', '91201', '91202', '91203', '91204', '91205',
                 '91206', '91207', '91208', '91210', '91214', '91303', '91304', '91306', '91307',
                 '91311', '91316', '91324', '91325', '91331', '91335', '91340', '91342', '91343',
                 '91344', '91345', '91352', '91356', '91364', '91367', '91371', '91401', '91402',
                 '91403', '91405', '91406', '91411', '91423', '91436', '91501', '91502', '91504',
                 '91505', '91506', '91601', '91602', '91604', '91605', '91606', '91607', '93510',
                 '93532', '93534', '93535', '93536', '93543', '93550', '93551', '93552', '93563',
                 '93591']

    # Demographic data to create correlated healthcare access barriers
    demographic_data = generate_demographic_data()

    # Correlations between income and healthcare access
    np.random.seed(42)  # For reproducibility

    # Base DataFrame
    healthcare_access = pd.DataFrame({'ZIPCode': zip_codes})

    # Join with demographic data
    healthcare_access = healthcare_access.merge(
        demographic_data[['ZIPCode', 'MedianIncome', 'PercentPoverty', 'PercentUninsured']],
        on='ZIPCode'
    )

    # Correlated healthcare access metrics
    # Lower income areas tend to have less healthcare access
    income_factor = (200000 - healthcare_access['MedianIncome']) / 200000

    healthcare_access['PercentNoRegularCheckup'] = 15 + (income_factor * 40) + np.random.normal(0, 5, len(zip_codes))
    healthcare_access['PercentNoRegularCheckup'] = np.clip(healthcare_access['PercentNoRegularCheckup'], 5, 70)

    healthcare_access['PercentDelayedCare'] = 10 + (income_factor * 30) + np.random.normal(0, 5, len(zip_codes))
    healthcare_access['PercentDelayedCare'] = np.clip(healthcare_access['PercentDelayedCare'], 5, 60)

    healthcare_access['PercentNoTransportation'] = 5 + (income_factor * 25) + np.random.normal(0, 3, len(zip_codes))
    healthcare_access['PercentNoTransportation'] = np.clip(healthcare_access['PercentNoTransportation'], 1, 40)

    healthcare_access['AvgDistanceToHospital'] = 1 + (income_factor * 8) + np.random.normal(0, 1, len(zip_codes))
    healthcare_access['AvgDistanceToHospital'] = np.clip(healthcare_access['AvgDistanceToHospital'], 0.5, 15)

    healthcare_access['AvgDistanceToClinic'] = 0.5 + (income_factor * 5) + np.random.normal(0, 0.8, len(zip_codes))
    healthcare_access['AvgDistanceToClinic'] = np.clip(healthcare_access['AvgDistanceToClinic'], 0.2, 10)

    # Public transit access (higher score is better)
    healthcare_access['PublicTransitAccessScore'] = 80 - (income_factor * 60) + np.random.normal(0, 10, len(zip_codes))
    healthcare_access['PublicTransitAccessScore'] = np.clip(healthcare_access['PublicTransitAccessScore'], 10, 95)

    # Digital divide (higher score means bigger divide)
    healthcare_access['DigitalDivideIndex'] = 10 + (income_factor * 70) + np.random.normal(0, 10, len(zip_codes))
    healthcare_access['DigitalDivideIndex'] = np.clip(healthcare_access['DigitalDivideIndex'], 5, 90)

    # Remove the demographic columns now that I've used them for correlation
    healthcare_access = healthcare_access.drop(['MedianIncome', 'PercentPoverty', 'PercentUninsured'], axis=1)

    logger.info(f"Successfully generated healthcare access data for {len(healthcare_access)} ZIP codes.")
    return healthcare_access


# Function to generate environmental health data
def generate_environmental_data():
    """
    Generate synthetic environmental health data.

    Returns:
        pandas.DataFrame: DataFrame containing environmental health metrics by ZIP code
    """
    logger.info("Generating environmental health data...")

    # Use the same ZIP codes as before
    zip_codes = ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90010',
                 '90011', '90012', '90013', '90014', '90015', '90016', '90017', '90018', '90019',
                 '90020', '90021', '90022', '90023', '90024', '90025', '90026', '90027', '90028',
                 '90029', '90031', '90032', '90033', '90034', '90035', '90036', '90037', '90038',
                 '90039', '90040', '90041', '90042', '90043', '90044', '90045', '90046', '90047',
                 '90048', '90049', '90056', '90057', '90058', '90059', '90061', '90062', '90063',
                 '90064', '90065', '90066', '90067', '90068', '90069', '90071', '90077', '90089',
                 '90090', '90094', '90210', '90211', '90212', '90230', '90232', '90245', '90247',
                 '90248', '90272', '90290', '90291', '90292', '90293', '90301', '90302', '90303',
                 '90304', '90305', '90401', '90402', '90403', '90404', '90405', '90501', '90502',
                 '90710', '90717', '90731', '90732', '90744', '90745', '90810', '90813', '91001',
                 '91006', '91007', '91010', '91011', '91016', '91020', '91024', '91030', '91040',
                 '91042', '91105', '91106', '91108', '91201', '91202', '91203', '91204', '91205',
                 '91206', '91207', '91208', '91210', '91214', '91303', '91304', '91306', '91307',
                 '91311', '91316', '91324', '91325', '91331', '91335', '91340', '91342', '91343',
                 '91344', '91345', '91352', '91356', '91364', '91367', '91371', '91401', '91402',
                 '91403', '91405', '91406', '91411', '91423', '91436', '91501', '91502', '91504',
                 '91505', '91506', '91601', '91602', '91604', '91605', '91606', '91607', '93510',
                 '93532', '93534', '93535', '93536', '93543', '93550', '93551', '93552', '93563',
                 '93591']

    # Get demographic data to create correlations
    demographic_data = generate_demographic_data()

    # Base DataFrame
    environmental_data = pd.DataFrame({'ZIPCode': zip_codes})

    # Join with demographic data
    environmental_data = environmental_data.merge(
        demographic_data[['ZIPCode', 'MedianIncome', 'PercentPoverty']],
        on='ZIPCode'
    )

    # Correlated environmental metrics
    # Lower income areas tend to have worse environmental conditions
    np.random.seed(42)  # For reproducibility

    income_factor = (200000 - environmental_data['MedianIncome']) / 200000

    # Air pollution (higher is worse)
    environmental_data['AirPollutionIndex'] = 20 + (income_factor * 60) + np.random.normal(0, 10, len(zip_codes))
    environmental_data['AirPollutionIndex'] = np.clip(environmental_data['AirPollutionIndex'], 10, 95)

    # Water quality (higher is better)
    environmental_data['WaterQualityIndex'] = 90 - (income_factor * 40) + np.random.normal(0, 10, len(zip_codes))
    environmental_data['WaterQualityIndex'] = np.clip(environmental_data['WaterQualityIndex'], 30, 98)

    # Food desert score (higher is worse)
    environmental_data['FoodDesertScore'] = 10 + (income_factor * 70) + np.random.normal(0, 15, len(zip_codes))
    environmental_data['FoodDesertScore'] = np.clip(environmental_data['FoodDesertScore'], 5, 95)

    # Green space access (percentage of population with park access)
    environmental_data['GreenSpaceAccess'] = 80 - (income_factor * 60) + np.random.normal(0, 10, len(zip_codes))
    environmental_data['GreenSpaceAccess'] = np.clip(environmental_data['GreenSpaceAccess'], 5, 95)

    # CalEnviroScreen score (higher is worse)
    environmental_data['CalEnviroScreenScore'] = 15 + (income_factor * 70) + np.random.normal(0, 10, len(zip_codes))
    environmental_data['CalEnviroScreenScore'] = np.clip(environmental_data['CalEnviroScreenScore'], 10, 95)

    # Remove the demographic columns now that we've used them for correlation
    environmental_data = environmental_data.drop(['MedianIncome', 'PercentPoverty'], axis=1)

    logger.info(f"Successfully generated environmental data for {len(environmental_data)} ZIP codes.")
    return environmental_data


# Function to generate healthcare facility data
def generate_healthcare_facilities():
    """
    Generate synthetic data on healthcare facilities in LA County.

    Returns:
        pandas.DataFrame: DataFrame containing healthcare facility information
    """
    logger.info("Generating healthcare facility data...")

    # Use a subset of ZIP codes to distribute facilities
    zip_codes = ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90010',
                 '90011', '90012', '90013', '90014', '90015', '90016', '90017', '90018', '90019',
                 '90020', '90021', '90022', '90023', '90024', '90025', '90026', '90027', '90028',
                 '90029', '90031', '90032', '90033', '90034', '90035', '90036', '90037', '90038',
                 '90039', '90040', '90041', '90042', '90043', '90044', '90045', '90046', '90047',
                 '90048', '90049', '90056', '90057', '90058', '90059', '90061', '90062', '90063',
                 '90064', '90065', '90066', '90067', '90068', '90069', '90071', '90077', '90089',
                 '90090', '90094', '90210', '90211', '90212', '90230', '90232', '90245', '90247',
                 '90248', '90272', '90290', '90291', '90292', '90293', '90301', '90302', '90303',
                 '90304', '90305', '90401', '90402', '90403', '90404', '90405', '90501', '90502',
                 '90710', '90717', '90731', '90732', '90744', '90745', '90810', '90813', '91001',
                 '91006', '91007', '91010', '91011', '91016', '91020', '91024', '91030', '91040',
                 '91042', '91105', '91106', '91108', '91201', '91202', '91203', '91204', '91205',
                 '91206', '91207', '91208', '91210', '91214', '91303', '91304', '91306', '91307',
                 '91311', '91316', '91324', '91325', '91331', '91335', '91340', '91342']