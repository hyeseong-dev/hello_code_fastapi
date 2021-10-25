from api.utils.db_util import database
from api.otps import schema

def find_otp_block(recipient_id:str):
    query = "Select * FROM py_otp_blocks WHERE recipient_id=:recipient_id and created_on >= now() at time zone 'UTC' - interval '5 minutes'" 
    return database.fetch_one(query, values={'recipient_id': recipient_id})