from dbr import *
import cv2
import pyexcel
import pandas as pd
import csv
from more_itertools import unique_everseen

def text_results_callback_func(frame_id, t_results, user_data):
        print(frame_id)

        for result in t_results:
            text_result = TextResult(result)
            print("Barcode Format : ")
            barcode_format = text_result.barcode_format_string
            print(barcode_format)
            print("Barcode Text : ")
            barcode_text = text_result.barcode_text
            print(barcode_text)
            print("Localization Points : ")
            localization_point = text_result.localization_result.localization_points
            print(localization_point)
            print("Exception : ")
            print(text_result.exception)
            print("-------------")

            dict_1 = [{"Barcode Format" : barcode_format,
                     "Barcode Text" : barcode_text,
                     "Localization points" : localization_point }]


#            with open('data_qr.csv','w') as f:
#                writer = csv.DictWriter(f, fieldnames=dict_1)
#                writer.writeheader()
#                f.write("\n")
            dict_1_df = pd.DataFrame.from_dict(dict_1)
            with open('data_qr.csv', 'a') as f:
                f.write('\n')
            dict_1_df.to_csv('data_qr.csv' ,sep='\t', index = False, mode ='a')
            with open('data_qr.csv', 'r') as f, open('data_qr_without_dupes.csv', 'w') as out_file:
                out_file.writelines(unique_everseen(f))

#            if dict_1["Barcode Text"] != barcode_text:
#                print("test")
#                dict_2 = [{"Barcode Format" : barcode_format,
#                     "Barcode Text" : barcode_text,
#                     "Localization points" : localization_point }]
#                dict_2_df = pd.DataFrame.from_dict(dict_2)
#                dict_1_df.append(dict_2_df)


 #           dict_1_df.to_csv('qr_data.csv' ,sep='\t', index = False)

from dbr import *
import cv2
import pyexcel
import pandas as pd
import csv
from more_itertools import unique_everseen

def text_results_callback_func(frame_id, t_results, user_data):
        print(frame_id)

        for result in t_results:
            text_result = TextResult(result)
            print("Barcode Format : ")
            barcode_format = text_result.barcode_format_string
            print(barcode_format)
            print("Barcode Text : ")
            barcode_text = text_result.barcode_text
            print(barcode_text)
            print("Localization Points : ")
            localization_point = text_result.localization_result.localization_points
            print(localization_point)
            print("Exception : ")
            print(text_result.exception)
            print("-------------")

            dict_1 = [{"Barcode Format" : barcode_format,
                     "Barcode Text" : barcode_text,
                     "Localization points" : localization_point }]

#            with open('data_qr.csv','w') as f:
#                writer = csv.DictWriter(f, fieldnames=dict_1)
#                writer.writeheader()
#                f.write("\n")
            dict_1_df = pd.DataFrame.from_dict(dict_1)
            with open('data_qr.csv', 'a') as f:
                f.write('\n')
            dict_1_df.to_csv('data_qr.csv' ,sep='\t', index = False, mode ='a')
            with open('data_qr.csv', 'r') as f, open('data_qr_without_dupes.csv', 'w') as out_file:
                out_file.writelines(unique_everseen(f))

#            if dict_1["Barcode Text"] != barcode_text:
#                print("test")
#                dict_2 = [{"Barcode Format" : barcode_format,
#                     "Barcode Text" : barcode_text,
#                     "Localization points" : localization_point }]
#                dict_2_df = pd.DataFrame.from_dict(dict_2)
#                dict_1_df.append(dict_2_df)


 #           dict_1_df.to_csv('qr_data.csv' ,sep='\t', index = False)


def intermediate_results_callback_func(frame_id, i_results, user_data):
        print(frame_id)
        for result in i_results:
            intermediate_result = IntermediateResult(result)
            print('Intermediate Result data type : {0}'.format(intermediate_result.result_type))
            print('Intermediate Result data : {0}'.format(intermediate_result.results))
            print("-------------")

def error_callback_func(frame_id, error_code, user_data):
        print(frame_id)
        error_msg = user_data.get_error_string(error_code)
        print('Error : {0} ; {1}'.format(error_code, error_msg))

def decode_video():
    video_width = 0
    video_height = 0

    # a. Decode video from camera
    vc = cv2.VideoCapture(1)

    # # b. Decode video file
    # video_file = "Put your video file path here."
    # vc = cv2.VideoCapture(video_file)

    video_width  = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vc.set(3, video_width) #set width
    vc.set(4, video_height) #set height

    stride = 0
    if vc.isOpened():
        rval, frame = vc.read()
        stride = frame.strides[0]
    else:
        return

    windowName = "Video Barcode Reader"


    reader = BarcodeReader()

    parameters = reader.init_frame_decoding_parameters()
    parameters.max_queue_length = 30
    parameters.max_result_queue_length = 30
    parameters.width = video_width
    parameters.height = video_height
    parameters.stride = stride
    parameters.image_pixel_format = EnumImagePixelFormat.IPF_RGB_888
    parameters.region_top = 0
    parameters.region_bottom = 100
    parameters.region_left = 0
    parameters.region_right = 100
    parameters.region_measured_by_percentage = 1
    parameters.threshold = 0.01
    parameters.fps = 0
    parameters.auto_filter = 1

    # start video decoding. The callback function will receive the recognized barcodes.
    reader.start_video_mode(parameters, text_results_callback_func)

    # # start video decoding. Pass three callbacks at the same time.
    # reader.start_video_mode(parameters, text_results_callback_func, "", intermediate_results_callback_func, error_callback_func, reader)

    while True:
        cv2.imshow(windowName, frame)
        rval, frame = vc.read()
        if rval == False:
            break

        try:
            # append frame to video buffer cyclically
            ret = reader.append_video_frame(frame)
        except:
            pass

        # 'ESC' for quit
        key = cv2.waitKey(1)
        if key == 27:
            break

    reader.stop_video_mode()
    cv2.destroyWindow(windowName)


if __name__ == "__main__":

    print("-------------------start------------------------")

    try:
        # Initialize license.
        # The string "DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9" here is a free public trial license. Note that network connection is required for this license to work.
        # You can also request a 30-day trial license in the customer portal: https://www.dynamsoft.com/customer/license/trialLicense?product=dbr&utm_source=samples&package=python
        error = BarcodeReader.init_license("DLS2eyJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSJ9")
        if error[0] != EnumErrorCode.DBR_OK:
            print("License error: "+ error[1])

        # Decode video from file or camera
        decode_video()

    except BarcodeReaderError as bre:
        print(bre)

    print("-------------------over------------------------")

