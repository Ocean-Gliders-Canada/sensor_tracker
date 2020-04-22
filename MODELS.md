# Sensor Tracker Models

## General

### Institutions
**Properties**
- Name
- Name of the institution
- Url
  - The institution's URL
- Street
- City
- Province
- Postal code
- Country
- Contact name
- Contact phone
- Contact email

### Manufacturers
**Properties**
- Name
- Street
- City
- Province
- Postal code
- Country
- Contact name
- Contact phone
- Contact email

### Projects
**Properties**
- Name

## Instruments

### Instrument Comment Boxes
**Properties per box**
- Event Time
- Comment


### Instrument on Platform History
**Properties**
- Instrument
  - The instrument that was put on a platform
- Platform
  - The platform that the instrument was put on
- Start time
  - The date the instrument was put on the platform
- End time
  - The date the instrument was removed from the platform
- Comment

### Instruments	
**Properties**
- Identifier
  - The name used to identify this instrument in the raw data. IE: SATCTD7229, sci_water
- Short name
  - The short, general name for the instrument. IE: ctd, fluorometer
- Long name
  - The full name for the instrument
- Manufacturer
- Serial
- Master instrument
- Comment
  - This is a good place to document anything unusual about this instrument's configuration

### Sensor on Instrument History
**Properties**
- Instrument
  - The instrument that was put on a platform
- Sensor
  - The platform that the instrument was put on
- Start time
  - The date the instrument was put on the platform
- End time
  - The date the instrument was removed from the platform
- Comment

### Sensors	
**Properties**
- Identifier
  - The name used to identify this sensor in the raw data. ie: sci_water_temp
- Long name
  - REQUIRED if 'Include in output' is checked. The general name for the sensor. IE: temperature
- Standard name
  - The official, standard name for the instrument. IE: sea_water_temperature. See CF naming: CF Naming Reference
- Serial
  - The Instrument which this sensor currently attach on. Modified this field will auto change sensor on instrument table.
- Type
  - Storage datatype to use for this sensor.The default is correct for most sensors
- Units
  - The units for the sensor. Please verify after adding a new sensor
- Precision
  - The precision of a sensor is the consistency for repeated measurements. Average deviation about the mean
- Accuracy
  - The accuracy of a sensor is the closeness to true values. Average distance from a known, true value
- Resolution
  - The resolution of a sensor is the smallest change it can detect in the quantity that it is measuring.
- Valid min
  - The minimum possible value that the sensor could produce
- Valid max
  - The maximum possible value that the sensor could produce
- Include in output
  - Whether or not data from this sensor should be included in any processed output. NOTE: Long name mast be populated if this is checked
- Display in web interface
  - Whether of not data from this seneor should be showed in the web interface.
- Comment
  - This is a good place to document anything unusual about this particular sensor. IE: wavelengths for spectral sensors

## Platforms

### Platform Comment Boxes
**Properties per box**

### Platform Deployment Comment Boxes	

### Platform deployments	
**Properties**

### Platform power types	
**Properties**

### Platform types	
**Properties**

### Platforms
**Properties**

