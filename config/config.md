# Config Directory

The config directory contains YAML files used to run Twitter streaming collector

The YAML file is expected to contain the following members:


    streamkind: <userlist, filter, random, geo, myfriends>
    appname: name_of_Twitter_app
    langs: [<two-letter-language-list>]
    file_prefix: <string prefix for output data>
    data_dir: <name of `data` subdirectory containing filter list>
    filter_file: <name of file in above directory to use for filter list>
    
### Examples:

A YAML file for collecting random tweets from the firehose stream

    streamkind: random
    appname: <your-app-name>
    langs: ['en']
    file_prefix: random

A YAML file for collecting tweets using a keyword filter
n.b. this example assumes that file `data/02_keyword_filter/covid_keywords.txt` exists
and contains a newline-separated list of keywords to use for filtering

    streamkind: keyword
    appname: <your-app-name>
    langs: ['en']
    file_prefix: covid19
    data_dir: 02_keyword_filter
    filter_file: covid_keywords.txt


A YAML file for collecting tweets from a list of specified users
n.b. this example assumes that file `data/01_screen_names/canadian_execs.tsv` exists
This TSV file will be read by Pandas and is assumed to contain a `id` column 
specifying the Twitter id for a given individual. Note - Twitter requires filtering by user
id and NOT by handle. Given a file containing handles only you can use `process_user_files.py`
to get the Twitter profile information (including ids) for each handle

    streamkind: userlist
    appname: <your-app-name>
    langs: ['en']
    file_prefix: random
    data_dir: 01_screen_names
    filter_file: canadian_execs.tsv





