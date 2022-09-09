import { StyleSheet, Text, View, Image, ScrollView } from 'react-native';
import { WebView } from 'react-native-webview';


export default function App() {
  let iframes = [
    '<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1850701/widgets/517041"></iframe>',
    '<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1850701/widgets/517795"></iframe>',
    '<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1850701/widgets/517796"></iframe>',
    '<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1850701/charts/1?color=%23db6f6d&dynamic=true&results=60&timescale=15&title=Temperature&type=line&xaxis=Time&yaxis=Temperature"></iframe>',
    '<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1850701/charts/2?color=%238daccd&dynamic=true&results=60&timescale=15&title=Humidity&type=line&xaxis=Time&yaxis=Humidity"></iframe>',
    '<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1850701/maps/channel_show"></iframe>'
  ]
  return (
    <View style={styles.container}>
      <View style={styles.headingWrapper}>
        <Image source={{uri: 'https://bloom-air-img.s3.eu-west-1.amazonaws.com/bloomAirLogoNoText.jpeg'}} style={styles.tinyLogo}/>
        <Text style={styles.headingText}>BloomAir Dashboard</Text>
      </View>
      <ScrollView>
        {iframes.map((iframe, index) => <WebView
          key={index}
          scalesPageToFit={true}
          bounces={false}
          scrollEnabled={false}
          javaScriptEnabled
          style={{ height: 200, width: 450}}
          source={{
            html: `
                  <!DOCTYPE html>
                  <html>
                    <head>
                      <meta name="viewport" content="user-scalable=0 width=device-width, initial-scale=0.7, maximum-scale=0.7">
                    </head>
                    <body>
                      <div id="baseDiv">
                        ${iframe}
                      </div>
                    </body>
                  </html>
            `,
          }}
          automaticallyAdjustContentInsets={false}
          />
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#fff',
    marginLeft: 30,
    marginRight: 'auto',
    marginTop: 50
  },
  headingWrapper: {
    display: 'flex',
    flexDirection: 'row'
  },
  headingText: {
    marginTop: 8,
    fontSize: 22,
    color: '#db6f6d'
  },
  tinyLogo: {
    width: 50,
    height: 50,
  },
});
