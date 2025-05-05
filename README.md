# iniMerger - Merge Multiple INIs Into One

Be default, the program looks for ini files located in "mergeinis", a folder in the same directory as the script. It will take all of these ini files, and merge them into a single file named "Output.ini".

For keys included in multiple ini files, the last file alphabetically wins. So if key `example.key` is in ini files `00.ini`, `01.ini`, and `17.ini`, then the value from `17.ini` will be the one used. The exception to this is the keys listed in `allowedDupes` inside of `iniMerger.ini`.

## Configuration Options (iniMerger.ini)
- `inputFolder`: The name of the folder containing all the ini files to merge
- `outputFile`: The name of the final merged ini that gets created
- `allowedDupes`: Keys that can appear multiple times in the merged ini, instead of the last merged file winning. By default this line is commented out, uncomment and set as desired if needed.

## Attributions

[Merge icon created by iconixar - Flaticon](https://www.flaticon.com/free-icons/merge)
