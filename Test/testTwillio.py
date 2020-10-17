from twilio.rest import Client

account_sid = 'AC2b7b24efed2b931eae736299db0b6d69'
auth_token = '990e4e9094bf5fb1d92920074aea0f4e'

client = Client(account_sid, auth_token)
message = client.messages.create(to='9137497489',
                                 from_='+12058983945',
                                 body = "Its me Suhaan, Sending Text from Twillio lol!! YAYYYYY!!!")
#,media_url="your pic.jpg url")
print(message.sid) 