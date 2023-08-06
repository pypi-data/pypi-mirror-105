#Python rest api for geo and covid information

##Includes 2 modules:
    1 geo_lib 
    2 news_lib

#geo_lib contains:
    1 administration.py
    2 city.py
    3 country.py
    4 time.py
#news_lib contains:
    1 covid.py
    2 help.py

#administration.py
    Provides class with 2 methods for api:
        1 get_currencies
        2 get_language
    which sends GET request to get currency type of given country and 
    language of given country

#city.py
    Provides class with 2 methods for api:
        1 get_cities
        2 get_city_details
    which sends GET request to get cities number and details for given params

#TODO finish rest
    

