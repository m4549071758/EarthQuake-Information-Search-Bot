#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import discord
import xml.etree.ElementTree as ET

import settings

token=settings.TOKEN


client = discord.Client()
@client.event
async def on_message(message):
    mc = message.content.split(',')
    if mc[0] == '!ei':
        er = e(mc[1]) if 1<len(mc) else e(0)
        embed = discord.Embed(title='**地震情報**', description='', color=0x51b3fc)
        if er['status'] == 'OK':
            embed = discord.Embed(title='**地震情報**', description='', color=er['color'])
            embed.set_thumbnail(url=er['icon'])
            embed.add_field(name='発生時刻', value=er['time'], inline=True)
            embed.add_field(name='震源地', value=er['epicenter'], inline=True)
            embed.add_field(name='震源の深さ', value=er['depth'], inline=True)
            embed.add_field(name='最大震度', value=er['intensity'], inline=True)
            embed.add_field(name='マグニチュード', value=er['magnitude'], inline=True)
            embed.add_field(name='揺れを観測した地域', value=er['areas'], inline=False)
            embed.set_image(url=er['map'])
        else:
            embed.add_field(name='地震情報', value='該当する地震はありませんでした', inline=True)
        await message.channel.send(embed=embed)

def et_root(xml_data, s):
    root = ET.fromstring(xml_data)
    deta_url = ''
    for item in root.iter('item'):
        if s == 0:
            deta_url = (item.attrib['url'])
            break

        if item.attrib['shindo'] == s:
            deta_url = (item.attrib['url'])
            break
    return deta_url

def e(s):
    xml_data_module = requests.get('https://www3.nhk.or.jp/sokuho/jishin/data/JishinReport.xml')
    xml_data_module.encoding = "Shift_JIS"
    _status = "NG"
    url = et_root(xml_data_module.text, s)
    edic = {'status':_status}
    if url != '':
        deta = requests.get(url)
        deta.encoding = "Shift_JIS"
        root = ET.fromstring(deta.text)
        time, Intensity, Epicenter, Depth, Magnitude, Areas, _map, ei = '', '', '', '', '', '', '', ''
        for Earthquake in root.iter('Earthquake'):
            time = (Earthquake.attrib['Time'])
            Intensity = (Earthquake.attrib['Intensity'])
            Epicenter = (Earthquake.attrib['Epicenter'])
            Magnitude = (Earthquake.attrib['Magnitude'])
            Depth = (Earthquake.attrib['Depth'])
            map_url = 'https://www3.nhk.or.jp/sokuho/jishin/'
        area_list = list(root.iter('Area'))
        for n in range(len(area_list)):
            Areas += '\n' + area_list[n].attrib['Name']
            if n == 9:
                Areas += '\n他'
                break
        for Detail in root.iter('Detail'):
            _map = map_url + Detail.text
            ei = eicon(Intensity)
        _status = 'OK'
        edic = {'status':_status, 'time': time, 'epicenter': Epicenter, "intensity": Intensity, "depth": Depth, "magnitude": Magnitude, "map": _map, "icon": ei["icon"], "color": ei["color"], 'areas': Areas}
    return edic

def eicon(i):
    r = { '1':{'icon':'https://i.imgur.com/yalXlue.png','color':0x51b3fc},
          '2':{'icon':'https://i.imgur.com/zPSFvj6.png','color':0x7dd45a},
          '3':{'icon':'https://i.imgur.com/1DVoItF.png','color':0xf0ed7e},
          '4':{'icon':'https://i.imgur.com/NqC3CE0.png','color':0xfa782c},
          '5-':{'icon':'https://i.imgur.com/UlFLa3G.png','color':0xb30f20},
          '5+':{'icon':'https://i.imgur.com/hExQwf2.png','color':0xb30f20},
          '6-':{'icon':'https://i.imgur.com/p9RrO96.png','color':0xffcdde},
          '6+':{'icon':'https://i.imgur.com/pNaFJ2Y.png','color':0xffcdde},
          '7':{'icon':'https://i.imgur.com/ZoOhL4v.png','color':0xffff6c}}
    return r[i]

client.run(token)
