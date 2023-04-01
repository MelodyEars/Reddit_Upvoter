import datetime

from .models_posting import autoposting_db, Posting, JobModel, Category, LinkSubReddit, Photo, UrlPost


# __________________________  Create  ______________________________
def db_add_url_to_upvoter(post_obj, url):
    with autoposting_db:
        url_obj = UrlPost.create(url=url)
        Posting.update(id_url=url_obj).where(Posting.id == post_obj.id).execute()


# ____________________________  UPDATE  _______________________________
def db_update_photo_is_work_1(photo_obj: Photo):
    with autoposting_db:
        Photo.update(is_submitted=True).where(Photo.id == photo_obj.id).execute()


def db_update_link_is_work_1(link_obj: LinkSubReddit):
    with autoposting_db:
        LinkSubReddit.update(is_submitted=True).where(LinkSubReddit.id == link_obj.id).execute()


def db_SUBLINK_reset_is_submitted(link_id: LinkSubReddit.id):
    with autoposting_db:
        LinkSubReddit.update(is_submitted=False).where(LinkSubReddit.id == link_id).execute()


def db_PHOTO_reset_is_submitted(photo_id: Photo.id):
    with autoposting_db:
        Photo.update(is_submitted=False).where(Photo.id == photo_id).execute()


def db_add_date_post(post_id: Posting.id):
    with autoposting_db:
        Posting.update(date_posted=datetime.datetime.now()).where(Posting.id == post_id).execute()


# _______________________________ get __________________________________
def db_get_exist_post_for_model(jobmodel_obj: JobModel):
    with autoposting_db:
        posts_objs: list[Posting] = Posting.select().where(
            (Posting.id_url.is_null(True)) &
            (Posting.id_jobmodel == jobmodel_obj.id)
        )
        return posts_objs


def db_get_list_post_obj_sort_by_date(jobmodel_obj: JobModel):
    with autoposting_db:
        post_objs = list(
            Posting
            .select()
            .where(
                (Posting.id_jobmodel == jobmodel_obj) &
                (Posting.id_url.is_null(False))
            )
            .order_by(Posting.date_posted.desc())
        )

    # sort older -> younger
    return post_objs


def db_get_gen_categories(jobmodel_obj: JobModel):
    with autoposting_db:
        post_objs = list(
            Posting
            .select()
            .where(
                (Posting.id_jobmodel == jobmodel_obj) &
                (Posting.id_url.is_null(True))
            )
        )
        # category_objs = [Category.get_by_id(post.id_category) for post in post_objs]
        category_ids = [post.id_category for post in post_objs]
        unique_category_ids = set(category_ids)
        unique_category = [Category.get_by_id(id_category) for id_category in unique_category_ids]

    return unique_category


def db_get_photos(jobmodel_obj: JobModel, category_obj: Category) -> list[Photo | None]:
    with autoposting_db:
        post_objs: list[Posting] = list(
            Posting.select()
            # .join(LinkSubReddit)
            # .join(Photo, on=(LinkSubReddit.id == Photo.id))
            .where(
                (Posting.id_jobmodel == jobmodel_obj.id) &
                (Posting.id_category == category_obj.id) &
                (Posting.id_url.is_null(True))
                # (Photo.is_submitted != True) &
                # (LinkSubReddit.is_submitted != True)
            )
            # .distinct(Posting.id_photo)
        )

        # photos_objs = [Photo.get_by_id(post.id_photo) for post in post_objs]
        photo_ids = [post.id_photo for post in post_objs if post.id_link_sub_reddit.is_submitted == False and post.id_photo.is_submitted == False]
        unique_photo_ids = set(photo_ids)
        unique_photos = [Photo.get_by_id(photo_id) for photo_id in unique_photo_ids]
    return unique_photos


def db_pick_up_reddit_sub(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo) -> list[LinkSubReddit]:
    with autoposting_db:
        post_objs: list[Posting] = (
            Posting.select()
            # .join(LinkSubReddit)
            # .join(Photo, on=(LinkSubReddit.id == Photo.id))
            .where(
                (Posting.id_jobmodel == jobmodel_obj) &
                (Posting.id_category == category_obj) &
                (Posting.id_photo == photo_obj) &
                (Posting.id_url.is_null(True))
                # (Photo.is_submitted != True) &
                # (LinkSubReddit.is_submitted != True)
            )
            # .distinct(Posting.id_link_sub_reddit)
        )

        link_sub_ids = [post.id_link_sub_reddit for post in post_objs if post.id_link_sub_reddit.is_submitted == False and post.id_photo.is_submitted == False]
        unique_link_sub_ids = set(link_sub_ids)
        unique_link_sub = [LinkSubReddit.get_by_id(link_sub_id) for link_sub_id in unique_link_sub_ids]

    return unique_link_sub


def db_get_post_for_posting(
        jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo, link_sub_obj: LinkSubReddit
) -> list[Posting]:
    with autoposting_db:
        list_post_obj: list[Posting] = list(
            Posting.select()
            .join(LinkSubReddit)
            .join(Photo, on=(LinkSubReddit.id == Photo.id))
            .where(
                (Posting.id_jobmodel == jobmodel_obj) &
                (Posting.id_category == category_obj) &
                (Posting.id_photo == photo_obj) &
                (Posting.id_link_sub_reddit == link_sub_obj) &
                (Posting.id_url.is_null(True)) &
                (Photo.is_submitted != True) &
                (LinkSubReddit.is_submitted != True)
            )
        )

    return list_post_obj


# ___________________________________________  DELETE  _________________________________________
# def db_delete_check_if_not_exists_records(id_photo: Posting.id_photo, id_link_sub_reddit: Posting.id_link_sub_reddit):
#     with autoposting_db:
#         has_related_photo = Posting.select().join(Photo).where(Photo.id == id_photo).exists()
#         has_related_link_sub = (
#             Posting.select()
#             .join(LinkSubReddit)
#             .where(LinkSubReddit.id == id_link_sub_reddit)
#             .exists()
#         )
#
#         if not has_related_photo:
#             photo_obj = Photo.get_by_id(id_photo)
#             photo_obj.delete_instance()
#
#         if not has_related_link_sub:
#             link_gub_obj = LinkSubReddit.get_by_id(id_link_sub_reddit)
#             link_gub_obj.delete_instance()


def db_delete_executed_post(selected_post_obj: Posting):
    # id_photo = post_obj.id_photo
    # id_link = post_obj.id_link_sub_reddit
    posts_objs = Posting.select().where(Posting.id_photo == selected_post_obj.id_photo)

    for post_obj in posts_objs:
        post_obj.delete_instance()

    #
    # return db_delete_check_if_not_exists_records(id_photo=id_photo, id_link_sub_reddit=id_link)


def db_del_post_banned_sub(link_sub_reddit: str):
    with autoposting_db.atomic():
        link_obj: LinkSubReddit = list(LinkSubReddit.select().where(LinkSubReddit.link_SubReddit == link_sub_reddit))[0]
        post_objs: list[Posting] = Posting.select().where(Posting.id_link_sub_reddit == link_obj)
        for post_obj in post_objs:
            post_obj.delete_instance()

        link_obj.delete_instance()
