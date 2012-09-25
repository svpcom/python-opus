# -*- coding: utf-8 -*-

import ctypes

from opus.api import constants, libopus
from opus.exceptions import OpusError


c_int_pointer = ctypes.POINTER(ctypes.c_int)


class Encoder(ctypes.Structure):
    """Opus encoder state.

    This contains the complete state of an Opus encoder.
    """

    pass

EncoderPointer = ctypes.POINTER(Encoder)


_get_size = libopus.opus_encoder_get_size
_get_size.argtypes = (ctypes.c_int,)
_get_size.restype = ctypes.c_int


def get_size(channels):
    """Gets the size of an OpusEncoder structure."""

    if not channels in (1, 2):
        raise ValueError('Wrong channels value. Must be equal to 1 or 2')

    return _get_size(channels)


_create = libopus.opus_encoder_create
_create.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, c_int_pointer)
_create.restype = EncoderPointer


def create(fs, channels, application):
    """Allocates and initializes an encoder state."""

    result_code = ctypes.c_int()

    result = _create(fs, channels, application, ctypes.byref(result_code))
    if result_code.value is not constants.OK:
        raise OpusError(result_code.value)

    return result


_ctl = libopus.opus_encoder_ctl
_ctl.restype = ctypes.c_int


def ctl(encoder, request, value=None):
    if value:
        return request(_ctl, encoder, value)

    return request(_ctl, encoder)

destroy = libopus.opus_encoder_destroy
destroy.argtypes = (EncoderPointer,)
destroy.restype = None
destroy.__doc__ = "Frees an OpusEncoder allocated by opus_encoder_create()"