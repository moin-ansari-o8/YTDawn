# 🎬 YTDawn - YouTube Audio/Video Downloader

A simple, clean Python program to download audio (and eventually video) from YouTube using yt-dlp.

## ✨ Features

- 🎵 Download audio in high-quality OPUS format
- 📋 Track downloads in JSON file
- ✅ Automatic duplicate detection
- 📁 Customizable download location
- 🔄 Resume incomplete downloads
- 💾 Persistent download history
- **⚡ SUPER EASY: Just add bare links to JSON and run!**

## 🚀 Quick Start - The Easy Way!

### Method 1: Edit JSON Directly (Recommended for Multiple Downloads)

1. Open `downloads.json`
2. Add your links:
   ```json
   {
     "audio": {
       "links": [
         {"link": "https://www.youtube.com/watch?v=VIDEO_ID_1"},
         {"link": "https://www.youtube.com/watch?v=VIDEO_ID_2"},
         {"link": "https://www.youtube.com/watch?v=VIDEO_ID_3"}
       ]
     },
     "video": {"links": []},
     "meta": {"default-path": "downloads"}
   }
   ```
3. Run: `python ytdawn.py`
4. Select option `1` (Download Audio)
5. Done! All your links will download automatically!

**That's it!** You don't need to add `is_downloaded`, `format`, or `path` fields - the program adds them automatically!

### Method 2: Use Interactive Menu (For Single Downloads)

1. Run: `python ytdawn.py`
2. Select option `3` (Add Audio Link)
3. Paste your URL
4. Select option `1` (Download Audio)

## 📦 Installation

1. **Install Python** (3.7 or higher)

2. **Install yt-dlp**:
   ```bash
   pip install -r requirements.txt
   ```

   Or manually:
   ```bash
   pip install yt-dlp
   ```

## 🚀 Usage

### Quick Start

Run the program:
```bash
python ytdawn.py
```

### Menu Options

1. **Download Audio** - Downloads all pending audio links
2. **Download Video** - (Coming soon)
3. **Add Audio Link** - Add a new YouTube URL for audio download
4. **Add Video Link** - Add a new YouTube URL for video download
5. **View All Links** - See all tracked links and their status
6. **Change Download Path** - Modify where files are saved
7. **Exit** - Close the program

### Example Workflow

1. Run `python ytdawn.py`
2. Select option `3` to add an audio link
3. Paste your YouTube URL
4. Select option `1` to download audio
5. Files will be saved to the `downloads` folder (or your custom path)

## 📄 JSON Structure

The `downloads.json` file tracks all your downloads:

```json
{
  "audio": {
    "links": [
      {
        "link": "https://youtube.com/watch?v=example",
        "is_downloaded": true,
        "format": "opus",
        "path": "downloads"
      }
    ]
  },
  "video": {
    "links": []
  },
  "meta": {
    "default-path": "downloads"
  }
}
```

### Fields Explained

- `link` - The YouTube URL
- `is_downloaded` - Download status (true/false)
- `format` - Audio format (opus for audio)
- `path` - Where the file was saved
- `default-path` - Default download directory

## 🎯 How It Works

1. **Startup Check**: Verifies yt-dlp is installed
2. **Load JSON**: Reads `downloads.json` or creates new one
3. **User Selection**: Choose audio or video download
4. **Process Queue**: Downloads all links where `is_downloaded` is false or missing
5. **Update Status**: Marks completed downloads and saves to JSON
6. **Repeat**: Continue adding/downloading as needed

## 🛠️ Manual JSON Editing

You can manually add links to `downloads.json`:

```json
{
  "audio": {
    "links": [
      {
        "link": "https://youtube.com/watch?v=VIDEO_ID_1",
        "is_downloaded": false,
        "format": "opus",
        "path": ""
      },
      {
        "link": "https://youtube.com/watch?v=VIDEO_ID_2",
        "is_downloaded": false,
        "format": "opus",
        "path": ""
      }
    ]
  }
}
```

Then run the program and select "Download Audio" to process them all.

## 📁 File Structure

```
ytdawn/
├── ytdawn.py           # Main program
├── downloads.json      # Download tracking database
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── downloads/         # Default download folder (created automatically)
```

## 🎵 Audio Download Details

- **Command Used**: `yt-dlp -x -f bestaudio --audio-format opus -P "PATH" "URL"`
- **Format**: OPUS (high quality, small size)
- **Quality**: Best available audio
- **Output**: Separate audio file (no video)

## 🔧 Troubleshooting

### "yt-dlp not found"
Install it: `pip install yt-dlp`

### "Permission denied" on downloads folder
Change the download path using option `6` in the menu

### Downloads marked as complete but file missing
The program tracks attempts, not success. Check the console output for actual download errors.

### JSON format error
Delete `downloads.json` and restart the program to create a fresh file

## 🚧 Roadmap

- [ ] Video download support with format selection
- [ ] Playlist support
- [ ] Download queue management
- [ ] Progress bars
- [ ] Batch link import
- [ ] Download history export

## 📝 License

Free to use and modify. Use responsibly and respect copyright laws.

## 🙏 Credits

Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features.

---

**Made simple. Kept simple. Works simply.** ✨
