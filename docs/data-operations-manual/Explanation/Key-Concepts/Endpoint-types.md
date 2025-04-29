# Endpoint URL Types and Plugins

The pipeline can collect data published in a wide range of different formats, which means there is a lot of variety in the types of URLs we might add as endpoints. Broadly, however, endpoints typically fall into one of the following two categories:
- Hosted file - these will usually be URL which ends in something like `.json` or `.csv`
- Standards compliant web server - these will usually be identifiable by parts of the URL like `MapServer` or `FeatureServer`, or sections that look like query parameters, like `?service=WFS&version=1.0.0`

## Data formats of resources that can be processed**
- Geojson (preferred for geospatial data because this mandates Coordinate Reference System WGS84)
- CSV text files containing WKT format geometry
- PDF-A 
- Shapefiles
- Excel files containing WKT format geometry (xls, xlsx, xlsm, xlsb, odf, ods, odt)
- Mapinfo
- Zip files containing Mapinfo or Shapefiles 
- GML
- Geopackage
- OGC Web Feature Service
- ESRI ArcGIS REST service output in GeoJSON format

**Hosted files**
These can typically be added as they are with no problems. The pipeline can read most common formats and will transform them into the csv format it needs if they’re not already supplied as csv.

**Web servers**
Web server endpoints usually provide some flexibility around the format that data is returned in. The data provider may have shared a correctly configured URL which returns valid data, or they may have just provided a link to the server service directory, which does not itself contain data we can process.

E.g. this URL from Canterbury provides information on a number of different planning-related layers available from their ArcGIS server:
`https://mapping.canterbury.gov.uk/arcgis/rest/services/External/Planning_Constraints_New/MapServer`

Depending on the endpoint, it may be necessary to either **edit the URL** to return valid data, or **use a plugin** to make sure the data is processed correctly. A plugin is typically needed for an API endpoint if the collector needs to paginate (e.g. the ArcGIS API typically limits to 1,000 records per fetch) or strip unnecessary content from the response (e.g. WFS feeds can sometimes contain access timestamps which can result in a new resource being created each day the collector runs).

>[!NOTE]  
> Wherever possible, we prefer to collect from a URL which returns data in an open standard such as geojson or WFS, instead of the ArcGIS service directory page.