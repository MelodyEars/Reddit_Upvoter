from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required
from NW_Upvoter.db_tortories_orm.models import WorkAccountWithLink


# ___________________________________________  create  _________________________________________________________
@db_connection_required
async def db_exist_record_link_account(link_obj, cookie_obj) -> (bool, WorkAccountWithLink):
    # check if id band with id link
    obj, created = await WorkAccountWithLink.get_or_create(cookie=cookie_obj, link=link_obj)

    return created, obj


# ___________________________________________  delete  _________________________________________________________
@db_connection_required
async def db_delete_record_work_account_with_link(obj_record: WorkAccountWithLink):
    """obj if needed to delete when exception exists"""
    if obj_record is not None:
        await obj_record.delete()
    else:
        print("obj_record is not an instance of WorkAccountWithLink")
