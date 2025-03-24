-- Create our main database
CREATE DATABASE LAHealthDisparities;
GO

-- Use our new database
USE LAHealthDisparities;
GO

-- Create table for LA County ZIP codes with demographic information
CREATE TABLE ZIPCodes (
    ZIPCode VARCHAR(10) PRIMARY KEY,
    CommunityName VARCHAR(100),
    TotalPopulation INT,
    MedianIncome DECIMAL(10, 2),
    PercentMinority DECIMAL(5, 2),
    PercentPoverty DECIMAL(5, 2),
    PercentUninsured DECIMAL(5, 2),
    SocialVulnerabilityIndex DECIMAL(5, 2)
);

-- Create table for healthcare facilities
CREATE TABLE HealthcareFacilities (
    FacilityID INT IDENTITY(1,1) PRIMARY KEY,
    FacilityName VARCHAR(100),
    FacilityType VARCHAR(50),  -- Hospital, Clinic, Community Health Center, etc.
    ZIPCode VARCHAR(10),
    Address VARCHAR(200),
    HasEmergencyServices BIT,
    AcceptsMediCal BIT,
    AcceptsMedicare BIT,
    FOREIGN KEY (ZIPCode) REFERENCES ZIPCodes(ZIPCode)
);

-- Create table for health indicators by ZIP code
CREATE TABLE HealthIndicators (
    IndicatorID INT IDENTITY(1,1) PRIMARY KEY,
    ZIPCode VARCHAR(10),
    Year INT,
    DiabetesPrevalence DECIMAL(5, 2),
    HeartDiseasePrevalence DECIMAL(5, 2),
    AsthmaPrevalence DECIMAL(5, 2),
    HypertensionPrevalence DECIMAL(5, 2),
    ObesityPrevalence DECIMAL(5, 2),
    MentalHealthDisordersPrevalence DECIMAL(5, 2),
    PreventableHospitalizations DECIMAL(10, 2),  -- Rate per 100,000
    LifeExpectancy DECIMAL(5, 2),
    FOREIGN KEY (ZIPCode) REFERENCES ZIPCodes(ZIPCode)
);

-- Create table for healthcare access barriers
CREATE TABLE HealthcareAccessBarriers (
    BarrierID INT IDENTITY(1,1) PRIMARY KEY,
    ZIPCode VARCHAR(10),
    Year INT,
    PercentNoRegularCheckup DECIMAL(5, 2),
    PercentDelayedCare DECIMAL(5, 2),
    PercentNoTransportation DECIMAL(5, 2),
    AvgDistanceToHospital DECIMAL(5, 2),  -- In miles
    AvgDistanceToClinic DECIMAL(5, 2),    -- In miles
    PublicTransitAccessScore DECIMAL(5, 2),  -- Scale 0-100
    DigitalDivideIndex DECIMAL(5, 2),     -- Scale 0-100 measuring internet access, tech literacy
    FOREIGN KEY (ZIPCode) REFERENCES ZIPCodes(ZIPCode)
);

-- Create table for environmental health factors
CREATE TABLE EnvironmentalFactors (
    EnvironmentalID INT IDENTITY(1,1) PRIMARY KEY,
    ZIPCode VARCHAR(10),
    Year INT,
    AirPollutionIndex DECIMAL(5, 2),
    WaterQualityIndex DECIMAL(5, 2),
    FoodDesertScore DECIMAL(5, 2),  -- Higher means worse access to healthy food
    GreenSpaceAccess DECIMAL(5, 2), -- Percent of population with park access
    CalEnviroScreenScore DECIMAL(5, 2),
    FOREIGN KEY (ZIPCode) REFERENCES ZIPCodes(ZIPCode)
);

-- Create index for faster queries
CREATE INDEX idx_zipcode ON HealthIndicators(ZIPCode);
CREATE INDEX idx_zipcode_health_access ON HealthcareAccessBarriers(ZIPCode);
CREATE INDEX idx_zipcode_environmental ON EnvironmentalFactors(ZIPCode);
GO

-- Create a view that joins all relevant data for easier querying
CREATE VIEW CommunityHealthView AS
SELECT
    z.ZIPCode,
    z.CommunityName,
    z.TotalPopulation,
    z.MedianIncome,
    z.PercentMinority,
    z.PercentPoverty,
    z.PercentUninsured,
    z.SocialVulnerabilityIndex,
    hi.DiabetesPrevalence,
    hi.HeartDiseasePrevalence,
    hi.AsthmaPrevalence,
    hi.HypertensionPrevalence,
    hi.ObesityPrevalence,
    hi.MentalHealthDisordersPrevalence,
    hi.PreventableHospitalizations,
    hi.LifeExpectancy,
    hab.PercentNoRegularCheckup,
    hab.PercentDelayedCare,
    hab.PercentNoTransportation,
    hab.AvgDistanceToHospital,
    hab.AvgDistanceToClinic,
    hab.PublicTransitAccessScore,
    hab.DigitalDivideIndex,
    ef.AirPollutionIndex,
    ef.WaterQualityIndex,
    ef.FoodDesertScore,
    ef.GreenSpaceAccess,
    ef.CalEnviroScreenScore,
    (SELECT COUNT(*) FROM HealthcareFacilities hf WHERE hf.ZIPCode = z.ZIPCode) AS FacilityCount
FROM
    ZIPCodes z
LEFT JOIN
    HealthIndicators hi ON z.ZIPCode = hi.ZIPCode AND hi.Year = 2023
LEFT JOIN
    HealthcareAccessBarriers hab ON z.ZIPCode = hab.ZIPCode AND hab.Year = 2023
LEFT JOIN
    EnvironmentalFactors ef ON z.ZIPCode = ef.ZIPCode AND ef.Year = 2023;
GO