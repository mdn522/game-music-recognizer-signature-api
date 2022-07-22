from shazamio import Shazam
from shazamio.signature import DecodedMessage
from shazamio.utils import get_song
import pathlib
from typing import Union


# Shazam
async def get_signature(data: Union[str, pathlib.Path, bytes, bytearray]) -> DecodedMessage:
    song = await get_song(data=data)
    audio = Shazam.normalize_audio_data(song)
    signature_generator = Shazam.create_signature_generator(audio)
    signature = signature_generator.get_next_signature()
    while not signature:
        signature = signature_generator.get_next_signature()

    return signature
