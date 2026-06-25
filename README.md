# pymp3compressor

Is a small, multi-processor based converter for mp3 file to change bitrate (compressing the file(s)).

This program is inteded to be used as exe file on windows.

If the var source_folder (below) contains subfolders which hold various mp3 files, it can act as bulk-converter. So it can read a file structure such as:

C:\

└── Desktop\

    ├── Artist1\
    
    │   ├── CD1\file(s).mp3
    
    │   ├── CD2\file(s).mp3
    
    │   └── ...
    
    └── Artist2\
    
        ├── CD1\file(s).mp3
        
        └── ...

If you would like to convert a single mp3 file, it works with the same:

C:\

└── Desktop\

    ├── Artist1\
    
    │   ├── CD1\<nothing here>
    
    │   ├── CD2\file1.mp3


Use as directed here:

Format:

  C:\> mp3_compressor.exe "source_folder" "bitrate"

Example:

  C:\Users\tronatorex\Desktop>mp3_compressor.exe "C:\TMP\mp3_compress" "64k"


Code is here provided as .py file.
