from flask import Flask,render_template,request,redirect,url_for
import requests
app=Flask(__name__)
@app.route('/')
def stats():
    url=" "
    response=requests.get(url)
    r=response.json()
    print(r)
    return render_template("stats.html",a=sum(r),b=str(r[0]),c=str(r[1]),d=str(r[2]))
if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)