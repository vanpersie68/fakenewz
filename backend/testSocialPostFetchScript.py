import csv

from services.articledata import extract_article_metadata

csv.field_size_limit(500 * 1024 * 1024)
total = 0
withImage = 0
withTitle = 0
withDes = 0
error =0

with open("politifact_fake.csv", encoding='UTF-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        url = row[1]
        print(f_csv.line_num)
        if url.startswith("http"):
            total +=1
            try:
                metadata = extract_article_metadata(url)
                if metadata["title"]:
                    withTitle+=1
                if metadata["image"]:
                    withImage+=1
                if metadata["description"]:
                    withDes+=1
            except Exception:
                error+=1

print("total:" + str(total))
print("with image:" + str(withImage))
print("with title:" + str(withTitle))
print("with description:" + str(withDes))
print("error:" + str(error))



