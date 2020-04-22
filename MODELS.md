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

### Instrument Comment Boxes
**Properties per box**
- User
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
**Properties**
- Name
  - The name of the platform
- Wmo id
  - The WMO ID for the mission. See: WMO Contact Info to acquire
- Serial number
  - Platform type
- Institution
  - The institution who owns the platform
- Purchase date
- Active
  - check if the platform is currently active

### Platform types	
**Properties**
- Model
- Manufacturer

### Platform power types	
**Properties**
- Model
- Manufacturer

### Platforms
**Properties**
- Name
  - The name of the platform
- Wmo id
  - The WMO ID for the mission. See: WMO Contact Info to acquire
- Serial number
  - Platform type
- Institution
  - The institution who owns the platform
- Purchase date
- Active
  - check if the platform is currently active

### Platform Comment Boxes
**Properties per box**
- User
- Event Time
- Comment

### Platform deployments	
**Properties**
- Wmo id
  - The WMO ID for the mission. See: WMO Contact Info to acquire
- Deployment number
- Platform
- Institution
  - The institution responsible for the deployment.
- Project
  - The project the data is being collected under.
- Power type
  - The battery type which was using in this deployment.
- Title
  - A short descriptive title for the deployment.
- Start time
- End time
- Deployment latitude
  - The latitude of the deployment
- Recovery latitude
  - The latitude of the recovery
- Deployment longitude
  - The longitude of the deployment
- Recovery longitude
  - The longitude of the recovery
- Deployment cruise
  - The cruise of the deployment
- Recovery cruise
  - The cruise of the recovery
- Deployment personnel
  - The personnel of the deployment
- Recovery personnel
  - The personnel of the recovery
- Testing mission
  - Whether this is a testing mission rather than a real deployment.
- Comment
  - The general comments for the deployment.
- Acknowledgement
  - Example: This deployment is supported by funding from NOAA
- Contributor name
  - A comma separated list of contributors to this data set
  - Example: "Jerry Garcia, Bob Weir, Bill Graham"
- Contributor role
  - A comma separated list of the roles for those specified in the contributor_name attribute
  - Example: "Principal Investigator, Principal Investigator, Data Manager"
- Creator email
  - The email of person collected data.
- Creator name
  - A comma separated of names of the person who collected the data.
- Creator url
  - A comma separated of URLs for the person who collected the data.
- Data repository link
  - URL for the repository from: Erddap.
- Publisher email
  - E-mail address of the publisher of the data.
- Publisher name
  - Name of the publisher of the data.
- Publisher url
  - A URL for the publisher of the data.
- Metadata link
  - This attribute provides a link to a complete metadata record for this data set or the collection that contains this data set.
- References
  - Published or web-based references that describe the data or methods used to produce it.
- Sea name
  - The sea in which the study is being conducted: Sea Names
- Depth
  - The depth of the deployment

### Platform Deployment Comment Boxes	
**Properties per box**
- User
- Event Time
- Comment

