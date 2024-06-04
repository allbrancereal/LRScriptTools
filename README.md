LRScriptToolsV1 - Automate voiceovers for your Video Scripts

Or as I like to call it, the automatic audio file and closed captioning generator for my video essay. I've been working on a Skyrim video that is longform, it's going to be quite in depth and I felt like it was a big undertaking to do it properly. The problem is that there is no direct conversion from plain text to closed caption SRT files. My suite of tools solves my templating issue by pre-estimating the word spoken length, using this each sentence has a SRT and WAV file generated with the estimated length. You can drop this folder into premiere, and then drop the bin in premiere directly into the timeline. It sets up the basic closed captioning and lines up your audio files as best as possible. Additionally, marker files are provided for Adobe Audition and http://markerbox.pro/ (Free) for Adobe Premiere Pro. You can either run the python scripts from source, or the binary files separately. A AIO Setup is provided to run each exe sequentially just from a TXT file, you can also not run the app from the setup and run each binary individually. Soo in Audition you have a huge list, and each marker- you can read your subtitle from the marker and adjust the audio files as needed, obviously the final script needs to be conformed to the captions, that script will come soon as v1.1 let me finish my essay first though

Features:
- Exported TXT files from Google Docs or Notepad are converted to a HTML file similar to Google Docs HTML output format- where each field is indexed by sentence. The field carries the text and a random color (one of three, never sequentially the same 2 colors)
- Converts the HTML to JSON for further processing, the HTML can be viewed for convenience.
- Using the JSON, and pre-defined configuration
- Command Line Support
- Individual Scripts are turned to EXE with UI ability, you can run LTextTagger.exe on a TXT file to make the HTML, you can run LScriptGenerator.exe to generate the JSON from the HTML, you can run LPremiereWavPrepare.exe to Premake Markers, Wavs & Subtitles. All of these use command line and the start script is just a convenience script that runs all the EXE's sequentially
- AIO Installer has all the EXE's baked in, installs to the installer/install dir and asks if you want to run the script. It doubles as a way for users to change spoken word length.

Limitations:
- It does not convert premiere generated files, as they are correct already.
- It currently does NOT overwrite WAV files after generating, if you change the spoken word length it still requires you to manually delete the old wav files
- The installer sometimes does not like it when you start from it, so just use the LStart.exe 

Github will be made available soon, source code is provided.

Free for non commercial use, if you use it please attribute to me. Shameless self promo:
This is the upcoming channel that I want to upload my longform essay: https://www.youtube.com/channel/UCEXAfoxkvqjFTRNrurGVWiw

Using my time estimate the sequence is about 4 hrs for 17 pages, seems kind of right at .6 words per second.
If you need quick help you can join my discord for all my scripts: https://discord.gg/MqfxQRwNnT
