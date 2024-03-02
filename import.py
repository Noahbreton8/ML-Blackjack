#python.exe -m pip install --upgrade pip
import pandas as pd

def importData():
    trainData = pd.read_csv("C:\\Users\\Noah\\Documents\\file1.csv", header = None) #if no header
    testData = pd.read_csv("C:\\Users\\Noah\\Documents\\file1.csv", header = None) #if no header

def main():
    importData()

main()