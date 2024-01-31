from fastapi import APIRouter
# from api.logic import get_answer


VERSION = 'v1'
router = APIRouter()


@router.post("/answer")
async def api_answer(answer: str, service_):
    """ Answer endpoint """

    return {'status': 'ok'}
