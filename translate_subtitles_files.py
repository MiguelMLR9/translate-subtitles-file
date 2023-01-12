from googletrans import Translator, LANGUAGES
import re
import traceback
def total_lines(lines:int,text:str)->str:
    text=text.split()
    number_of_words=len(text)
    if number_of_words%lines==1:
        total_words_per_line=max(number_of_words//lines,round(number_of_words/lines))+1
    else:
        total_words_per_line=max(number_of_words//lines,round(number_of_words/lines))
    aux=""
    text2=[]
    for i in range(len(text)):
        aux+=text[i]+" "
        if i==0:
            continue
        if (i+1)%total_words_per_line==0 or i==len(text)-1:
            text2.append(aux.strip()+"\n")
            aux=""
    return text2

try:
    translator=Translator()
    filename=input("filename:")
    ext=input("file extension (.srt, .txt, ...):")
    source_language_code=input("source language code (if don't know just press enter [dict with all 'code':'language' will be printed]):")
    if source_language_code=="":
        print(LANGUAGES)
        source_language_code=input("source language code:")
    destination_language_code=input("destination language code:")
    text=""
    with open(filename+ext,'r',encoding='utf-8') as file:
        text=file.readlines()
    phrase=''
    index_number=[]
    translated_text=[]
    for index, value in enumerate(text[:60]):
        if index==0 or value=="\n" or "-->" in value or (re.fullmatch("[\d]{1,5}\\n",value)and text[index-1]=="\n") or "</font>" in value:
            continue
        if "-->" in text[index-1]:
            if text[index+1]=="\n":
                while True:
                    try:
                        text[index]=translator.translate(value,dest=destination_language_code,src=source_language_code).text+"\n"
                        break
                    except:
                        print("retry")
                        pass
                continue
            phrase=value.replace("\n"," ")
            index_number.append(index)
            continue
        index_number.append(index)
        phrase+=value.replace("\n"," ")
        if text[index+1]=="\n":
            while True:
                try:
                    phrase=translator.translate(phrase,dest=destination_language_code,src=source_language_code).text
                    break
                except:
                    pass
            translated_text=total_lines(len(index_number),phrase)
            for i in range(len(translated_text)):
                text[index_number[i]]=translated_text[i]
            phrase=""
            index_number=[]
    with open(destination_language_code+"_"+filename+ext,"w",encoding="utf-8") as file:
        file.writelines(text)
    print("ALL DONE!")
except:
    print(traceback.format_exc())
input()