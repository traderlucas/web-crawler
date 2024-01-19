# Usage

Now that the project exists, make a virtual environment:
```bash
$ cd tap-foobar
$ python3 -m venv ~/.virtualenvs/tap-foobar
$ source ~/.virtualenvs/tap-foobar/bin/activate
```
Install the package:
```bash
$ pip install -e .
```

And invoke the tap in discovery mode to get the catalog:
```bash
$ tap-foobar -c sample_config.json --discover
```
The output should be a catalog with the single sample stream (from the schemas folder):
```bash
{
  "streams": [
    {
      "metadata": [],
      "schema": {
        "additionalProperties": false,
        "properties": {
          "string_field": {
            "type": [
              "null",
              "string"
            ]
          },
          "datetime_field": {
            "type": [
              "null",
              "string"
            ],
            "format": "date-time"
          },
          "double_field": {
            "type": [
              "null",
              "number"
            ]
          },
          "integer_field": {
            "type": [
              "null",
              "integer"
            ]
          }
        },
        "type": [
          "null",
          "object"
        ]
      },
      "stream": "sample_stream",
      "key_properties": [],
      "tap_stream_id": "sample_stream"
    }
  ]
}
```
If this catalog is saved to a `catalog.json` file, it can be passed back into the tap in sync mode:
```
tap-foobar -c sample_config.json --properties catalog.json
```

Now you build the tap!

# Testing

Before testing the Tap we need to generate all catalogs that will be validated during the tests, 
make sure to create and commit all catalogs.

Create one catalog for one stream.
```
tap-produtos-crawler -c sample_config.json --discover > tap_produtos_crawler/catalogs/sample_catalog.json
```

With everything created, run:
```
make test
```

# Docker

Tap is done? Nice!
To publish our tap we just need to run the following steps:

Docker Build:
```sh
make TAP_NAME=tap-produtos-crawler build_tap
```
Publishing a Docker Image:
```sh
make TAP_NAME=tap-produtos-crawler publish_tap
```