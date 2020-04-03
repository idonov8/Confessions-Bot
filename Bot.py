
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import facebook
import time


def main(posts):
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : "159611571402099",  # Step 1
    "access_token" : "EAAaSal46B0oBAG83cLVZAdyNFeOG12kZAgvXVoHyZCV0Dj3RQKdtLoecYf2b9e300yDho1nN9Uko3XgjnfrinyxsaAOCY5AvzdajldBciZCiMMCzj2asA1IYZCR3anvZBdiZC3E9he0eeRKoenTkfk1bwEWmXPefxkZD"   # Step 3
    }

  api = get_api(cfg)
  if posts:
	  for post, number in posts.iteritems():
	  	msg = "#" + str(number) + " - " + post
	  	status = api.put_wall_post(msg)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

while True:

  scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('Bot_secrets.json', scope)
  client = gspread.authorize(creds)

  sheet = client.open('Confessions Bot').sheet1
  confessions = sheet.col_values(2)
  posts = {}
  for i in range(1, len(confessions)):
    num = int(sheet.cell(i, 3).value)
    global numz
    numz = sheet.cell(i+1, 3).value
    if not numz and sheet.cell(i+1, 2).value:
      sheet.update_cell(i+1, 3, str(num+1))
      posts[sheet.cell(i+1, 2).value] = num +1

  print(posts)
  print(time.ctime())

  if __name__ == "__main__":
    main(posts)

  time.sleep(3600)
