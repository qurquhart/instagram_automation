from instagram_tools import mountain_project_poster


# credentials
ig_username = "username"
ig_password = "password"

# string conataining all hashtags
hashtags = "#climbing #rockclimbing #climb #bouldering #climber #trad #sportclimbing #climbers " \
           "#climbon #climbingwall #climbingphotography #climbingday #climbingtraining "\
           "#climbingismypassion #climberlife #climbingnation #climbinggear #climbhard "\
           "#climbingworldwide #indoorbouldering #chalkbag " \
           "#rockclimbinggear #chalkbags #boulderingtraining #boulderingislife"


mountain_project_poster(ig_username, ig_password, hashtags, 'chromedriver.exe')