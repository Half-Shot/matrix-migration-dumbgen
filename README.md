# matrix-migration-dumbgen

Creates dummy migration files for various services including Hipchat

## Running

Simply run `main.py -h` to discover the available options.

For example, to generate a hipchat export with 2000 rooms and 1000 users: `./main.py --hipchat export.tar.gz -u 2000 -r 1000 --email dummy@half-shot.uk`
