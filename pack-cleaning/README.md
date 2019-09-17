### Pack Cleaning Python Scripts

- `pack_find_duplicates.py` will iterate all the (unpacked) packs and remove the duplicated files
- `pack_merge_files.py` will merge all the (unpacked) packs into a single `d_/` folder
- `pack_generate.py` will split a `d_/` folder into new ready-to-pack packs (all maps in `maps`, and no useless `patch` packs)
- `pack_delete_empty_folders.sh` will remove all the empty folders
- `pack_index_make.py` will generate a new Index from the (unpacked) packs
