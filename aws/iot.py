import requests

class IOT:
    def __init__(self):
        self.endpoint = "a38xyah013qn9m-ats.iot.eu-west-1.amazonaws.com"
        self.cert = "/home/pi/BloomAir/aws/certs/linux_mock_thing.cert.pem"
        self.key = "/home/pi/BloomAir/aws/certs/linux_mock_thing.private.key"
        self.topic = "bloomair/test"
    
    def publish(self, message):
        # create and format values for HTTPS request
        publish_url = 'https://' + self.endpoint + ':8443/topics/' + self.topic + '?qos=1'
        publish_msg = message.encode('utf-8')

        # make request
        publish = requests.request('POST',
                    publish_url,
                    data=publish_msg,
                    cert=[self.cert, self.key])

        # print results
        print("Response status: ", str(publish.status_code))
        if publish.status_code == 200:
                print("Response body:", publish.text)
