# ------------------------------------------------------------------------------------
# Protocol.py
#
# This file defines the protocol details for a Sony Projector. It was updated from the original to
# include the capability to change the lens from 1.85 to 2.35 for true theatre viewing.
#
# The original details came from the document:
# https://www.digis.ru/upload/iblock/f5a/VPL-VW320,%20VW520_ProtocolManual.pdf
#
# The updated code came from the protocol document:
# https://www.digis.ru/upload/iblock/eac/VPL-VW1000ES,%20VW1100ES_ProtocolManual.pdf

ACTIONS = {
    "GET": 0x01,
    "SET": 0x00
}

COMMANDS = {
    "SET_POWER": 0x0130,
    "CALIBRATION_PRESET": 0x0002,
    "ASPECT_RATIO": 0x0020,
    "PICTURE_POSITION": 0x0066,
    "INPUT": 0x0001,
    "GET_STATUS_ERROR": 0x0101,
    "GET_STATUS_POWER": 0x0102,
    "GET_STATUS_LAMP_TIMER": 0x0113
}

INPUTS = {
    "HDMI1": 0x004,
    "HDMI2": 0x005
}

ASPECT_RATIOS = {
    "NORMAL": 0x0001,
    "V_STRETCH": 0x000B,
    "ZOOM_1_85": 0x000C,
    "ZOOM_2_35": 0x000D,
    "STRETCH": 0x000E,
    "SQUEEZE": 0x000F
}

PICTURE_POSITION = {
    "1.85.1": 0x0000,
    "2.35.1": 0x0001,
    "Custom1": 0x0002,
    "Custom2": 0x0003,
    "Custom3": 0x0004
}

POWER_STATUS = {
    "STANDBY": 0,
    "START_UP": 1,
    "START_UP_LAMP": 2,
    "POWER_ON": 3,
    "COOLING": 4,
    "COOLING2": 5
}
