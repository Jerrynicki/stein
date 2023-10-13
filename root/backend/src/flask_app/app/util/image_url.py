STATIC_PREFIX = "/static"
POST_IMAGES_PREFIX = "/images/post"
PROFILE_IMAGES_PREFIX = "/images/user"

def get_post_image_url(id: int):
    return STATIC_PREFIX + POST_IMAGES_PREFIX + "/" + str(id)

def get_profile_image_url(name: str):
    return STATIC_PREFIX + PROFILE_IMAGES_PREFIX + "/" + name