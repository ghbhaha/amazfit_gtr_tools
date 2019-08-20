import os


class Header:
    dialSignature = b"HMDIAL\0"

    headerSize = 40
    unknownPos = 32
    parametersSizePos = 36

    def __init__(self, unknown, parametersSize):
        self.signature = Header.dialSignature
        self.unknown = unknown
        self.parametersSize = parametersSize


    def isValid(self):
        return self.signature == Header.dialSignature


    def writeTo(self, stream):
        path = os.path.dirname(stream.name)
        headerPath = os.path.join(path, "header.bin")
        with open(headerPath, 'rb') as readStream:
            headerBuffer = readStream.read(64)
            headerBuffer = bytearray(headerBuffer)
            t = self.parametersSize.to_bytes(4, byteorder='little')
            headerBuffer[56:56 + len(t)] = t
            stream.write(headerBuffer)

    @staticmethod
    def readFrom(stream):
        sig_buffer = stream.read(16)

        bipMode = sig_buffer[0x0b] == 0xff
        if bipMode:
            Header.headerSize = 40 - 16
            Header.unknownPos = 32 - 16
            Header.parametersSizePos = 36 - 16
        else:
            Header.headerSize = 64 - 16
            Header.unknownPos = 52 - 16
            Header.parametersSizePos = 56 - 16

        buffer = stream.read(Header.headerSize)

        path = os.path.dirname(stream.name)
        name, _ = os.path.splitext(os.path.basename(stream.name))
        unpackedPath = os.path.join(path, name)
        headerPath = os.path.join(unpackedPath, "header.bin")
        with open(headerPath, 'wb') as fileStream:
            fileStream.write(sig_buffer)
            fileStream.write(buffer)
            fileStream.flush()

        header = Header(
            unknown = int.from_bytes(buffer[Header.unknownPos:Header.unknownPos+4], byteorder='little'),
            parametersSize = int.from_bytes(buffer[Header.parametersSizePos:Header.parametersSizePos+4], byteorder='little'))
        header.signature = sig_buffer[0:7]
        return header