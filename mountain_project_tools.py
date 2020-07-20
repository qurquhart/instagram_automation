def mountain_project_api(latitude, longitude, distance, min_difficulty, max_difficulty, results, api_key):
    '''pull data from the mountain project api'''
    return f"https://www.mountainproject.com/data/get-routes-for-lat-lon?lat={latitude}"\
           f"&lon={longitude}&maxDistance={distance}&minDiff={minimum_difficulty}"\
           f"&maxDiff={maximum_difficulty}&maxResults={results}&key={api_key}"
