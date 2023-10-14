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
    
    img_pre = Image.open(io.BytesIO(image))
    
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

        print(new_width, new_height, width, height, img.size, level, QUALITY_LEVELS[level])

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

    return result

def to_profile_picture(image: bytes) -> models.profile_picture.ProfilePicture:
    # TODO
    
    with Image.open("hopper.jpg") as im:

        # The crop method from the Image module takes four coordinates as input.
        # The right can also be represented as (left+width)
        # and lower can be represented as (upper+height).
        (left, upper, right, lower) = (20, 20, 100, 100)

        # Here the image "im" is cropped and assigned to new variable im_crop
        im_crop = im.crop((left, upper, right, lower))