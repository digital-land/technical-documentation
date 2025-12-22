---
title: Endpoint URL Types and Plugins
---

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

## Adding query parameters to ArcGIS server URLs
This is often necessary when LPAs only provide a link to the service directory page, rather than the data itself. To get a URL we can process you may need to:

1. **Identify the correct layer**. If there isn’t a layer name already clear in the URL you may need to check which feature layers there are on the server by getting to the services directory. This is usually a URL which ends with MapServer or FeatureServer

    E.g. `https://mapping.canterbury.gov.uk/arcgis/rest/services/External/Planning_Constraints_New/MapServer` or `https://maps.birmingham.gov.uk/server/rest/services/planx/PlanX/FeatureServer`

    These pages should list the name of each layer and a number in brackets, e.g. “Article 4 Direction (3)”

2. **Add the layer number and query parameters to the URL.**
Append to the URL the number of the feature layer you need, plus minimal query parameters which will return all of the data available. 

    E.g `URL` + `/3/` (layer number) + `query?where=1%3D1&outfields=*&f=geojson` (query parameters)

    Like `https://mapping.canterbury.gov.uk/arcgis/rest/services/External/Planning_Constraints_New/MapServer/3/query?where=1%3D1&outfields=*&f=geojson `

    See the [ArcGIS docs](https://developers.arcgis.com/documentation/portal-and-data-services/data-services/feature-services/query-features/) for more info on queries, but in short after `query?` there are three parameters used to return all of the data, separated by &:

    - `where=1%3D1` - This is just ASCII url encoded version of “where=1=1” which makes use of the query SQL parameters to say return all data (where 1=1 is always ignored by SQL engines)
    - `outfields=*` - return all fields of the dataset
    - `f=geojson` - return in geojson format. Depending on the server configuration this can sometimes be tweaked if necessary to give a different file format
 
