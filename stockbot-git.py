import requests
import threading
import time
from bsedata.bse import BSE


mutex=threading.Lock()
stock_api=BSE()


def handler(response):
	query=response['result'][0]['message']['text']
	sender=response['result'][0]['message']['chat']['id']
	query=query.split(" ")
	if len(query)!=2:
		return

	if query[0]=="/price" and query[1].isdigit():
		
		try:
			mutex.acquire()
			resp=stock_api.getQuote(query[1])
			mutex.release()

			msg=" [+]Company Name: {0} \n[+]Current Value: {1} \n[+]Previous open: {2} \n[+]Previous close: {3}\n".format(resp['companyName'],resp['currentValue'],resp['previousOpen'],resp['previousClose'])

		except:
			msg="[*]Invalid stock quote number"

	else:
		msg="[*]Invalid command syntax"

	requests.post("https://api.telegram.org/apikey/sendMessage",data={'chat_id':sender,'text':msg})





def main():
	update_id=801632199
	print("[+]Expecting id "+str(update_id))

	try:
		while True:
			time.sleep(0.2)

			response=requests.post("https://api.telegram.org/apikey/getUpdates",data={'offset':str(update_id)})

			if not response.ok:
				raise Exception

			response=response.json()

			if not response['result']:
				continue

			th=threading.Thread(target=handler,args=(response,))
			th.start()
			update_id+=1
			print("[+]Expecting id "+str(update_id))

	except KeyboardInterrupt:
		print("[+]Exited, last id was "+str(update_id))




if __name__ == '__main__':
	main()