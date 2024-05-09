from fastapi import APIRouter, Body, Path, Query, Request

from .protocol import transmit

__all__ = ["router"]

router = APIRouter(prefix="/chacon54662", tags=["chacon54662"])


@router.get("/state/{stateKey}", summary="Get button state")
async def get_state(request: Request, stateKey: str = Path(pattern="[a-z0-9-]")):
    """Get the current state for a given stateKey"""
    if stateKey in request.app.state.chacon54662:
        return request.app.state.chacon54662[stateKey]
    else:
        return 0


@router.put("/word", summary="Send 24-bit code word")
async def put_word(request: Request, word: str = Body(pattern="[01]{24}"), repeat: int = 3,
                   stateKey: str = Query(default=None, pattern="[a-z0-9-]"), stateValue: int = Query(default=None, ge=0, le=1)):
    """Send a 24-bit code word and optionally save state in a given stateKey"""
    if stateKey is not None and stateValue is not None:
        request.app.state.chacon54662[stateKey] = stateValue
    for _ in range(repeat):
        transmit(request.app.state.gpio, int(word, 2))
