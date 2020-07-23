from instagram_tools import insta_post


# login credentials
ig_username = "username"
ig_password = "password"

# path to image
image_filepath = "image.jpg"

# instagram caption
ig_caption = "There's an image above me."

# location of chromedriver https://chromedriver.chromium.org/downloads
path_to_chromedriver = "chromedriver.exe"


insta_post(ig_username, ig_password, image_filepath,
           ig_caption, path_to_chromedriver)
