from skidl import SKIDL, TEMPLATE, Alias, Part, Pin, SchLib

SKIDL_lib_version = '0.0.1'

test3_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'GND', 'dest':TEMPLATE, 'tool':SKIDL, '_match_pin_regex':False, 'description':'Power symbol creates a global label with name "GND" , ground', 'datasheet':'', 'value_str':'GND', 'keywords':'power-flag', 'region':<skidl.arrange.Region object at 0x7faa5fa11090>, 'ref_prefix':'#PWR', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='GND',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'VCC', 'dest':TEMPLATE, 'tool':SKIDL, '_match_pin_regex':False, 'description':'Power symbol creates a global label with name "VCC"', 'datasheet':'', 'value_str':'VCC', 'keywords':'power-flag', 'region':<skidl.arrange.Region object at 0x7faa5fa11090>, 'ref_prefix':'#PWR', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='VCC',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'NCS2325D', 'dest':TEMPLATE, 'tool':SKIDL, '_match_pin_regex':False, 'symtx':'V', 'description':'Dual 36V, Precision, Rail-to-Rail Input/Output, Low Offset Voltage, Operational Amplifier, SOIC-8', 'datasheet':'http://www.ti.com/lit/ds/symlink/opa2197.pdf', 'value_str':'NCS2325D', '_aliases':Alias({'OPA2196xD', 'OPA2197xD', 'NCS20072D', 'OPA1692xD', 'MCP6L02x-xSN', 'AD8676xR', 'OPA2156xD'}), 'keywords':'dual opamp rtor', 'ref_prefix':'U', 'num_units':3, 'fplist':['SOIC*3.9x4.9mm*P1.27mm*'], 'do_erc':True, 'aliases':Alias({'OPA2196xD', 'OPA2197xD', 'NCS20072D', 'OPA1692xD', 'MCP6L02x-xSN', 'AD8676xR', 'OPA2156xD'}), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='~',func=Pin.types.OUTPUT,do_erc=True),
            Pin(num='2',name='-',func=Pin.types.INPUT,do_erc=True),
            Pin(num='3',name='+',func=Pin.types.INPUT,do_erc=True),
            Pin(num='5',name='+',func=Pin.types.INPUT,do_erc=True),
            Pin(num='6',name='-',func=Pin.types.INPUT,do_erc=True),
            Pin(num='7',name='~',func=Pin.types.OUTPUT,do_erc=True),
            Pin(num='4',name='V-',func=Pin.types.PWRIN,do_erc=True),
            Pin(num='8',name='V+',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'R_US', 'dest':TEMPLATE, 'tool':SKIDL, '_match_pin_regex':False, 'symtx':'L', 'description':'Resistor, US symbol', 'datasheet':'~', 'tx_ops':'L', 'value_str':'4K7', 'keywords':'R res resistor', 'region':<skidl.arrange.Region object at 0x7faa5fa11b10>, 'ref_prefix':'R', 'num_units':1, 'fplist':['R_*'], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])
