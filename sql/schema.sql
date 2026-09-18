-- 1. Dimension Tables
CREATE TABLE Dim_Location (
  location_key INT IDENTITY(1,1) PRIMARY KEY,
  city NVARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Dim_Condition (
  condition_key INT IDENTITY(1,1) PRIMARY KEY,
  conditions NVARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Dim_Date (
  date_key INT PRIMARY KEY,
  full_date DATE NOT NULL,
  [year] SMALLINT NOT NULL,
  [month] TINYINT NOT NULL,
  [day] TINYINT NOT NULL,
  day_of_week NVARCHAR(15) NOT NULL,
  [quarter] TINYINT NOT NULL
);

-- 2. Fact Table
CREATE TABLE Fact_Weather_Daily (
  weather_fact_id BIGINT IDENTITY(1,1) PRIMARY KEY,
  date_key INT NOT NULL FOREIGN KEY REFERENCES Dim_Date(date_key),
  location_key INT NOT NULL FOREIGN KEY REFERENCES Dim_Location(location_key),
  condition_key INT NOT NULL FOREIGN KEY REFERENCES Dim_Condition(condition_key),
  tempmax DECIMAL(5,2) NULL,
  tempmin DECIMAL(5,2) NULL,
  temp DECIMAL(5,2) NULL,
  feelslike DECIMAL(5,2) NULL,
  humidity DECIMAL(5,2) NULL,
  precip DECIMAL(8,2) NULL,
  precipprob DECIMAL(5,2) NULL,
  windspeed DECIMAL(6,2) NULL,
  windgust DECIMAL(6,2) NULL,
  cloudcover DECIMAL(5,2) NULL,
  sunrise TIME NULL,
  sunset TIME NULL,
  created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT UQ_Fact_Weather_Date_Location UNIQUE (date_key, location_key)
);

-- 3. Performance Indexes
CREATE INDEX IX_Fact_Weather_Date ON Fact_Weather_Daily(date_key);
CREATE INDEX IX_Fact_Weather_Location ON Fact_Weather_Daily(location_key);