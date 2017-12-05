# Web-Crawler
Description
----------
The repository is used to extract the information of fund from the website of Asset Management Association of China(AMAC), including the information of manager, the fund scale, the register date, the register code, the type, etc.

The code includes both the web crawling of static webpage and dynamic webpage. It also involves distributed web crawling.

Package
--------
re, BeautifulSoup, pandas, requests, threading

Technique
------
exception handling, packet capture, headers, cookies, anti-crawling

Procedure
-----------
request the website(get/post)-->get the response and store them-->decoding and encoding-->process the data-->input and output of files

Data Source
--------
www.amac.org.cn/
