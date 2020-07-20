from mountain_project_tools import mountain_project_api


mountain_project_api(  
    # location lat long nn.nn - distance(miles) 1-200
    latitude="34.05",
    longitude="-118.24",
    distance="200",
    # difficulty 5.x to 5.x - abcd suffix
    min_difficulty="5.6",
    max_difficulty="5.10",
    # results total
    results="500",
    # api key
    api_key="200184563-600b5620d2aeef5b58b889e459f5ce5b")
