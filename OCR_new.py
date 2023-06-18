from transformers import pipeline
import datetime
import re
captioner = pipeline("image-to-text",model="jinhybr/OCR-Donut-CORD")

import datetime
import re


ERROR_MSG = "not found"
import re
import datetime


ERROR_MSG = "not found"


def split_string(input_string):
    """
    Splits an input string into substrings based on a pattern matching numbers, hyphens, periods, colons, or forward slashes.

    Args:
        input_string (str): The input string to be split.

    Returns:
        list: A list of substrings that match the specified pattern, containing numbers separated by hyphens, periods, colons, or forward slashes. Substrings with less than 5 characters or without any digits are excluded.

    Example:
        >>> split_string("Hello, today is 2023-06-17. How are you?")
        ['2023-06-17']
    """
    # pattern = r"[,./-:d]+"  # Regular expression pattern to match numbers, hyphens, forward slashes, and periods
    pattern = r"\b(\d{0,4}[-,./]\d{0,4}(?:[-,./]\d{0,4})?)\b"
    split_values = re.findall(pattern, input_string)
    pattern = r"\d+"  # Regular expression pattern to match one or more digits
    result = [string for string in split_values if re.search(pattern, string) and len(string) > 4]
    return result

def is_valid_date_format(str):
    """
    Checking if the date has a valid format such as:
    dd.mm.yyy or dd-mm-yyy or dd:mm:yyy or dd/mm/yyy or dd,mm,yyy

    Args:
        str (string): date as string

    Returns:
        bool: true if the date is valid with or without year eles false
    """
    date_without_year = r"^\d{0,2}[-,./]\d{0,2}$"
    date_with_year = r"^\d{0,2}[-,./]\d{0,2}[-,./]\d{0,4}$"
    flag1 = re.match(date_without_year, str)
    flag2 = re.match(date_with_year, str)
    if bool(flag1) or bool(flag2):
        return True
    else:
        return False

def is_valid_date(date_string):
    """
    Checks if a date string is valid and can be parsed according to the format '%d/%m/%Y'.

    Args:
        date_string (str): The date string to be validated.

    Returns:
        bool: True if the date string is valid and can be parsed, False otherwise.

    Example:
        >>> is_valid_date("31/12/2022")
        True
        >>> is_valid_date("2022/12/31")
        False
    """
    try:
        datetime.datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def  run_expiration_date_workflow(string):
    """
        find the date in format dd/mm or dd/mm/yyyy from the given string using regex
    Args:
        string (str): string with date

    Returns:
        str: the date that found from the string in format dd/mm/yyyy or not found
    """
    # Define regex pattern for date format
    print("string ===== ",string )
    strings = split_string(string)
    valid_dates = []


    # all the dates will have / as split
    for char in [',','.','/','-',':']:
        for i in range(len(strings)):
            if len(strings[i]) > 2:
                strings[i] = strings[i].replace(char, "/")


    for i in range(len(strings)):
        if not is_valid_date_format(str=strings[i]):
            if fix_date(strings[i][:4]) == ERROR_MSG:
                strings[i] = ERROR_MSG
            else: 
                strings[i] = fix_date(strings[i][:4]) + strings[i][4:]


    # all the dates will include year
    for i in range(len(strings)):

        if ERROR_MSG in strings[i]:
            continue
        if strings[i].count('/') == 0:
            strings[i] = fix_date(strings[i])
            if strings[i] != ERROR_MSG:
                strings[i] += '/' + datetime.date.today().strftime("%Y")
                valid_dates.append(strings[i])

        elif strings[i].count('/') == 1:
            strings[i] += '/' + datetime.date.today().strftime("%Y")
            valid_dates.append(strings[i])

        elif strings[i].count('/') == 2:
            year = '20'+strings[i][-2:]
            valid_dates.append(strings[i][:-2] + year)


    result=[]
    #   Save only the dates that have valid format
    result = [valid_date for valid_date in valid_dates if is_valid_date(valid_date)]

    #   Sorting the dates from the latest to the earliest
    result.sort(key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y"), reverse=True)

    print("##########")
    if result:
        print(result[0])
        print("##########")
        return result[0]
    else: 
        print(ERROR_MSG)
        print("##########")
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
    try:
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
    except:
        return ERROR_MSG



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

