# Weihnachtsmarkt Data

This repository is complementary to the [Weihnachtsmarkt App](https://github.com/codeformuenster/weihnachtsmarkt).

The idea is to write a python module for each market and then just use the geojson file to import everythin into kinto.

# Usage

```bash
cat secrets/KINTO_PASSWORD | read KINTO_PASSWORD
export KINTO_PASSWORD="$KINTO_PASSWORD"

sudo --preserve-env docker-compose run import python import.py
```
