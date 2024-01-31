from fastapi import APIRouter


router = APIRouter()


@router.get("/health-check")
async def api_health_check():
    """ Health check endpoint """

    return {'status': 'ok'}

