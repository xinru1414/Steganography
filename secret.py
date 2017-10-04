"""
Steganography
A python program that hides information (text messages) in png files
Based on DrapsTV's "Steganography Tutorial - Hiding Text inside an Image" https://www.youtube.com/watch?v=q3eOOMx5qoo

Loads an image and look at each pixel's hex value
If the pixel's blue channel falls in the 0-5 range then 1 bit of info is stored
Ends the stream with a delimiter of fifteen 1's and one 0.
"""

from PIL import Image
import binascii
import optparse


def rgb2hex(r, g, b):
    """
    Turn rgb color values to hex color values
    :param r (int): red chanel value
    :param g (int): green chanel value
    :param b (int): blue chanel value
    :return (string): a hex value
    """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex2rgb(hexcode):
    """
    Turn hex color values to rgb color values
    :param hexcode (string): hex value
    :return (tuple): r, g, b value
    """
    assert isinstance(hexcode, str)
    assert len(hexcode) == 7
    r = int(hexcode[1:3], 16)
    g = int(hexcode[3:5], 16)
    b = int(hexcode[5:7], 16)

    return r, g, b

def str2bin(message):
    """
    Turn a message into binary omit first two digits
    :param message: This should be a str encoded in utf-8
    :return: binary string
    """
    message_bytes = bytes(message, "utf-8")
    binary = bin(int(binascii.hexlify(message_bytes), 16))
    return binary[2:]


def bin2str(binary):
    """
    Turn a binary into string
    :param binary:
    :return:
    """
    message_bytes = binascii.unhexlify('%x' % (int(binary, 2)))
    return str(message_bytes, encoding="utf-8")


def encodeblue(hexcode, digit):
    """

    :param hexcode:
    :param digit:
    :return:
    """
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

def encodegreen(hexcode, digit):
    """

    :param hexcode:
    :param digit:
    :return:
    """
    if hexcode[-3] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-3] + digit + hexcode[5:]
        return hexcode
    else:
        return None


def decodeblue(hexcode):
    """

    :param hexcode:
    :return:
    """
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None


def decodegreen(hexcode):
    """

    :param hexcode:
    :return:
    """
    if hexcode[-3] in ('0', '1'):
        return hexcode[-3]
    else:
        return None

def hide(filename, message):
    """
    Hide the message in the png image
    :param filename (png): the png file that's been used as the medium
    :param message (string): the secret message you are trying to hide
    :return:
    """
    img = Image.open(filename)
    binary = str2bin(message) + '1111111111111110'
    if img.mode in 'RGBA':
        img = img.convert('RGBA')
        pixels = img.getdata()

        new_pixels = []
        digit = 0
        count = 0
        for item in pixels:

            if digit < len(binary) and count % 2 == 0:
                new_pix = encodeblue(rgb2hex(item[0], item[1], item[2]), binary[digit])
                if new_pix is None:
                    new_pixels.append(item)
                else:
                    r, g, b = hex2rgb(new_pix)
                    new_pixels.append((r, g, b, 255))
                    digit += 1
            elif digit < len(binary) and count % 2 != 0:
                new_pix = encodegreen(rgb2hex(item[0], item[1], item[2]), binary[digit])
                if new_pix is None:
                    new_pixels.append(item)
                else:
                    r, g, b = hex2rgb(new_pix)
                    new_pixels.append((r, g, b, 255))
                    digit += 1
            else:
                new_pixels.append(item)
            count += 1
        img.putdata(tuple(new_pixels))
        img.save(filename, 'PNG')
        return "Completed!"
    return "Incorrect Image mode detect, couldn't hide message"


def retr(filename):
    """
    retrieve the message from the png image
    :param filename: the png file that contains the secret message
    :return: the secret message
    """
    img = Image.open(filename)
    binary = ''
    count = 0

    if img.mode in 'RGBA':
        img = img.convert('RGBA')
        pixels = img.getdata()
        for item in pixels:
            if count % 2 == 0:
                digit = decodeblue(rgb2hex(item[0], item[1], item[2]))
            else:
                digit = decodegreen(rgb2hex(item[0], item[1], item[2]))
            count += 1
            if digit is None:
                pass
            else:
                binary = binary + digit
                if binary[-16:] == '1111111111111110':
                    print("success")
                    return bin2str(binary[:-16])
        return bin2str(binary)
    return "Incorrect Image mode detect, couldn't retrieve message"


def main():
    """
    parameter handling
    """
    parser = optparse.OptionParser('usage %png '
                                   '-e/-d <target file>')
    parser.add_option('-e', dest='hide', type='string',
                      help='target picture parse to hide text')

    parser.add_option('-d', dest='retr', type='string',
                      help='target picture parse to retrieve text')
    (options, args) = parser.parse_args()
    if options.hide is not None:
        text = input("Enter a message to hide: ")
        print(hide(options.hide, text))
    elif options.retr is not None:
        print(retr(options.retr))
    else:
        print(parser.usage)
        exit(0)


if __name__ == "__main__":
    main()
