from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

tx_test_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'Q_PNP_CBE', 'dest':TEMPLATE, 'tool':SKIDL, 'keywords':'transistor PNP', 'value_str':'Q_PNP_CBE', 'description':'PNP transistor, collector/base/emitter', 'symtx':'', 'datasheet':'~', 'tool_version':'kicad', '_match_pin_regex':False, 'ref_prefix':'Q', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='C',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='B',func=Pin.types.INPUT,do_erc=True),
            Pin(num='3',name='E',func=Pin.types.PASSIVE,do_erc=True)] })])