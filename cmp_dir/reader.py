from hashlib import sha256
from threading import Thread, Lock, active_count
from sys import stdout
import os

class Reader:
    def __init__(self, dir1, dir2, maxThreads):
        self._dirs = (dir1, dir2)
        self._lock = Lock()
        self._nr_bytes = 0
        self._nr_bytes_read = 0
        self._data = ({}, {})
        self._maxThreads = maxThreads
        self._threads = []

    def _count_bytes(self, path):
        for item in os.listdir(path):
            item_path = path + "/" + item

            if os.path.isdir(item_path):
                self._make_thread(self._count_bytes, (item_path,))
            elif not os.path.islink(item_path):
                with self._lock:
                    self._nr_bytes += os.path.getsize(item_path)

    def _read_files(self, path, dict):
        for item in os.listdir(path):
            item_path = path + "/" + item

            if os.path.isdir(item_path):
                self._make_thread(self._read_files, (item_path, dict))
            elif not os.path.islink(item_path):
                self._make_thread(self._read_file, (item_path, dict))
                

    def _read_file(self, path, dict):
        file = open(path, "rb")
        data = file.read()
        file.close()
        checksum = sha256(data).hexdigest()

        with self._lock:
            self._nr_bytes_read += os.path.getsize(path)

        if self._nr_bytes > 0:
            stdout.write(
                "\rReading files..."
                + "{:.2f}".format(
                    round((self._nr_bytes_read / self._nr_bytes) * 100, 2)
                ) + "%   "
            )

        if not checksum in dict:
            dict[checksum] = []
        
        dict[checksum].append(path)

    def _make_thread(self, functionName, functionArgs):
        if active_count() < self._maxThreads:
            with self._lock:
                thread = Thread(
                        target=functionName,
                        args=functionArgs
                    )
            
                thread.start()
                self._threads.append(thread)
        else:
            functionName(*functionArgs)

    def read(self):
        stdout.write("\nCounting folder sizes...")

        for i in range(2):
            self._make_thread(self._count_bytes, (self._dirs[i],))

        for thread in self._threads:
            thread.join()

        self._threads = []

        for i in range(2):
            self._make_thread(self._read_files, (self._dirs[i], self._data[i]))

        for thread in self._threads:
            thread.join()

        return self._data
