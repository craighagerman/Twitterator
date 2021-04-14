# Config Directory

The config directory contains YAML files used to run Twitter streaming collector

The YAML file is expected to contain the following members:


    streamkind: <userlist, filter, random, geo, myfriends>
    appname: name_of_Twitter_app
    langs: [<two-letter-language-list>]
    file_prefix: <string prefix for output data>
    data_dir: <name of `data` subdirectory containing filter list>
    filter_file: <name of file in above directory to use for filter list>
    
