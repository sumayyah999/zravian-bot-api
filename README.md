# [zravian](https://zravian.com) bot api

## Overview

This API library is meant to ease the development of bots for travian v3.6. It was designed to work for zravian specifically as other private servers might have a different API. 

## Running the tests
### Running tests using PyCharm
In order to create a new `configuration` to run, go to 
`Run → Edit Configurations... → Hit the + in top-left → Python tests → Unittests`. 

Configure the `Target:` as `Module Name` having the module name `tests`.

Make sure that `./tests/configs` is marked as `Resource Root` and `./api` is marked as `Sources Root`. To do this, `right click on the directory → Mark Directory as → Sources Root`  