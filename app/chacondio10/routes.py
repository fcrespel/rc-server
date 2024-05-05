from fastapi import APIRouter, Body, Path, Request

from .protocol import transmit

router = APIRouter(prefix="/chacondio10", tags=["chacondio10"])

@router.get("/{sender}/{button}")
async def get_button(request: Request, sender: int = Path(ge=0, le=67108863), button: int = Path(ge=0, le=15)):
  if sender in request.app.state.chacondio10 and button in request.app.state.chacondio10[sender]:
    return request.app.state.chacondio10[sender][button]
  else:
    return 0

@router.put("/{sender}/{button}")
async def put_button(request: Request, sender: int = Path(ge=0, le=67108863), button: int = Path(ge=0, le=15), onoff: int = Body(ge=0, le=1), repeat: int = 5):
  if not sender in request.app.state.chacondio10:
    request.app.state.chacondio10[sender] = {}
  if onoff > 0:
    request.app.state.chacondio10[sender][button] = 1
    for i in range(repeat):
      transmit(request.app.state.gpio, sender, False, button, True)
  else:
    request.app.state.chacondio10[sender][button] = 0
    for i in range(repeat):
      transmit(request.app.state.gpio, sender, False, button, False)
