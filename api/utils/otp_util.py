from api.utils.db_util import database
from api.otps import schema

def find_block_otp(recipient_id: str):
    query = "SELECT * FROM py_otp_blocks WHERE recipient_id=:recipient_id AND created_on >=now() at time zone 'UTC' - interval '5 minutes'"
    return database.fetch_one(query, values={'recipient_id': recipient_id})

def save_otp(
    request: schema.CreateOTP,
    session_id: str,
    otp_code: str,
):
    query = "INSERT INTO py_otps VALUES(:id,\
                                        :recipient_id,\
                                        :session_id,\
                                        :otp_code,\
                                        :status,\
                                        :created_on,\
                                        :updated_on,\
                                        :otp_failed_count")
    return database.execute(query, values={})