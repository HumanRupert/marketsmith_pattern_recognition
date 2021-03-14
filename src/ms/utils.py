from datetime import date


def convert_msdate_to_date(ms_date):
    str_btwn_paranthesis = ms_date[ms_date.find("(")+1:ms_date.find(")")]

    if(str_btwn_paranthesis[0] == "-"):
        millis = int(str_btwn_paranthesis.split("-")[1]) * -1
    else:
        millis = int(str_btwn_paranthesis.split("-")[0])

    date_obj = date.fromtimestamp(millis/1000)
    return date_obj
