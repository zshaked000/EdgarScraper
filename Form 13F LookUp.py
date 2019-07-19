
import requests
import bs4
import csv
from bs4 import BeautifulSoup



def get13F(cik = "0001166559",mostRecent = 0):
    URL = "https://www.sec.gov/cgi-bin/browse-edgar"
    PARAMS = {
        "CIK":cik,
        "type":"13f",
        "date":"",
        "owner":"exclude",
        "count":"100"
    }

    response = requests.get(URL,params=PARAMS)

    if response.status_code == 200:
        print("Success")
        soup = BeautifulSoup(response.content,'lxml')
        # print(soup.find_all('a',id = 'documentsbutton'))

        rawHREFTagsDocumentPageURLS = soup.find_all('a',id = 'documentsbutton')

        documentPageURLS = []

        for tag in rawHREFTagsDocumentPageURLS:
            url = "https://www.sec.gov" + tag.attrs['href']
            documentPageURLS.append(url)


        response = requests.get(documentPageURLS[mostRecent])
        
        soup = BeautifulSoup(response.content,'html.parser')

        tags = soup.find_all('a')

        thirteenFTagsURL = []
        
        for tag in tags:
            # print(tag)
            if tag.text.endswith(".xml") and tag.text != "primary_doc.xml":
                thirteenFTagsURL.append("https://www.sec.gov" + tag.attrs["href"])

        for url in thirteenFTagsURL:
            # print(url)
            # print("made it this far")
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                tags = soup.find_all('infotable')
                # print("tags count: ",len(tags))
                # print("about to write to file")
                with open("outPut.tsv","w",encoding = "utf8",newline = '') as tsv_file:
                    tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
                    tsv_writer.writerow(["NAME OF ISSUER","TITLE OF CLASS", "CUSIP","VALUE", "SHRS OR SH/","DISCRETION","SOLE","SHARED","NONE"])
                    for tag in tags:
                        # print("tag: ",list(tag.children))
                        currentRow = []
                        for column in tag:
                            # print("col:",column)


                            if column.name == "nameofissuer":
                                currentRow.append(column.text)
                            elif column.name == "titleofclass":
                                currentRow.append(column.text)
                            elif column.name == "cusip":
                                currentRow.append(column.text)
                            elif column.name == "value":
                                currentRow.append(column.text)
                            elif column.name == "shrsorprnamt":
                                for col in column.children:
                                    if col.name == "sshprnamt":
                                        currentRow.append(col.text)
                                    elif col.name == "sshprnamttype":
                                        currentRow.append(col.text)
                            elif column.name == "investmentdiscretion":
                                currentRow.append(column.text)
                            elif column.name == "votingauthority":
                                for col in column.children:
                                    if col.name == "sole":
                                        currentRow.append(col.text)
                                    elif col.name == "shared":
                                        currentRow.append(col.text)
                                    elif col.name == "none":
                                        currentRow.append(col.text)

                        tsv_writer.writerow(currentRow)
            else:
                print("failed here")   
    elif response.status_code == 404:
        print("you've got a 404 uh-oh")
    else:
        print("not found")


get13F("0001166559") 
# get13F("0001166559") 
# get13F("0001756111") 
# get13F("0001555283") 
# get13F("0001397545") 
# get13F("0001543160") 
# get13F("0001496147") 
# get13F("0001357955") 
# get13F("0001439289") 
# get13F("0001086364")
