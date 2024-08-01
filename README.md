# vidio (video io)

This generates the AXIStream frame for video subsystems to be used with cocotb.
This generates the AXIStream frame for video subsystems to be used with cocotb.

Functions:
- GenAXIStream: Generates an AXIS frame
- ConvertAXIStreamCS: Converts color space RGB to YUV [In development]

Roadmap:
- AXIS to matrix [Add 422, 420]
- Matrix to AXIS
- Generate color bars AXIS/matrix, supporting ITU-R BT.601-7, ITU-R BT.709-5
- Color convertion
- Chroma convertion
- Video to SMPTE-2110 packet

References:
- [Xilinx TPG](https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/v_tpg/v8_1/pg103-v-tpg.pdf)
- [cocotb](https://docs.cocotb.org/en/stable/)
- [cocotbext-axi](https://github.com/alexforencich/cocotbext-axi)

#
<!-- <https://docs.cocotb.org/en/stable/extensions.html -->

<!--
Build instructions

python3 -m build
pip install ./dist/cocotbext_vidio-x.y.z-py3-none-any.whl

Publish package at pypi.org using twine, need to enter API key
python3 -m twine upload  dist/*
-->