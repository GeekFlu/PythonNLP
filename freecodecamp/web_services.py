import json
import urllib.request
import urllib.error
import urllib.parse

if __name__ == "__main__":
    data = '''
      [
        { "id" : "001",
          "x" : "2",
         "name" : "Quincy"
        } ,
        { "id" : "009",
          "x" : "7",
          "name" : "Mrugesh"
        }
      ]
    '''
    info = json.loads(data)
    print(info[1]['name'])
    service_url = "https://maps.googleapis.com/maps/api/geocode/json?"

    while True:
        address = input("Enter location: ")
        if len(address) < 1:
            break

        url = service_url + urllib.parse.urlencode({'address': address})
        print('Retrieving url: ' + url)
        url_handler = urllib.request.urlopen(url)
        data = url_handler.read().decode()
        try:
            json = json.loads(data)
        except:
            json = None

        if not json or 'status' not in json or json['status'] != 'OK':
            print("Failure********")
            print(data)
            continue

        lat = json["results"][0]["geometry"]["location"]["lat"]
        lng = json["results"][0]["geometry"]["location"]["lng"]
        print(f"Latitude {lat}, Longitude {lng}")
        location = json["results"][0]["formatted_address"]
        print(location)
