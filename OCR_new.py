from transformers import pipeline
import datetime
import re
captioner = pipeline("image-to-text",model="jinhybr/OCR-Donut-CORD")


ERROR_MSG = "not found"

def split_string(input_string):
    pattern = r"[,./-:d]+"  # Regular expression pattern to match numbers, hyphens, forward slashes, and periods
    split_values = re.findall(pattern, input_string)
    pattern = r"\d+"  # Regular expression pattern to match one or more digits
    result = [string for string in split_values if re.search(pattern, string) and len(string) > 4]
    return result

def is_valid_date(string):
    try:
        datetime.datetime.strptime(string, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def  run_expiration_date_workflow(string):
    """
        find the date in format dd/mm or dd/mm/yyyy from the given string using regex
    Args:
        string (str): string with date

    Returns:
        str: the date that found from the string or not found
    """
    # Define regex pattern for date format
    print("string = ",string )
    strings = split_string(string)
    valid_dates = []


    # all the dates will have / as split
    for char in [',','.','/','-',':']:
        for i in range(len(strings)):
            if len(strings[i]) > 2:
                strings[i] = strings[i].replace(char, "/")

    # all the dates will include year
    for i in range(len(strings)):
        if strings[i].count('/') == 2:
            year = '20'+strings[i][-2:]
            valid_dates.append(strings[i][:-2] + year)


        elif strings[i].count('/') == 1:
            strings[i] += '/' + datetime.date.today().strftime("%Y")
            valid_dates.append(strings[i])

        # numbers -> date , fix date func
        elif strings[i].count('/') == 0:
            strings[i] = fix_date(strings[i])
            if strings[i] != ERROR_MSG:
                strings[i] += '/' + datetime.date.today().strftime("%Y")
                valid_dates.append(strings[i])

    result=[]
    result = [valid_date for valid_date in valid_dates if is_valid_date(valid_date)]
    if result:
        return result[0]
    else: 
        return ERROR_MSG



def fix_date(date:str):
    """
    changing the format of the date to be dd/mm \n
    if the numbers of the date are non sense for example month or day with hte number 77\n
    it will return not found\n
    Args:   
        date (str): the numbers of the date only

    Returns:
        str: dd/mm date format or not found
    """
    day = ''
    month = ''
    
    if date[0] == '0':
        day = date[1]
        if date[2] == '0':
            month = date[3]
        else:
            month = date[2:4]
    else:
        day = date[:2]
        if date[2] == '0':
            month = date[3]
        else:
            month = date[2:4]

    #   in case we got invalid date
    if int(month) > 12 or int(day) > 31:
        return ERROR_MSG
        
    return f"{day}/{month}"


from PIL import Image

import os

# Get the current directory
dir_path = os.getcwd()

# List all files in the directory
all_files = os.listdir(dir_path)

# Filter out only the PNG files
png_files = [file for file in all_files if file.endswith('.png')]
print(png_files)
for png_img in png_files:
    # Load the image
    image = Image.open(png_img)

    data = captioner(image)

    # print(f"{png_img} string sent:", data[0]['generated_text'])
    print(f"{png_img} = ", run_expiration_date_workflow(data[0]['generated_text']))

