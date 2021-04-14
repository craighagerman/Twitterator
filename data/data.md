
# Data Directory

The `data` directory contains subdirectories for input and output data as follows 

### 01_screen_names  
- directory to hold files containing a list of Twitter screen names (handles)
- these are used by `userlist` streamkind
- n.b. these files are in TSV format and will be read by Pandas to extract the `Handle` column
- other (non-Handle) columns are human-readable context of who the handle belongs to

### 02_keyword_filter  
- directory to hold files containing a list of keywords to filter on
- these are used by `keyword` streamkind

### 03_stream_data
- directory to hold json files of data collected from a Twitter stream



