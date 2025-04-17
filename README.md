# tile service for INFORMATION SYSTEM BAIKAL
The tile service is a set of scripts executed in a specific order. The purpose of the service is to work with .tif files. The main task of the service is automatic processing and slicing.tif files uploaded to the server for tiles
## Stack
- [Python](https://www.python.org/)
## Scripts
- sliceAllFilesScript.py - script designed to slice all files into tiles in a specific directory in some other directory. it is necessary for slicing files that originally exist on the server.
- slicingScript.py - script designed to slice a specific file into tiles
- tile_service.py - a script designed to track changes in certain directories and when a file .tif appears slice it using slicingScript.py into the appropriate directory

