import sys


# TAP Viewer
print("tapview - ZX Spectrum TAP file viewer v0.1 - (c) 2020 Aki")
print("Usage: python tapview.py [TAP file]")
print()

# check if parameter has been provided
if len(sys.argv) == 1:
    print("TAP file required!")
    sys.exit()

# converts to lower case and saves shell argument into FILE var
FILE = sys.argv[1].lower()

# set global things
hex_numbers = ["0", "1", "2", "3", "4", "5", "6", "7",
               "8", "9", "a", "b", "c", "d", "e", "f"]
header = [[]]

# check cmd line stuff
if "-h" in FILE or "--help" in FILE:
    print("This program shows content of a ZX Spectrum TAP file.")
    sys.exit()

if ".tap" not in FILE:
    print("Please enter a valid TAP file (example: manicminer.tap)")
    sys.exit()


def open_file():
    with open(FILE, "rb") as file:
        content = file.read()
        print("TAP file:", FILE)
        print()
        return content

def search_for_headers(content):
    header_count = 0
    for byte in range(len(content)):
        if content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 0 \
            or content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 1 \
            or content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 2 \
            or content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 3:
            for i in range(byte, byte + 20):
                header[header_count].append(str(content[i]))
            # print("header=", header)
            header_count += 1
            header.append([])
    return True

def label():
    print("Nr Name       Type            Start Length  StHex  LenHex  Flag")
    print("=" * 63)

def parse_single_header(header):
    # something that has to be done (why?????????????? idk)
    header.pop(-1)

    for sub_header in header:
        # show header number
        header_idx = header.index(sub_header)
        if header_idx < 10:
            header_idx = "0" + str(header_idx)
        else:
            header_idx = str(header_idx)

        # convert strings (in header) to integers
        for i in range(len(sub_header)):
            sub_header[i] = int(sub_header[i])

        # parse header
        for index in range(len(sub_header)):
            # header flag
            if index == 2:
                if sub_header[index] == 0:
                    header_flag = 0
                if sub_header[index] == 255:
                    header_flag = 255

            # file name
            if index == 4:
                file_name = ""
                for character in range(4, 14):
                    file_name += chr(sub_header[character])

            # file type
            if index == 3:
                if sub_header[index] == 0:
                    type = "Program        "
                if sub_header[index] == 1:
                    type = "Number array   "
                if sub_header[index] == 2:
                    type = "Character array"
                if sub_header[index] == 3:
                    type = "Bytes          "

            # length of body
            if index == 14:
                highByte = hex(sub_header[index + 1])[2:]
                lowByte = hex(sub_header[index])[2:]
                if highByte in hex_numbers:
                    highByte = "0" + highByte
                if lowByte in hex_numbers:
                    lowByte = "0" + lowByte
                len_byteHex = int("0x" + highByte + lowByte, 16)
            
            # start address
            if index == 16:
                highByte = hex(sub_header[index + 1])[2:]
                lowByte = hex(sub_header[index])[2:]
                if highByte in hex_numbers:
                    highByte = "0" + highByte
                if lowByte in hex_numbers:
                    lowByte = "0" + lowByte
                start_byteHex = int("0x" + highByte + lowByte, 16)
                
            # body flag
            if index == 19:
                if sub_header[index] == 0:
                    body_flag = 0
                if sub_header[index] == 128:
                    body_flag = 128

        # if screen$
        if start_byteHex == 16384 and len_byteHex == 6912:
            type = "Screen$        "

        # print zx block line
        print(header_idx, file_name, type, "{0:{width}}".format(start_byteHex, width=5), " {0:{width}}".format(len_byteHex, width=5), " {0:{width}}".format(str(hex(start_byteHex)), width=6), "{0:{width}}".format(hex(len_byteHex), width=6), "  {0:{width}}".format(header_flag, width=3), end="")
        print()

if __name__ == '__main__':
    content = open_file()
    if search_for_headers(content) == True:
        label()
        parse_single_header(header)
    else:
        print("No header found.")
    print()
    print("Done.")
