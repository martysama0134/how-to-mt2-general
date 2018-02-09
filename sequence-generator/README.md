# Intro
This python script automatically generates the sequence table for `EterLib\NetStream.cpp` (in `s_bSequenceTable`) and `game\src\sequence.cpp` (in `gc_abSequence`).

(the keys get changed every time you run the script)

A sequence table is just a simple random generated array with 16x2048 bytes between 0x0 and 0xfe.

Replacing the sequence table makes older/unwanted launchers unable to access the server.
