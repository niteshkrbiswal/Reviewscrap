from flask import Flask,request,jsonify,render_template
#from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests


app = Flask(__name__)
@app.route("/",methods=["GET"])
#@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review",methods=["POST","GET"])
def index():
    if request.method=="POST":
        try:
            searchString=request.form['content'].replace(" ","")
            flipkart_url='https://www.flipkart.com/search?q='+searchString
            uClient=uReq(flipkart_url)
            flipkartPage=uClient.read()
            uClient.close()
            flipkart_html=bs(flipkartPage,"html.parser")
            bigboxes=flipkart_html.findAll("div",{"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box=bigboxes[0]
            #url=big_box[0].a["href"]
            #complete_url=flipkart_url+url
            complete_url='https://www.flipkart.com'+box.div.div.div.a["href"]


            request_url=requests.get(complete_url)
            request_url.encoding="utf-8"
            beautified_url=bs(request_url.text,"html.parser")
            print(beautified_url)
            review_page=beautified_url.find_all("div",{"class":"_16PBlm"})

            filename=searchString+".csv"
            fw=open(filename,"w")
            headers="product,Price,Customer Name,Rating,Heading,Comment \n"
            fw.write(headers)

            reviews=[]
            for commentbox in review_page:
                try:
                    price = commentbox.find_all("div", {"class": "_30jeq3 _16Jk6d"})[0].text
                except:
                    price="No price"
                try:
                    name = commentbox.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
                except:
                    name="No Name"

                try:
                    rating = commentbox.find_all("div", {"class": "_3LWZlK _1BLPMq"})[0].text
                except:
                    rating="No rating"

                try:
                    commentHead = commentbox.find_all("p", {"class": "_2-N8zT"})[0].text
                except:
                    commentHead="No heading"

                try:
                    comtag = commentbox.find_all("div", {"class": ""})[0].div.text

                except Exception as e:
                    print("Exception while creating dictionary:",e)
                mydict={"Product":searchString,"price":price,"Name":name,"Rating":rating,"CommentHead":commentHead,"Comment":comtag}
                reviews.append(mydict)
            return render_template('results.html',reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print("The Exception message is :",e)
            return "something is wrong"
    #return render_template('results.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(port=5001)