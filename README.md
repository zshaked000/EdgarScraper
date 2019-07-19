# EdgarScraper
Given a CIK number retrieve form 13F from the SEC EDGAR database


I was unable to successfully parse the last CIK 0001086364 which was associated to black rock. It is as a result of the check which I used to grab the .xml files by checking the text description of the "\<a href= />" tag. Upon further investigation of the first listed filing I found there is no .xml file other than the primary doc which results in an empty return. https://www.sec.gov/Archives/edgar/data/1086364/000108636419000039/0001086364-19-000039-index.htm


I hope that it is all running well please let me know if there are any modifications I can make or anything further I can provide to more accurately achieve the goals of the challenge description.

