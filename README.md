# vidio (video io)

This was built to generate simulation model similar to AMD-Xilinx Test Pattern Generator IP but can be used with cocotb

Implemented
- Generates an AXI stream of one RGB video frame with specfied resolution, pixel-width and pattern. 

Roadmap:
- AXIS to matrix
- Matrix to AXIS
- Generate color bars AXIS/matrix, supporting ITU-R BT.601-7, ITU-R BT.709-5
- Color convertion
- Chroma convertion
- Video to SMPTE-2110 packet

References:
- [Xilinx TPG](https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/v_tpg/v8_1/pg103-v-tpg.pdf)
- [cocotb](https://docs.cocotb.org/en/stable/)
- [cocotbext-axi](https://github.com/alexforencich/cocotbext-axi)
- [vlc python bindings](https://wiki.videolan.org/python_bindings)

#
<!-- <https://docs.cocotb.org/en/stable/extensions.html -->
