#!/usr/bin/env python3
import os
import json
import base64
import singer
from datetime import datetime
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema
from google.cloud import storage

import tap_produtos_crawler.crawler.main as crawler_extraction


def get_products_from_gcs(config, stream):
    creds = base64.b64decode(config["base64_file"]).decode("ascii")
    creds_json = json.loads(creds)

    storage_client = storage.Client.from_service_account_info(creds_json)
    bucket = storage_client.get_bucket("raw_data_crawler_produtos")
    blob = bucket.blob(f"{stream}.csv")
    return blob.download_as_bytes()


REQUIRED_CONFIG_KEYS = ["base64_file"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """Load schemas from schemas folder"""
    schemas = {}
    for filename in os.listdir(get_abs_path("schemas")):
        path = get_abs_path("schemas") + "/" + filename
        file_raw = filename.replace(".json", "")
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        stream_metadata = []
        key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def sync(config, state, catalog):
    """Sync data from tap source"""
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        bookmark_column = stream.replication_key
        is_sorted = True
        stream_metadata = metadata.to_map(stream.metadata)
        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=metadata.get(
                stream_metadata, (), "table-key-properties"
            ),
        )

        products = get_products_from_gcs(
            config=config, stream=stream.tap_stream_id
        )

        tap_data = crawler_extraction.main_extract(
            tap_stream_id=stream.tap_stream_id, products=products
        )

        extracted_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tap_data = [
            {**item, "extracted_at": extracted_at} for item in tap_data
        ]

        max_bookmark = None

        for row in tap_data:

            # write one or more rows to the stream:
            singer.write_records(stream.tap_stream_id, [row])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state(
                        {stream.tap_stream_id: row[bookmark_column]}
                    )
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, row[bookmark_column])
        if bookmark_column and not is_sorted:
            singer.write_state({stream.tap_stream_id: max_bookmark})
    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
