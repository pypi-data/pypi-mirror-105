"""NeoPixel write for Pico u2if."""

from .pico_u2if import pico_u2if


def neopixel_write(gpio, buf):
    """NeoPixel Writing Function"""

    # pad output buffer from 3 bpp to 4 bpp
    buffer = []
    for i in range(0, len(buf), 3):
        buffer.append(0)
        buffer.append(buf[i + 2])
        buffer.append(buf[i + 1])
        buffer.append(buf[i])

    pico_u2if.neopixel_write(gpio, buffer)
