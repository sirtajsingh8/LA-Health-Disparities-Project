-- Use our database
USE LAHealthDisparities;
GO

-- Clear existing data if any exists
DELETE FROM EnvironmentalFactors;
DELETE FROM HealthcareAccessBarriers;
DELETE FROM HealthIndicators;
DELETE FROM HealthcareFacilities;
DELETE FROM ZIPCodes;
GO

-- Insert data into ZIPCodes table
INSERT INTO ZIPCodes (ZIPCode, CommunityName, TotalPopulation, MedianIncome, PercentMinority, PercentPoverty, PercentUninsured, SocialVulnerabilityIndex)
VALUES 
('90001', 'Florence-Graham', 57110, 38056.00, 97.6, 29.8, 24.3, 8.7),
('90002', 'Watts', 51223, 35543.00, 96.8, 32.5, 26.7, 9.2),
('90003', 'South Central LA', 66266, 36954.00, 97.2, 31.3, 25.1, 8.9),
('90004', 'Koreatown', 62180, 47765.00, 85.3, 23.1, 21.4, 7.2),
('90005', 'Westlake', 43367, 46322.00, 88.7, 24.6, 22.3, 7.5),
('90006', 'Pico-Union', 59185, 35543.00, 94.6, 33.2, 27.8, 9.3),
('90007', 'University Park', 45021, 32765.00, 92.3, 37.4, 28.9, 9.5),
('90008', 'Baldwin Hills', 32327, 68534.00, 91.5, 14.3, 12.8, 5.3),
('90010', 'Hancock Park', 29345, 85654.00, 62.4, 10.2, 9.1, 4.1),
('90011', 'South Central LA', 68354, 32211.00, 97.8, 35.6, 29.8, 9.7),
('90012', 'Chinatown', 31254, 43567.00, 88.9, 27.5, 23.5, 7.8),
('90015', 'Downtown LA', 18765, 54321.00, 80.2, 22.1, 18.7, 6.5),
('90017', 'Downtown LA', 23456, 47890.00, 85.6, 25.8, 22.1, 7.3),
('90024', 'Westwood', 47452, 91345.00, 38.7, 19.3, 7.2, 3.2),
('90025', 'West LA', 43534, 95432.00, 42.3, 8.7, 6.8, 2.8),
('90026', 'Echo Park', 51345, 58765.00, 78.2, 19.4, 18.3, 6.1),
('90027', 'Los Feliz', 45367, 76543.00, 56.7, 12.6, 10.2, 4.3),
('90033', 'Boyle Heights', 54321, 34567.00, 96.5, 33.4, 28.7, 9.4),
('90045', 'Westchester', 43876, 87654.00, 48.2, 9.1, 7.3, 3.1),
('90046', 'Hollywood Hills', 34598, 112345.00, 32.1, 7.8, 5.4, 2.3),
('90048', 'Beverly Grove', 22345, 105678.00, 28.7, 8.5, 6.1, 2.7),
('90210', 'Beverly Hills', 21356, 193567.00, 22.3, 5.2, 3.1, 1.4),
('90211', 'Beverly Hills', 8976, 174532.00, 25.6, 5.8, 3.6, 1.6),
('90230', 'Culver City', 45678, 89765.00, 56.7, 9.8, 7.3, 3.4),
('90232', 'Culver City', 24354, 92345.00, 58.3, 9.2, 6.8, 3.1),
('90291', 'Venice', 43256, 105678.00, 42.3, 11.2, 8.7, 3.7),
('90292', 'Marina del Rey', 23456, 132456.00, 34.5, 7.3, 4.5, 2.1),
('90301', 'Inglewood', 54367, 47654.00, 94.5, 21.3, 19.8, 7.5),
('90302', 'Inglewood', 32456, 45678.00, 93.2, 22.5, 20.3, 7.8),
('90402', 'Santa Monica', 12345, 168973.00, 18.7, 4.5, 2.8, 1.3),
('90403', 'Santa Monica', 34567, 123456.00, 27.8, 8.3, 5.2, 2.5),
('90404', 'Santa Monica', 39875, 86754.00, 52.3, 14.6, 10.3, 4.7),
('90405', 'Santa Monica', 42367, 92345.00, 43.2, 12.5, 8.5, 3.8),
('90501', 'Torrance', 53456, 78965.00, 65.4, 11.8, 9.3, 4.1),
('90502', 'Torrance', 32456, 76543.00, 68.7, 12.5, 10.1, 4.4),
('90731', 'San Pedro', 45678, 68954.00, 73.2, 16.5, 13.8, 5.6),
('90732', 'San Pedro', 24354, 83456.00, 52.3, 10.2, 8.7, 3.6),
('90744', 'Wilmington', 56789, 48765.00, 89.7, 23.4, 21.2, 7.9),
('90745', 'Carson', 64532, 76543.00, 87.6, 13.2, 11.5, 5.2),
('91342', 'Sylmar', 87654, 61234.00, 84.5, 17.3, 15.6, 6.3),
('91344', 'Porter Ranch', 34567, 115678.00, 43.2, 5.6, 4.2, 2.1),
('91355', 'Valencia', 35678, 102345.00, 38.7, 6.3, 4.8, 2.3),
('91356', 'Tarzana', 27654, 108976.00, 35.6, 7.2, 5.3, 2.5),
('91364', 'Woodland Hills', 32456, 97654.00, 42.3, 8.5, 6.7, 3.1),
('91405', 'Van Nuys', 56789, 54321.00, 82.3, 19.7, 17.5, 6.8),
('91601', 'North Hollywood', 45678, 68543.00, 72.3, 17.8, 15.6, 6.1);
GO

-- Insert data into HealthIndicators table
INSERT INTO HealthIndicators (ZIPCode, Year, DiabetesPrevalence, HeartDiseasePrevalence, AsthmaPrevalence, HypertensionPrevalence, ObesityPrevalence, MentalHealthDisordersPrevalence, PreventableHospitalizations, LifeExpectancy)
VALUES
('90001', 2023, 18.5, 10.2, 15.6, 35.2, 32.1, 18.5, 350.0, 76.5),
('90002', 2023, 19.2, 11.4, 17.3, 36.4, 33.5, 19.7, 365.0, 75.8),
('90003', 2023, 17.8, 10.8, 16.5, 34.8, 31.2, 18.9, 340.0, 76.9),
('90004', 2023, 14.3, 8.7, 13.2, 28.6, 24.5, 16.3, 280.0, 79.5),
('90005', 2023, 15.1, 9.2, 13.8, 29.8, 25.7, 16.9, 295.0, 78.9),
('90006', 2023, 19.5, 11.6, 17.8, 36.7, 33.9, 20.1, 370.0, 75.5),
('90007', 2023, 20.3, 12.1, 18.5, 37.8, 35.2, 21.4, 385.0, 74.8),
('90008', 2023, 12.4, 7.5, 11.6, 25.3, 21.8, 14.5, 235.0, 82.2),
('90010', 2023, 9.8, 6.1, 9.5, 20.4, 17.3, 11.2, 190.0, 84.6),
('90011', 2023, 20.1, 12.5, 18.2, 38.5, 35.6, 22.3, 380.0, 74.3),
('90012', 2023, 16.7, 10.1, 15.3, 32.6, 28.2, 17.2, 325.0, 77.8),
('90015', 2023, 15.4, 9.3, 14.1, 30.2, 26.3, 16.4, 300.0, 78.5),
('90017', 2023, 16.2, 9.8, 14.9, 31.8, 27.5, 17.1, 315.0, 78.1),
('90024', 2023, 8.3, 5.2, 8.7, 18.5, 14.5, 9.8, 160.0, 86.4),
('90025', 2023, 8.7, 5.4, 8.9, 19.2, 15.1, 10.2, 165.0, 85.8),
('90026', 2023, 13.4, 8.2, 12.8, 27.5, 23.6, 15.4, 265.0, 80.2),
('90027', 2023, 10.5, 6.5, 10.1, 22.1, 18.7, 12.3, 210.0, 83.7),
('90033', 2023, 18.9, 11.3, 17.2, 36.1, 33.2, 19.8, 360.0, 75.9),
('90045', 2023, 9.3, 5.7, 9.2, 19.7, 16.2, 10.8, 175.0, 85.1),
('90046', 2023, 7.8, 4.9, 8.2, 17.5, 13.8, 9.2, 150.0, 87.2),
('90048', 2023, 8.1, 5.1, 8.5, 18.1, 14.2, 9.5, 155.0, 86.8),
('90210', 2023, 6.5, 4.2, 7.3, 15.3, 11.6, 7.8, 120.0, 89.5),
('90211', 2023, 6.8, 4.3, 7.5, 15.8, 12.1, 8.1, 125.0, 88.9),
('90230', 2023, 9.5, 5.8, 9.3, 20.1, 16.5, 11.0, 180.0, 84.8),
('90232', 2023, 9.2, 5.6, 9.0, 19.5, 16.0, 10.7, 175.0, 85.2),
('90291', 2023, 8.5, 5.3, 8.8, 18.9, 14.9, 10.0, 165.0, 86.0),
('90292', 2023, 7.2, 4.6, 7.8, 16.7, 12.8, 8.6, 135.0, 88.1),
('90301', 2023, 15.7, 9.6, 14.5, 31.2, 26.8, 17.5, 310.0, 78.1),
('90302', 2023, 16.2, 9.9, 14.9, 32.1, 27.6, 18.1, 320.0, 77.5),
('90402', 2023, 6.1, 4.0, 7.0, 14.8, 11.1, 7.4, 115.0, 90.2),
('90403', 2023, 7.5, 4.8, 8.0, 17.1, 13.4, 8.9, 145.0, 87.5),
('90404', 2023, 10.8, 6.7, 10.3, 22.7, 19.2, 12.6, 215.0, 83.2),
('90405', 2023, 9.8, 6.1, 9.7, 20.8, 17.5, 11.3, 195.0, 84.5),
('90501', 2023, 11.3, 7.0, 10.8, 23.6, 20.1, 13.2, 225.0, 82.5),
('90502', 2023, 11.8, 7.3, 11.2, 24.5, 20.8, 13.7, 235.0, 81.9),
('90731', 2023, 12.8, 7.9, 12.1, 26.3, 22.5, 14.9, 250.0, 80.8),
('90732', 2023, 10.2, 6.3, 9.9, 21.5, 18.3, 11.8, 205.0, 84.0),
('90744', 2023, 16.7, 10.2, 15.3, 32.8, 28.3, 18.6, 330.0, 77.0),
('90745', 2023, 12.3, 7.6, 11.7, 25.7, 22.0, 14.2, 245.0, 81.3),
('91342', 2023, 13.8, 8.5, 13.1, 28.2, 24.1, 15.8, 275.0, 79.8),
('91344', 2023, 7.9, 5.0, 8.3, 17.8, 14.0, 9.4, 155.0, 86.9),
('91355', 2023, 8.5, 5.3, 8.8, 18.9, 14.8, 9.9, 165.0, 86.0),
('91356', 2023, 8.2, 5.1, 8.5, 18.3, 14.3, 9.6, 160.0, 86.4),
('91364', 2023, 9.0, 5.5, 8.9, 19.3, 15.8, 10.5, 170.0, 85.5),
('91405', 2023, 14.5, 8.9, 13.6, 29.1, 25.2, 16.2, 285.0, 79.2),
('91601', 2023, 13.2, 8.1, 12.5, 27.1, 23.1, 15.1, 260.0, 80.5);
GO

-- Insert data into HealthcareAccessBarriers table
INSERT INTO HealthcareAccessBarriers (ZIPCode, Year, PercentNoRegularCheckup, PercentDelayedCare, PercentNoTransportation, AvgDistanceToHospital, AvgDistanceToClinic, PublicTransitAccessScore, DigitalDivideIndex)
VALUES
('90001', 2023, 35.6, 28.4, 22.3, 3.8, 1.9, 45.2, 68.7),
('90002', 2023, 38.1, 30.5, 24.8, 4.2, 2.1, 42.8, 72.3),
('90003', 2023, 36.3, 29.0, 23.1, 3.9, 2.0, 44.5, 69.8),
('90004', 2023, 27.5, 22.0, 17.6, 2.9, 1.5, 58.7, 53.2),
('90005', 2023, 28.9, 23.1, 18.5, 3.1, 1.6, 56.3, 55.8),
('90006', 2023, 38.7, 31.0, 25.2, 4.3, 2.2, 42.1, 73.2),
('90007', 2023, 40.2, 32.2, 26.5, 4.5, 2.3, 40.3, 75.6),
('90008', 2023, 22.1, 17.7, 14.1, 2.3, 1.2, 67.8, 42.3),
('90010', 2023, 17.2, 13.8, 11.0, 1.8, 0.9, 74.5, 32.7),
('90011', 2023, 41.5, 33.2, 27.3, 4.6, 2.4, 38.9, 77.8),
('90012', 2023, 30.5, 24.4, 19.5, 3.3, 1.7, 52.1, 58.7),
('90015', 2023, 28.3, 22.6, 18.1, 3.0, 1.5, 57.4, 54.5),
('90017', 2023, 29.7, 23.8, 19.0, 3.2, 1.6, 54.8, 56.9),
('90024', 2023, 14.5, 11.6, 9.3, 1.5, 0.8, 79.2, 27.5),
('90025', 2023, 15.3, 12.2, 9.8, 1.6, 0.8, 77.8, 29.0),
('90026', 2023, 25.6, 20.5, 16.4, 2.7, 1.4, 61.8, 49.5),
('90027', 2023, 18.9, 15.1, 12.1, 2.0, 1.0, 72.1, 36.2),
('90033', 2023, 37.2, 29.8, 24.2, 4.0, 2.0, 43.5, 71.2),
('90045', 2023, 16.4, 13.1, 10.5, 1.7, 0.9, 76.1, 31.0),
('90046', 2023, 13.5, 10.8, 8.6, 1.4, 0.7, 82.3, 25.6),
('90048', 2023, 14.1, 11.3, 9.0, 1.5, 0.8, 80.5, 26.8),
('90210', 2023, 11.2, 9.0, 7.2, 1.2, 0.6, 87.6, 21.2),
('90211', 2023, 11.8, 9.4, 7.5, 1.2, 0.6, 86.2, 22.3),
('90230', 2023, 16.7, 13.4, 10.7, 1.8, 0.9, 75.4, 31.8),
('90232', 2023, 16.2, 13.0, 10.4, 1.7, 0.9, 76.5, 30.7),
('90291', 2023, 14.9, 11.9, 9.5, 1.6, 0.8, 78.5, 28.3),
('90292', 2023, 12.6, 10.1, 8.1, 1.3, 0.7, 84.2, 24.0),
('90301', 2023, 30.1, 24.1, 19.3, 3.2, 1.7, 53.2, 58.5),
('90302', 2023, 31.0, 24.8, 19.8, 3.3, 1.7, 51.7, 60.1),
('90402', 2023, 10.6, 8.5, 6.8, 1.1, 0.6, 88.7, 20.1),
('90403', 2023, 13.0, 10.4, 8.3, 1.4, 0.7, 83.2, 24.6),
('90404', 2023, 19.5, 15.6, 12.5, 2.1, 1.1, 70.5, 37.5),
('90405', 2023, 17.2, 13.8, 11.0, 1.8, 0.9, 74.6, 32.6),
('90501', 2023, 20.3, 16.2, 13.0, 2.2, 1.1, 68.9, 39.1),
('90502', 2023, 21.2, 17.0, 13.6, 2.3, 1.2, 67.2, 41.0),
('90731', 2023, 23.4, 18.7, 15.0, 2.5, 1.3, 64.3, 45.2),
('90732', 2023, 18.3, 14.6, 11.7, 1.9, 1.0, 73.1, 34.8),
('90744', 2023, 32.1, 25.7, 20.5, 3.5, 1.8, 49.8, 62.3),
('90745', 2023, 22.6, 18.1, 14.5, 2.4, 1.2, 65.4, 43.5),
('91342', 2023, 26.4, 21.1, 16.9, 2.8, 1.5, 60.5, 51.2),
('91344', 2023, 13.8, 11.0, 8.8, 1.5, 0.7, 81.2, 26.1),
('91355', 2023, 14.9, 11.9, 9.5, 1.6, 0.8, 78.5, 28.2),
('91356', 2023, 14.3, 11.4, 9.1, 1.5, 0.8, 80.1, 27.0),
('91364', 2023, 15.8, 12.6, 10.1, 1.7, 0.9, 76.7, 30.0),
('91405', 2023, 27.1, 21.7, 17.4, 2.9, 1.5, 59.1, 52.3),
('91601', 2023, 25.2, 20.2, 16.1, 2.7, 1.4, 62.3, 48.5);
GO

-- Insert data into EnvironmentalFactors table
INSERT INTO EnvironmentalFactors (ZIPCode, Year, AirPollutionIndex, WaterQualityIndex, FoodDesertScore, GreenSpaceAccess, CalEnviroScreenScore)
VALUES
('90001', 2023, 78.5, 62.3, 85.6, 25.3, 87.2),
('90002', 2023, 80.2, 60.1, 88.4, 23.1, 89.5),
('90003', 2023, 79.1, 61.8, 86.3, 24.5, 87.9),
('90004', 2023, 68.7, 69.5, 72.8, 35.6, 75.3),
('90005', 2023, 70.2, 67.8, 74.5, 33.8, 77.2),
('90006', 2023, 81.0, 59.5, 89.1, 22.4, 90.3),
('90007', 2023, 82.5, 57.8, 91.3, 20.7, 92.1),
('90008', 2023, 61.3, 74.6, 63.2, 45.8, 65.8),
('90010', 2023, 55.1, 79.3, 54.7, 53.2, 57.5),
('90011', 2023, 83.2, 56.5, 92.5, 19.8, 93.5),
('90012', 2023, 71.8, 66.1, 76.8, 31.5, 78.9),
('90015', 2023, 69.5, 68.7, 73.8, 34.2, 76.5),
('90017', 2023, 70.8, 67.2, 75.2, 32.8, 77.8),
('90024', 2023, 51.3, 82.1, 49.5, 58.7, 53.2),
('90025', 2023, 52.5, 81.2, 51.0, 57.2, 54.8),
('90026', 2023, 65.7, 71.5, 68.9, 38.5, 71.5),
('90027', 2023, 57.2, 77.8, 57.5, 50.1, 59.8),
('90033', 2023, 79.8, 61.2, 87.5, 23.5, 88.7),
('90045', 2023, 53.8, 80.2, 52.6, 55.7, 56.3),
('90046', 2023, 49.7, 83.5, 47.2, 61.5, 51.5),
('90048', 2023, 50.5, 82.8, 48.2, 60.2, 52.5),
('90210', 2023, 45.2, 87.8, 41.3, 68.2, 46.8),
('90211', 2023, 46.5, 86.5, 43.1, 66.5, 48.3),
('90230', 2023, 54.3, 79.6, 53.2, 54.8, 57.0),
('90232', 2023, 53.5, 80.3, 52.1, 56.1, 55.8),
('90291', 2023, 50.8, 82.5, 48.7, 59.5, 52.5),
('90292', 2023, 47.3, 85.2, 44.5, 64.8, 49.2),
('90301', 2023, 72.5, 66.2, 76.8, 31.5, 79.5),
('90302', 2023, 73.8, 65.1, 78.3, 30.2, 80.8),
('90402', 2023, 43.5, 89.2, 39.2, 71.5, 44.8),
('90403', 2023, 48.5, 84.5, 45.8, 62.8, 50.3),
('90404', 2023, 58.3, 76.5, 59.0, 48.5, 61.2),
('90405', 2023, 55.1, 79.2, 54.5, 53.5, 57.5),
('90501', 2023, 59.8, 75.1, 61.2, 46.2, 63.5),
('90502', 2023, 61.5, 74.3, 63.5, 45.1, 66.0),
('90731', 2023, 63.8, 72.5, 66.5, 42.3, 68.7),
('90732', 2023, 56.5, 78.3, 56.2, 51.5, 58.7),
('90744', 2023, 75.2, 64.3, 80.1, 28.5, 82.3),
('90745', 2023, 62.5, 73.5, 64.8, 43.8, 67.2),
('91342', 2023, 67.2, 70.5, 70.5, 37.2, 73.1),
('91344', 2023, 50.1, 83.2, 47.8, 60.5, 52.1),
('91355', 2023, 50.8, 82.6, 48.5, 59.8, 52.3),
('91356', 2023, 50.5, 82.8, 48.2, 60.1, 52.0),
('91364', 2023, 52.1, 81.5, 50.5, 57.5, 54.3),
('91405', 2023, 66.8, 71.2, 69.8, 38.1, 72.4),
('91601', 2023, 64.5, 72.1, 67.5, 39.5, 70.1);
GO

-- Insert data into HealthcareFacilities table
-- Carefully ensuring all ZIPCodes used here exist in the ZIPCodes table
INSERT INTO HealthcareFacilities (FacilityName, FacilityType, ZIPCode, Address, HasEmergencyServices, AcceptsMediCal, AcceptsMedicare)
VALUES
('Cedars-Sinai Medical Center', 'Hospital', '90048', '8700 Beverly Blvd', 1, 1, 1),
('UCLA Medical Center', 'Hospital', '90024', '10833 Le Conte Ave', 1, 1, 1),
('Providence Saint John''s Health Center', 'Hospital', '90404', '2121 Santa Monica Blvd', 1, 1, 1),
('Kaiser Permanente Los Angeles', 'Hospital', '90027', '4867 Sunset Blvd', 1, 1, 1),
('Children''s Hospital Los Angeles', 'Hospital', '90027', '4650 Sunset Blvd', 1, 1, 1),
('USC Keck Hospital', 'Hospital', '90033', '1500 San Pablo St', 1, 1, 1),
('Good Samaritan Hospital', 'Hospital', '90017', '1225 Wilshire Blvd', 1, 0, 1),
('California Hospital Medical Center', 'Hospital', '90015', '1401 S Grand Ave', 1, 1, 1),
('Harbor-UCLA Medical Center', 'Hospital', '90502', '1000 W Carson St', 1, 1, 1),
('LAC+USC Medical Center', 'Hospital', '90033', '2051 Marengo St', 1, 1, 1),
('Venice Family Clinic', 'Clinic', '90291', '604 Rose Ave', 0, 1, 1),
('APLA Health Center', 'Clinic', '90005', '3741 S La Brea Ave', 0, 1, 1),
('Saban Community Clinic', 'Clinic', '90046', '8405 Beverly Blvd', 0, 1, 1),
('St. John''s Well Child & Family Center', 'Clinic', '90011', '808 W 58th St', 0, 1, 1),
('Westside Family Health Center', 'Clinic', '90405', '1711 Ocean Park Blvd', 0, 1, 1),
('Chinatown Service Center', 'Clinic', '90012', '767 N Hill St', 0, 1, 1),
('QueensCare Health Centers', 'Clinic', '90004', '4618 Fountain Ave', 0, 1, 1),
('Eisner Health', 'Clinic', '90015', '1245 W 7th St', 0, 1, 1),
('South Bay Family Healthcare', 'Clinic', '90501', '742 W Gardena Blvd', 0, 1, 1),
('Watts Healthcare Corporation', 'Clinic', '90002', '10300 Compton Ave', 0, 1, 1),
('Florence-Graham Community Health Center', 'Community Health Center', '90001', '1234 E Florence Ave', 0, 1, 1),
('Watts Community Health Center', 'Community Health Center', '90002', '2345 S Central Ave', 0, 1, 1),
('South LA Community Center', 'Community Health Center', '90003', '3456 S Vermont Ave', 0, 1, 1),
('Koreatown Community Health Center', 'Community Health Center', '90004', '4567 W Olympic Blvd', 0, 1, 1),
('Westlake Community Health Center', 'Community Health Center', '90005', '5678 Wilshire Blvd', 0, 1, 1),
('Pico-Union Health Center', 'Community Health Center', '90006', '6789 W Pico Blvd', 0, 1, 1),
('University Park Community Center', 'Community Health Center', '90007', '7890 S Figueroa St', 0, 1, 1),
('Baldwin Hills Health Center', 'Community Health Center', '90008', '8901 Crenshaw Blvd', 0, 1, 1),
('Hancock Park Medical Group', 'Clinic', '90010', '9012 W 3rd St', 0, 0, 1),
('South Central Health Clinic', 'Community Health Center', '90011', '1234 E Vernon Ave', 0, 1, 1),
('Westwood Medical Plaza', 'Clinic', '90024', '10921 Wilshire Blvd', 0, 0, 1),
('West LA Family Health', 'Clinic', '90025', '2317 Sawtelle Blvd', 0, 1, 1),
('Echo Park Community Clinic', 'Community Health Center', '90026', '1811 Sunset Blvd', 0, 1, 1),
('Los Feliz Primary Care', 'Clinic', '90027', '4323 Los Feliz Blvd', 0, 1, 1),
('Westchester Family Center', 'Community Health Center', '90045', '8540 Lincoln Blvd', 0, 1, 1),
('Hollywood Hills Medical Group', 'Clinic', '90046', '7317 Sunset Blvd', 0, 0, 1),
('Beverly Hills Medical Center', 'Clinic', '90210', '414 N Camden Dr', 0, 0, 1),
('Beverly Hills Community Clinic', 'Clinic', '90211', '8635 W 3rd St', 0, 0, 1),
('Culver City Family Health', 'Clinic', '90230', '3831 Hughes Ave', 0, 1, 1),
('Culver City Community Center', 'Community Health Center', '90232', '4343 Duquesne Ave', 0, 1, 1),
('Venice Beach Medical Group', 'Clinic', '90291', '1808 Lincoln Blvd', 0, 0, 1),
('Marina Medical Center', 'Clinic', '90292', '4560 Admiralty Way', 0, 0, 1),
('Inglewood Community Health Center', 'Community Health Center', '90301', '323 N Prairie Ave', 0, 1, 1),
('Inglewood Family Medicine', 'Clinic', '90302', '445 E Manchester Blvd', 0, 1, 1),
('Santa Monica Medical Center', 'Clinic', '90402', '1245 15th St', 0, 0, 1),
('Santa Monica Community Clinic', 'Community Health Center', '90403', '2509 Pico Blvd', 0, 1, 1),
('Ocean Park Health Center', 'Community Health Center', '90404', '2121 Cloverfield Blvd', 0, 1, 1),
('Santa Monica Family Health', 'Clinic', '90405', '2901 Ocean Park Blvd', 0, 1, 1),
('Torrance Memorial Medical Center', 'Hospital', '90501', '3330 Lomita Blvd', 1, 1, 1),
('Torrance Health Center', 'Community Health Center', '90502', '2201 W Carson St', 0, 1, 1),
('San Pedro Peninsula Hospital', 'Hospital', '90731', '1300 W 7th St', 1, 1, 1),
('San Pedro Community Clinic', 'Clinic', '90732', '731 S Beacon St', 0, 1, 1),
('Wilmington Community Health Center', 'Community Health Center', '90744', '1009 N Avalon Blvd', 0, 1, 1),
('Carson Family Health Center', 'Community Health Center', '90745', '21825 S Avalon Blvd', 0, 1, 1),
('Olive View-UCLA Medical Center', 'Hospital', '91342', '14445 Olive View Dr', 1, 1, 1),
('Providence Tarzana Medical Center', 'Hospital', '91356', '18321 Clark St', 1, 0, 1),
('Woodland Hills Kaiser', 'Hospital', '91364', '5601 De Soto Ave', 1, 0, 1),
('Valley Presbyterian Hospital', 'Hospital', '91405', '15107 Vanowen St', 1, 1, 1);
GO

-- Check if the view exists and drop it
IF EXISTS (SELECT * FROM sys.views WHERE name = 'CommunityHealthView')
BEGIN
    DROP VIEW CommunityHealthView;
END
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

-- Print confirmation message
PRINT 'Database population complete. Data is ready for analysis.';
GO