from fastapi import APIRouter, HTTPException, status
from api.otps import schema, crud
from api.enums import otp
from api.utils import otp_util
import uuid

router = APIRouter(prefix='/api/v1')

@router.post('/otp/send')
async def send_otp(
    type: otp.OTPType,
    request: schema.CreateOTP
):

    # Check block OTP
    otp_blocks = await crud.find_otp_block(request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Sorry, Blokcked In 5 Minues')

    # Generate and save to table py_otps
    otp_code = otp_util.random(6)
    session_id = str(uuid.uuid1())
    await crud.save_otp()

    return 'SENT OTP'

    
@router.post('/otp/verify')
async def verify_otp():
    return 'Sending OTP to '

