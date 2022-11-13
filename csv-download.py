def main():

    import requests

    url = "https://repo.hops.works/master/hopsworks-tutorials/data/iris.csv"

    with requests.get(url, stream=True) as response:
        response.raise_for_status()

        with open("iris_data.csv", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            file.flush()

    print("Done")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())