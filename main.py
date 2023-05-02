import requests,json,re
from bs4 import BeautifulSoup
import openai
# calling chatgpt api key
openai.api_key="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"
model_engine="text-davinci-003"
#getting the url
search_query=input("enter the text----").replace(" ","_")
url = f'https://en.wikipedia.org/wiki/{search_query}'
print(url)

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")




# getting images


imagedata=[]
all_images = soup.find_all('div',{'class':'thumbinner'})
for image1 in all_images:
    if len(image1.find_all('div',{'class':'tsingle'}))!=0:
      tsingles=image1.find_all('div',{'class':'tsingle'})
      for tsingle in tsingles:
        thumbimage=tsingle.find('div',{'class':'thumbimage'})
        image=thumbimage.find('img')
        image=image.get('src') if image else ""
        caption=tsingle.find('div',{'class':'thumbcaption'})
        caption=caption.text if caption else " "
        image_info={
          "link":"https:"+image,
          "caption":caption
        }
        imagedata.append(image_info)
        
    else:  
      image=image1.find('img',{'class':'thumbimage'})
      image=image.get('src') if image else " "
      caption=image1.find('div',{'class':'thumbcaption'})
      caption=caption.text if caption else " "
      image_info={
        "link":"https:"+image,
        "caption":caption
      }
      imagedata.append(image_info)

try:
  gallery=[]
  galarydatas=soup.find_all('li',{'class':'gallerybox'})
  for galarydata in galarydatas:
    image=galarydata.find('img')
    image=image.get('src') if image else " "
    caption=galarydata.find('div',{'class':'gallerytext'})
    caption=caption.text if caption else " "
    image_info={
        "link":"https:"+image,
        "caption":caption
      }
    gallery.append(image_info)
    imagedata=imagedata+gallery
except:
  pass

with open("image_info.json","w") as file:
  json.dump(imagedata,file)







  
# Get all the paragraphs in the page
paragraphs = soup.find_all('p')
# content=[{"title":"-----","content_text":"  "}]
content=[]
heading1=""
for para1 in paragraphs:
    heading=para1.find_previous('h2').text
    heading=re.sub(r"\[+[\w+\ ]+\]"," ",heading).upper()
    if heading1!=heading:
      print("----->",heading)
      try:
        data_info={
        "title":heading1,
        "content_text":content_text
        }
        content.append(data_info)
      except:
        pass
      content_text=" "
    para=para1.text
    # para=re.sub(r"\[+[\w+\ ]+\]"," ",para)
    # prompt=f"write the summary of the given paragraph in 50 words-'{para}'"
    # completion=openai.Completion.create(engine=model_engine,prompt=prompt,max_tokens=1024,n=1,stop=None,temperature=0.5)
    # para=completion.choices[0].text
    # print("Paragraph:", para)
    content_text=content_text+para
    heading1=heading

with open("content_info.json","w") as file:
  json.dump(content,file)