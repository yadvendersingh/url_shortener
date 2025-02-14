import streamlit as st
import requests
import re

def validate_url(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(pattern, url) is None:
        return False
    return True

st.title("URL Shortener")
baseurl = "http://localhost:8000/url/"
complete_url = st.text_input("Enter the URL to shorten")
short_url = st.text_input("Enter the short URL")
input = {"complete_url": complete_url, "short_url": short_url}
if st.button("Shorten URL"):
    if not validate_url(complete_url):
        st.write("Please enter a valid URL!")
    elif short_url is None or short_url == "":
        st.write("Please enter a short URL!")
    else:
        res = requests.post(baseurl, json=input)
        if res.status_code==200:
            st.write("Short URL is : "+baseurl+short_url)
        else:
            st.write("Error in shortening the URL:", res.json()["message"])