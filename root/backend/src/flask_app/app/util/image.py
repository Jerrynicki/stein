import io
import copy

from PIL import Image

import app.models as models

# represents the number of pixels at the longest
# axis that the image will be rendered down to
# images should not be rendered "upwards"
QUALITY_LEVELS = {
    0: 1920//2,
    1: 1920,
    2: 1920*2
}
IMG_TYPE = {
    "mime": "image/jpeg",
    "pil_format": "jpeg",
    "quality": 87
}
RESIZE_ALGO = Image.Resampling.BICUBIC

def to_post_pictures(image: bytes, post_id: int) -> list[models.post_picture.PostPicture]:
    result = list()
    
    img_pre_io = io.BytesIO(image)
    img_pre = Image.open(img_pre_io)
    
    width = img_pre.width
    height = img_pre.height
    size = (width, height)
    long_side = 0 if width > height else 1

    break_after = False # allows prematurely escaping in case
                        # not all quality levels are applicable
    for level in QUALITY_LEVELS:
        img = None

        if size[long_side] <= QUALITY_LEVELS[level]:
            # if the image is small enough, the largest quality
            # level should always be the original resolution
            # we break afterwards to avoid upscaling
            img = img_pre
            new_width = width
            new_height = height
            break_after = True
        else:
            if long_side == 0: # width is the long side
                new_width = QUALITY_LEVELS[level]
                new_height = int(QUALITY_LEVELS[level] * (height / width))
            else: # height is the long side
                new_width = int(QUALITY_LEVELS[level] * (width / height))
                new_height = QUALITY_LEVELS[level]

            img = img_pre.resize((new_width, new_height), resample=RESIZE_ALGO)

        assert img is not None # if this fails, there is a logic error somewhere

        img_io = io.BytesIO()
        img.save(img_io, format=IMG_TYPE["pil_format"], quality=IMG_TYPE["quality"])
        img.close()

        result.append(models.post_picture.PostPicture())
        result[-1].post_id = post_id
        result[-1].quality_level = level
        result[-1].width = new_width
        result[-1].height = new_height
        result[-1].mimetype = IMG_TYPE["mime"]
        result[-1].image = img_io.getvalue()

        img_io.close()

        if break_after:
            break

    img_pre.close()
    img_pre_io.close()

    return result

def to_profile_picture(image: bytes, user_name: str) -> models.profile_picture.ProfilePicture:
    """Crops the image to be a square and resizes it to 384x384"""

    SIZE = 384
    
    img_pre_io = io.BytesIO(image)
    img_pre = Image.open(img_pre_io)
    
    width = img_pre.width
    height = img_pre.height
    size = (width, height)

    box = (0, 0, 0, 0)

    if width > height:
        box = (
            (width-height)//2,
            0,
            width - (width-height)//2,
            height
        )
    else: 
        box = (
            0,
            (height-width)//2,
            width,
            height - (height-width)//2
        )

    img = img_pre.crop(box=box)
    img = img.resize((SIZE, SIZE), resample=RESIZE_ALGO)

    img_io = io.BytesIO()
    img.save(img_io, format=IMG_TYPE["pil_format"], quality=IMG_TYPE["quality"])
    
    result = models.profile_picture.ProfilePicture()
    result.user_name = user_name
    result.mimetype = IMG_TYPE["mime"]
    result.width = SIZE
    result.height = SIZE
    result.image = img_io.getvalue()
    
    img_pre.close()
    img.close()
    img_io.close()
    img_pre_io.close()

    return result