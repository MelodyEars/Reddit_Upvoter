import time

from loguru import logger

from database.autoposting_db.models_posting import JobModel, Photo, Category, Posting, LinkSubReddit
from database.autoposting_db import db_grab_model_obj, db_get_gen_categories, db_get_photos, db_pick_up_reddit_sub, \
    db_get_post_for_posting, db_update_photo_is_work_1, db_update_link_is_work_1, db_get_exist_post_for_model


# def get_name_model():
#     jobmodels_objs: list[JobModel] = db_grab_model_obj()
#
#     # while list exists from Posting.select()
#     for jobmodels_obj in jobmodels_objs:
#         logger.warning('Models')
#         logger.info(jobmodels_obj.account.login)  # __________________ log account's login
#         yield jobmodels_obj


def pick_up_category(jobmodel_obj: JobModel):
    category_objs: list[Category] = db_get_gen_categories(jobmodel_obj)
    print(category_objs)
    while category_objs:
        category_obj = category_objs.pop()
        logger.warning('Category')
        logger.info(category_obj.name_category)  # __________________ log category

        photos_objs: list[Photo] = db_get_photos(jobmodel_obj, category_obj)
        print(photos_objs)
        while photos_objs:
            photo_obj = photos_objs.pop()
            logger.warning('Photo')
            logger.info(photo_obj.id)  # __________________ log photo

            link_sub_objs: list[LinkSubReddit] = db_pick_up_reddit_sub(jobmodel_obj, category_obj, photo_obj)
            # if link_sub_objs:
            print(link_sub_objs)
            while link_sub_objs:
                link_sub_obj = link_sub_objs.pop()
                # link_sub_obj = link_sub_objs.pop()
                logger.warning(f'Link Sub {link_sub_obj.id}')  # __________________ log link

                list_post_obj: list[Posting] = db_get_post_for_posting(jobmodel_obj, category_obj, photo_obj, link_sub_obj)

                if list_post_obj:
                    post_obj = list_post_obj[0]
                    yield post_obj, link_sub_obj, photo_obj
                    break

    return None, None, None


def yield_up_data_from_db(jobmodel_obj: JobModel):
    for post_obj, link_sub_obj, photo_obj in pick_up_category(jobmodel_obj):
        if post_obj:
            logger.info(f'Block photo: {post_obj.id_photo.path_photo} and link: {post_obj.id_link_sub_reddit.link_SubReddit}')

            # send value
            logger.info("Start collecting data.")
            yield post_obj
            logger.info("Finish collecting data.")
            db_update_link_is_work_1(link_sub_obj)  # block link
            db_update_photo_is_work_1(photo_obj)  # block photo, reset on began program
            # logger.info("Wait 10 minutes")
            # time.sleep(10 * 60 * 60)


def if_enough_post(jobmodel_obj: JobModel):
    posts_objs = db_get_exist_post_for_model(jobmodel_obj)
    if posts_objs:
        return
    else:
        name = jobmodel_obj.model_name
        while True:
            logger.critical(f"Додай фото в {name}")
            time.sleep(15)