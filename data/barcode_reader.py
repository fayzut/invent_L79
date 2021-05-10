from urllib.parse import unquote

from pyzbar import pyzbar
import cv2


def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        print("detected barcode:", obj)
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        data = unquote(str(obj.data[:-1]))
        print("Data:", data)
        # print("Data:", obj.data)
        print()

    return image, data


def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width,
                           decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0),
                          thickness=5)
    return image


def decode_file(link):
    barcodes = glob(link)
    for barcode_file in barcodes:
        # load the image to opencv
        print(barcode_file)
        img = cv2.imread(barcode_file)
        # decode detected barcodes & get the image
        # that is drawn
        img, data = decode(img)
        # show the image
        # cv2.imshow("img", img)
        # cv2.imwrite("barcode_detected.png", img)
        # cv2.waitKey(0)
        if data:
            return data


if __name__ == "__main__":
    from glob import glob

    print(decode_file("../static/images/barcode_%D0%A4A00001.png"))
