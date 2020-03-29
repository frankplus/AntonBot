#!/usr/bin/python3

import sys
import corona 
import news

print(corona.elaborate_query(sys.argv[1]))

print(news.get_latest_news(sys.argv[1]))