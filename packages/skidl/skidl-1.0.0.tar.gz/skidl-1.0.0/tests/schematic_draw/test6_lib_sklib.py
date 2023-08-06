from skidl import SKIDL, TEMPLATE, Alias, Part, Pin, SchLib

SKIDL_lib_version = "0.0.1"

test6_lib = SchLib(tool=SKIDL).add_parts(
    *[
        Part(
            **{
                "name": "GND",
                "dest": TEMPLATE,
                "tool": SKIDL,
                "datasheet": "",
                "description": 'Power symbol creates a global label with name "GND" , ground',
                "value_str": "GND",
                "_match_pin_regex": False,
                "keywords": "power-flag",
                "ref_prefix": "#PWR",
                "num_units": 1,
                "fplist": [],
                "do_erc": True,
                "aliases": Alias(),
                "pin": None,
                "footprint": None,
                "pins": [Pin(num="1", name="GND", func=Pin.types.PWRIN, do_erc=True)],
            }
        ),
        Part(
            **{
                "name": "VCC",
                "dest": TEMPLATE,
                "tool": SKIDL,
                "datasheet": "",
                "description": 'Power symbol creates a global label with name "VCC"',
                "value_str": "VCC",
                "_match_pin_regex": False,
                "keywords": "power-flag",
                "ref_prefix": "#PWR",
                "num_units": 1,
                "fplist": [],
                "do_erc": True,
                "aliases": Alias(),
                "pin": None,
                "footprint": None,
                "pins": [Pin(num="1", name="VCC", func=Pin.types.PWRIN, do_erc=True)],
            }
        ),
        Part(
            **{
                "name": "R",
                "dest": TEMPLATE,
                "tool": SKIDL,
                "datasheet": "~",
                "description": "Resistor",
                "value_str": "R",
                "_match_pin_regex": False,
                "keywords": "R res resistor",
                "ref_prefix": "R",
                "num_units": 1,
                "fplist": ["R_*"],
                "do_erc": True,
                "aliases": Alias(),
                "pin": None,
                "footprint": None,
                "pins": [
                    Pin(num="1", name="~", func=Pin.types.PASSIVE, do_erc=True),
                    Pin(num="2", name="~", func=Pin.types.PASSIVE, do_erc=True),
                ],
            }
        ),
    ]
)
