from skidl import *

fpga = Part(lib="FPGA_Lattice.lib", name="ICE40HX8K-BG121")
fpga.uA.symtx = "R"
generate_svg(file_="test7")
