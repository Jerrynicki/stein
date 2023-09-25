STATIC_PREFIX = "/static"
POST_IMAGES_PREFIX = "/images/post"

def get_post_image_url(id: int):
    return STATIC_PREFIX + POST_IMAGES_PREFIX + "/" + str(id)