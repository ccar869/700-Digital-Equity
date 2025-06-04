from test import speedTest
import json

def main():
    internetTestToJson()


def internetTestToJson():
    results = speedTest()
    
    json_result = {
        "download": results[0],
        "upload": results[1],
        "packet_loss": results[2],
        "avg_ping": results[3]
    }

    print(json.dumps(json_result, indent=4))


if __name__ == "__main__":
    main()