from typing import Generator

from loguru import logger

from database.autoposting_db.models_posting import JobModel, Photo, Category, Posting, LinkSubReddit
from database.autoposting_db import db_grab_model_obj, db_get_gen_categories, db_get_photos, db_pick_up_reddit_sub, \
    db_get_post_for_posting, db_update_photo_is_work_1, db_update_link_is_work_1


def get_name_model():
    jobmodels_objs: list[JobModel] = db_grab_model_obj()

    # while list exists from Posting.select()
    for jobmodels_obj in jobmodels_objs:
        logger.warning('Models')
        logger.info(jobmodels_obj.account.login)  # __________________ log account's login
        yield jobmodels_obj


def pick_up_link_sub_reddit(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo):
    link_sub_objs: list[LinkSubReddit] = db_pick_up_reddit_sub(jobmodel_obj, category_obj, photo_obj)

    # for link_sub_obj in link_sub_objs:
    while link_sub_objs:
        link_sub_obj = link_sub_objs.pop()

        logger.warning('Link Sub')
        logger.info(link_sub_obj.link_SubReddit)  # __________________ log link

        # if not link_sub_obj.is_submitted:
        list_post_obj: list[Posting] = db_get_post_for_posting(jobmodel_obj, category_obj, photo_obj, link_sub_obj)

        if list_post_obj:
            post_obj = list_post_obj[0]
            return post_obj, link_sub_obj

        link_sub_objs: list[LinkSubReddit] = db_pick_up_reddit_sub(jobmodel_obj, category_obj, photo_obj)

    return None, None


def pick_up_photos(jobmodel_obj: JobModel, category_obj: Category):
    photos_objs: list[Photo] = db_get_photos(jobmodel_obj, category_obj)

    # for photo_obj in photos_objs:
    while photos_objs:
        photo_obj = photos_objs.pop()
        logger.warning('Photo')
        logger.info(photo_obj.path_photo)  # __________________ log photo
        # if not photo_obj.is_submitted:
        post_obj: Posting
        post_obj, link_sub_obj = pick_up_link_sub_reddit(jobmodel_obj, category_obj, photo_obj)

        if post_obj:
            yield post_obj
            db_update_link_is_work_1(link_sub_obj)  # block link
            db_update_photo_is_work_1(photo_obj)  # block photo, reset on began program
        # else:
        #     return

        # photos_objs = db_get_photos(jobmodel_obj, category_obj)


def pick_up_category(jobmodel_obj: JobModel):
    category_objs: Generator[Category] = db_get_gen_categories(jobmodel_obj)

    for category_obj in category_objs:
        logger.warning('Category')
        logger.info(category_obj)  # __________________ log category

        yield from pick_up_photos(jobmodel_obj, category_obj)


def yield_up_data_from_db(jobmodel_obj: JobModel):
    for post_obj in pick_up_category(jobmodel_obj):
        logger.info(f'Block photo: {post_obj.id_photo.path_photo} and link: {post_obj.id_link_sub_reddit.link_SubReddit}')

        # send value
        logger.info("Start collecting data.")
        yield post_obj
        logger.info("Finish collecting data.")


