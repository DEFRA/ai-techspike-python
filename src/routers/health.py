from fastapi import APIRouter

router = APIRouter(
    prefix='/health',
    tags=['health']
)

@router.get("/", response_description="Check the health of the API")
async def get_health():
    return {"message": "success"}