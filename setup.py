import requests
from bs4 import BeautifulSoup
import time
import csv
header_list = ['Mark:','US Serial Number:','US Registration Number:','Registration Date:','Status Date:','Publication Date:','Attorney Name:','Attorney Primary Email Address:','Attorney Email Authorized:','Correspondent Name/Address:','Correspondent e-mail:','Correspondent e-mail Authorized:','Owner Name:','Owner Address:','Legal Entity Type:','State or Country Where Organized:']
def get_uspto_data(url):
	"""
	获取USPTO网站数据并解析HTML
	"""
	try:
		# 发送GET请求
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
		}
		response = requests.get(url, headers=headers)
		response.raise_for_status()  # 检查请求是否成功
		
		# 解析HTML
		soup = BeautifulSoup(response.text, 'html.parser')
		
		# 返回解析后的soup对象
		return soup
		
	except requests.RequestException as e:
		print(f"请求错误: {e}")
		return None
	except Exception as e:
		print(f"解析错误: {e}")
		return None
def getText(html,text = ''):
    tag = html.find('div',string=text)
    if bool(tag):tag = tag.find_next('div')
    res = ''
    if bool(tag):
        res = tag.text.replace(' ','').replace('\n','').replace('\t','')
    else:
        res = ''
    return res
def getCsvList(soup,i):
	"""
	从soup对象中提取数据并返回一个列表
	"""
	html = soup.prettify()
	try:
		data_list = [str(i)]
		# 提取所需数据
		for header in header_list:
			data = getText(soup,header)
			if data:
				data_list.append(data)
			else:
				data_list.append('')
		
		return data_list
		
	except Exception as e:
		print(f"数据提取错误: {e}")
		return []
try:
		method = int(input("输入查询方法：1、根据输入的最大最小值来获取数据；2、修改更新原来的csv数据\n"))
		if method == 1:
				min_value = int(input("请输入最小值："))
				max_value = int(input("请输入最大值："))
				print(f"您选择了方法1，最小值为{min_value}，最大值为{max_value}")
				# 在这里可以添加根据最小值和最大值获取数据的逻辑
		elif method == 2:
				change_file = input("请输入要修改的csv文件名（不带扩展名）：")
				change_value = input("请输入要修改的值：使用逗号分隔多个值\n")
				change_values = change_value.split(',')
				print("您选择了方法2，修改更新原来的csv数据")
				# 在这里可以添加修改更新csv数据的逻辑
		else:
				print("无效的查询方法，请输入1或2。")
except ValueError:
		print("请输入有效的数字！")
if method == 1:
	f = open(str(min_value)+'.csv',mode='w',newline='',encoding='UTF8')
	rwriter = csv.writer(f)
	rwriter.writerow(['CaseNumber','Mark','US Serial Number','US Registration Number','Registration Date','Status Date','Publication Date','Attorney Name','Attorney Primary Email Address','Attorney Email Authorized','Correspondent Name/Address','Correspondent e-mail','Correspondent e-mail Authorized','Owner Name','Owner Address','Legal Entity Type','State or Country Where Organized'])
	f.close()
	for i in range(min_value, max_value + 1):
		url = f"https://tsdr.uspto.gov/statusview/rn{i}"
		soup = get_uspto_data(url)
		if(soup):
			list1 = getCsvList(soup,i)
		fr = open(str(min_value)+'.csv',mode='a',newline='',encoding='UTF8')
		rwriter = csv.writer(fr)
		rwriter.writerow(list1)
		fr.close()
		print(f"数据已写入 {min_value}.csv 文件，当前处理的注册号为: {i}")
		time.sleep(3)  # 避免请求过于频繁
if method == 2:
	f = open(change_file+'.csv','r')
	csv_reader =csv.reader(f)
	data = list(csv_reader)
	for idx,row in data:
		if row[0] in change_values:
			url = f"https://tsdr.uspto.gov/statusview/rn{i}"
			soup = get_uspto_data(url)
			if(soup):
				list1 = getCsvList(soup,i)
			data[idx] = list1
	fr = open(change_file+'.csv','w', newline='',encoding='UTF8')
	csv_writer = csv.writer(fr)
	csv_writer.writerows(data)
	fr.close()
