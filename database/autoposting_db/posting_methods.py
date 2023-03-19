from .models_posting import autoposting_db, Posting, JobModel, Category, LinkSubReddit, Photo, UrlPost


# __________________________  Create  ______________________________
def db_write_url(url):
    UrlPost.create(url=url)

# ____________________________  UPDATE  _______________________________


def db_update_photo_is_work_1(post_obj: Posting):
    with autoposting_db:
        Photo.update(is_submitted=1).where(
            (Photo.is_submitted == 0) &
            (Photo.path_photo == post_obj.id_photo.path_photo)
        ).execute()

        LinkSubReddit.update(is_submitted=1).where(
            (LinkSubReddit.is_submitted == 0) &
            (LinkSubReddit.link_SubReddit == post_obj.id_link_sub_reddit.link_SubReddit)
        ).execute()


def db_reset_is_submit_post_0():
    with autoposting_db:
        LinkSubReddit.update(is_submitted=0).where(LinkSubReddit.is_submitted == 1).execute()
        Photo.update(is_submitted=0).where(Photo.is_submitted == 1).execute()


# _______________________________ get __________________________________
def db_get_gen_categories(jobmodel_obj: JobModel) -> list[Posting.id_category]:
    with autoposting_db:
        post_objs = list(
            Posting
            .select()
            .where(Posting.id_jobmodel == jobmodel_obj)
        )

        category_objs = [Category.get_by_id(post.id_category) for post in post_objs]

    return category_objs


def db_get_photos(jobmodel_obj: JobModel, category_obj: Category) -> list[Photo | None]:
    with autoposting_db:
        post_objs: list[Posting] = list(
            Posting.select()
            .join(LinkSubReddit)
            .join(Photo, on=(LinkSubReddit.id == Photo.id))
            .where(
                (Posting.id_jobmodel == jobmodel_obj.id) &
                (Posting.id_category == category_obj.id) &
                (Photo.is_submitted == False) &
                (LinkSubReddit.is_submitted == False)
            ))

        photos_objs = [Photo.get_by_id(post.id_photo) for post in post_objs]

    return photos_objs


# def db_generator_photos(jobmodel_obj: JobModel, category_obj: Category):
# 	while photos_objs := db_get_photos(jobmodel_obj, category_obj):

def db_pick_up_reddit_sub(jobmodel_obj: JobModel, category_obj: Category, photo_obj: Photo):
    with autoposting_db:
        post_objs: list[Posting] = (
            Posting.select()
            .join(LinkSubReddit)
            .join(Photo, on=(LinkSubReddit.id == Photo.id))
            .where(
                (Posting.id_jobmodel == jobmodel_obj) &
                (Posting.id_category == category_obj) &
                (Posting.id_photo == photo_obj) &
                (Photo.is_submitted == False) &
                (LinkSubReddit.is_submitted == False)
            )
        )

        link_sub_objs = [LinkSubReddit.get_by_id(post.id_link_sub_reddit) for post in post_objs]
    return link_sub_objs


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
                (Photo.is_submitted == False) &
                (LinkSubReddit.is_submitted == False)
            )
        )

    return list_post_obj


# ___________________________________________  DELETE  _________________________________________
def db_delete_check_if_not_exists_records(id_photo: Posting.id_photo, id_link_sub_reddit: Posting.id_link_sub_reddit):
    with autoposting_db:
        has_related_photo = Posting.select().join(Photo).where(Photo.id == id_photo).exists()
        has_related_link_sub = (
            Posting.select()
            .join(LinkSubReddit)
            .where(LinkSubReddit.id == id_link_sub_reddit)
            .exists()
        )

        if not has_related_photo:
            photo_obj = Photo.get_by_id(id_photo)
            photo_obj.delete_instance()

        if not has_related_link_sub:
            link_gub_obj = LinkSubReddit.get_by_id(id_link_sub_reddit)
            link_gub_obj.delete_instance()


def db_delete_executed_post(post_obj: Posting):
    id_photo = post_obj.id_photo
    id_link = post_obj.id_link_sub_reddit

    post_obj.delete_instance()

    return db_delete_check_if_not_exists_records(id_photo=id_photo, id_link_sub_reddit=id_link)

