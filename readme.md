# RESTDB
A simple REST API server base MariaDB

## /set
|param|description|
|--------|-------|
|key|key|
|value|value|
|password|kv password|
|token|md5(unix_timestamp_sec/30 + (main or kv password))|

## /get
|param|description|
|--------|-------|
|key|key|
|token|md5(unix_timestamp_sec/30 + kv password)|
