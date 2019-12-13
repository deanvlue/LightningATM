#!/usr/bin/python3

import zbarlight
import logging
import time

from PIL import Image
from io import BytesIO
from picamera import PiCamera


def scan():

    with PiCamera() as camera:
        try:
            camera.start_preview()
            time.sleep(1)
            logging.info("Start scanning for QR code")
        except:
            logging.error("PiCamera.start_preview() raised an exception")

        stream = BytesIO()
        qr_codes = None
        # Set timeout to 10 seconds
        timeout = time.time() + 10

        while qr_codes is None and (time.time() < timeout):
            stream.seek(0)
            # Start camera stream (make sure RaspberryPi camera is focused correctly
            # manually adjust it, if not)
            camera.capture(stream, "jpeg")
            stream.seek(0)
            qr_codes = zbarlight.scan_codes("qrcode", Image.open(stream))
            time.sleep(0.05)
        camera.stop_preview()

        # break immediately if we didn't get a qr code scan
        if not qr_codes:
            logging.info("No QR within 10 seconds detected")
            return False

        # decode the first qr_code to get the data
        qr_code = qr_codes[0].decode()

        return qr_code
