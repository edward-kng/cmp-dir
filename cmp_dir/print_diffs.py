def print_diffs(dir1_path, dir2_path, checksums_dir1, checksums_dir2):
    diffs_found = False

    for file in checksums_dir1:
        if not file in checksums_dir2:
            if not diffs_found:
                print(f"\n\nFiles found in {dir1_path} that were missing or changed in {dir2_path}:")
                diffs_found = True
            
            print("\n\tFile located at: ")

            for path in checksums_dir1[file]:
                print("\t\t" + path)
