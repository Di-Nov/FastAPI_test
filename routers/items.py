from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def read_root():
    return [
        {
            'id': 1,
            'name': 'first'
        }
    ]

@router.get('/{item_id}')
def read_iteam(item_id: int):
    return {'item_id': item_id, 'name': 'first'}
