#!/usr/bin/env python

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--inputfile','-i',default="SignalNorm_Splines_full.txt",type=str,help='input file')
parser.add_argument('--outputfile','-o',default="./test.txt",type=str,help='output file')
parser.add_argument('--signal','-s',default="grav",type=str,help='signal model')
parser.add_argument('--width','-w',default=-1,type=int)
parser.add_argument('--mass','-m',default=-1,type=int)
parser.add_argument('--debug','-d',action="store_true",help='debug mode')
args = parser.parse_args()

def Read_SignalNorm():
    # Provide the file path
    file_path = args.inputfile
    # Define column names
    columns = ["year", "coup", "mass", "cat", "norm"]
    # Read the data from the file into a DataFrame
    df = pd.read_csv(file_path, sep=" ", header=None, names=columns)
    # Print the resulting DataFrame
    # print(df)
    return df

def get_norm(year, coup, mass, cat, df):
    if (args.signal=="grav"):
        if (coup==14): coupstr = "kMpl001"
        elif (coup==1400): coupstr = "kMpl01"
        elif (coup==5600): coupstr = "kMpl02"
    elif (args.signal=="heavyhiggs"):
        if (coup==14): coupstr = "0p014"
        elif (coup==1400): coupstr = "1p4"
        elif (coup==5600): coupstr = "5p6"
    condition = (df["year"] == year) & (df["coup"] == coupstr) & (df["mass"] == mass) & (df["cat"] == cat)

    # Use loc to filter the DataFrame based on the condition and retrieve the "norm" value
    norm_value = df.loc[condition, "norm"].values[0] if any(condition) else None
    return norm_value

def find_coup_lowhigh(cint):
    ctotal = [14, 1400, 5600]
    for i in range(len(ctotal) - 1):
        if ctotal[i] <= cint <= ctotal[i + 1]:
            return ctotal[i], ctotal[i + 1]
    return None  # If the number is outside the range of the list

def Interpolate(year, cint, mass, cat,df):
    cl, ch = find_coup_lowhigh(cint)
    nl = get_norm(year, cl, mass, cat, df)
    nh = get_norm(year, ch, mass, cat, df)

    nint = ((nh - nl)/float(ch-cl))*float(cint - cl) + nl
    return nint

def Write_interpolate_file():
    df = Read_SignalNorm()
    cats = ["EBEB","EBEE","All"]
    if (args.width == -1): widths = [14, 361, 707, 1054, 1400, 2450, 3500, 4550, 5600]
    else: widths = [args.width]
    if (args.mass == -1):
        masses=[]
        for mass in range(500,6000,10):
            masses.append(mass)
    else: masses = [args.mass]
    # Open the file in write mode and write the lines
    with open(args.outputfile, "w") as file:
        for year in range(2016,2019):
            for coup in widths:
                for cat in cats:
                    for mass in masses:
                        norm = Interpolate(year, coup, mass, cat, df)
                        line = "%i %i %i %s %.6f\n"%(year,coup,mass,cat,norm)
                        print(line)
                        file.write(line)

if __name__ == "__main__":
    Write_interpolate_file()
