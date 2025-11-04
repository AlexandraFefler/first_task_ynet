from flask import Flask, jsonify, render_template, Response
from urllib.request import urlopen, Request
from xml.etree import ElementTree as ET

app = Flask(__name__)

RSS_URL = "https://www.ynet.co.il/Integration/StoryRss2.xml"

def fetch_rss_xml():
    req = Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=10) as resp:
        return resp.read()

@app.route("/")
def home():
    # this html fetches from /rss route
    return render_template("index.html")

@app.route("/rss")
def rss():
    try:
        xml_bytes = fetch_rss_xml()
        root = ET.fromstring(xml_bytes)
        channel = root.find("channel")

        items = []
        if channel is not None:
            for it in channel.findall("item"):
                title = (it.findtext("title") or "").strip()
                link = (it.findtext("link") or "").strip()
                pub_date = (it.findtext("pubDate") or "").strip()
                if title:
                    items.append({"title": title, "link": link, "pubDate": pub_date})

        resp = jsonify({"items": items})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except Exception as e:
        err = Response(f"Error: {e}", status=500)
        err.headers["Access-Control-Allow-Origin"] = "*"
        return err

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)