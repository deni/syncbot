import requests
import json


def api_request(domain, token, data_specific):
	headers = {
		'Authorization': 'Bearer ' + token,
	}
	
	data_base = {
		"utf8": 1,
		"format": "json",
		"formatversion": "2",
		"curtimestamp": 1,
	}
	
	url = 'https://{}/w/api.php'.format(domain)
	
	try:
		response = requests.post(
			url,
			headers = headers,
			data = data_base | data_specific
		)
		response_json = response.json()
	except:
		return(False)
	
	if 'error' in response_json:
		print(response_json)
		
		return(False)
	
	return(response_json)

def get_watchlist_feed(domain, token, timestamp_from):
	data_specific = {
		"action": "query",
		"list": "watchlist",
		# "wlallrev": 1,
		"wlend": timestamp_from,
	}
	
	result = api_request(domain, token, data_specific)
	watchlist = result['query']['watchlist']
	
	if type(watchlist) is list:
		return(result)
	else:
		return(False)

def watchlist_feed_pages(feed):
	watchlist = feed['query']['watchlist']
	try:
		pages = []
		for page in watchlist:
			pages.append(page['title'])
		return(pages)
	except:
		return(False)

def get_csrf(domain, token):
	data_specific = {
		'action': 'query',
		'meta': 'tokens',
		'type': 'csrf'
	}
	
	result = api_request(domain, token, data_specific)
	
	try:
		csrf = result['query']['tokens']['csrftoken']
	except:
		return(False)
	
	return(csrf)

def page_edit(
	domain,
	token,
	page_id,
	base_revision,
	text,
	summary,
	minor,
):
	csrf = get_csrf(domain, token)
	
	data_specific = {
		'action': 'edit',
		'pageid': page_id,
		'text': text,
		'summary': summary,
		'bot': 1,
		'baserevid': base_revision,
		'nocreate': 1,
		'token': csrf,
	}
	
	if minor:
		data_specific['minor'] = 1
	
	result = api_request(domain, token, data_specific)
	if not result:
		return(False)
	
	if result['edit']['result'] == 'Success':
		return(result)
	else:
		return(False)

def page_read(
	domain,
	token,
	page_id,
):
	data_specific = {
		'action': 'query',
		'prop': 'revisions',
		'pageids': page_id,
		'rvprop': 'flags|content|ids',
		'rvslots': '*',
	}
	
	result = api_request(domain, token, data_specific)
	
	if result['query']['pages'][0]['revisions'][0]['slots']['main']['content']:
		return(result)
	else:
		return(False)

