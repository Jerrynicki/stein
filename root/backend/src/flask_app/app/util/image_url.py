import flask

import app.dbh.dbhelper as dbh
import app.models as models

STATIC_DB_PREFIX = "/dbstatic" # see main/dbserve.py
POST_IMAGES_PREFIX = "/images/post"
PROFILE_IMAGES_PREFIX = "/images/user"

def get_post_images(post_id: int) -> list[dict]:
    response = []

    images = dbh.get_multiple(models.post_picture.PostPicture, models.post_picture.PostPicture.post_id, post_id)

    for pi in images:
        response.append(
            {
                "quality_level": pi.quality_level,
                "width": pi.width,
                "height": pi.height,
                "url": STATIC_DB_PREFIX + POST_IMAGES_PREFIX + "/" + str(pi.id)
            }
        )

    return response

def get_profile_image_url(name: str):
    """Returns None if user doesn't have a profile picture, otherwise returns the
    link to it"""

    if dbh.get(models.profile_picture.ProfilePicture, models.profile_picture.ProfilePicture.user_name, name)\
        is not None:
        return STATIC_DB_PREFIX + PROFILE_IMAGES_PREFIX + "/" + name
    else:
        return None