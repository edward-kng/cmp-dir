# cmp-dir

cmp-dir is a small command-line tool to compare two folders and find any missing or modified files. The script ignores folder structure and will not count a file that has been moved or renamed in one folder as missing, as long as it exists in both folders.

Note: Symbolic links are ignored.

## Usage

Clone the repo and run:

```
python3 -m cmp_dir </path/to/folder1> </path/to/folder2> [nr of threads]
```

Threads are optional, but using multiple threads will likely improve performance.

## License

This program is open-source software under the MIT license.
