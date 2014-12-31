#!/usr/bin/env python
# coding: utf-8
 
# You need a RaspberryPi B+ with LED lamps to run this script.
# Also a separate setting.py file should contain:
#
# def get_cred():
#  consumer_key='CONSUMER KEY'
#  consumer_secret='CONSUMER SECRET'
#  access_token='ACCESS TOKEN'
#  access_token_secret='ACCESS TOKEN SECRET'
#  return consumer_key,consumer_secret,access_token,access_token_secret
#
# Copyright 2015 ‌Behzad Tabibian [btabibian at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


from textblob import TextBlob

import RPi.GPIO as GPIO

import time

import ujson

import settings

led_y = 11
led_g = 37
led_r = 16

#returns twitter credentials,
consumer_key, consumer_secret, access_token, access_token_secret = settings.get_cred()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_y,GPIO.OUT)
GPIO.setup(led_r,GPIO.OUT)
GPIO.setup(led_g,GPIO.OUT)

class StdOutListener(StreamListener):

  def on_data(self, data):
    # rcvd data
    data_j = ujson.loads(data)
    GPIO.output(led_y,GPIO.HIGH)
    blob = TextBlob(data_j['text'])
    
    # if sentiment is negative turn red on
    if blob.sentiment.polarity < 0:
      GPIO.output(led_r,GPIO.HIGH)
    # if sentiment is positive turn green on
    if blob.sentiment.polarity > 0:
      GPIO.output(led_g,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(led_y,GPIO.LOW)
    GPIO.output(led_r,GPIO.LOW)
    GPIO.output(led_g,GPIO.LOW)
    return True

  def on_error(self, status):
    print status

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

stream.filter(track=['#iran'])