# 🎬 YTDawn - YouTube Audio/Video Downloader

Fast, clean YouTube downloader with CLI support and smart caching.

## ✨ Features

- 🎵 Download high-quality audio (OPUS format)
- 🖥️ **CLI commands** - Run from anywhere on your system
- ⚡ **Smart caching** - Fetches metadata once, uses forever
- 🔄 **Auto-resume** - Continue interrupted downloads
- 📊 **Live progress** - Real-time speed and progress bar
- 🔁 **Auto-reload** - Checks for new links after each batch
- 📋 Clean console output with minimal noise

## 📦 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add to PATH (Optional - for CLI use):**
   - Add `W:\workplace-1\ytdawn` to your system PATH
   - Now you can run `ytdawn` from anywhere!

## 🚀 Quick Start

### CLI Mode (Fast & Easy)

```bash
# List all audio links
ytdawn -la

# Download all pending audio
ytdawn -da

# Add a new audio link
ytdawn -aa "https://youtube.com/watch?v=xxxxx"

# Show help
ytdawn --help
```

### Interactive Menu

```bash
ytdawn
```

## 📝 CLI Commands

| Command | Description |
|---------|-------------|
| `ytdawn -la` | List all audio links |
| `ytdawn -lv` | List all video links |
| `ytdawn -da` | Download all pending audio |
| `ytdawn -dv` | Download all pending video |
| `ytdawn -aa <URL>` | Add audio link |
| `ytdawn -av <URL>` | Add video link |

## 💡 Simple Usage

**Method 1: Direct JSON Edit (Bulk)**

1. Open `downloads.json`
2. Add links:
   ```json
   {
     "audio": {
       "links": [
         {"link": "https://youtube.com/watch?v=xxxxx"}
       ]
     }
   }
   ```
3. Run: `ytdawn -da`

**Method 2: CLI Command**

```bash
ytdawn -aa "https://youtube.com/watch?v=xxxxx"
ytdawn -da
```
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

## 🎯 How It Works

1. **Smart Caching**: Fetches metadata once, stores in JSON
2. **Auto-Resume**: Interrupted downloads continue from where they stopped
3. **Batch Processing**: Downloads all pending links automatically
4. **Auto-Reload**: Checks for new links after completing batch
5. **Clean Output**: Minimal console noise with live progress

## 📊 Console Output

```
⏳ Fetching metadata for 2 link(s)...
  [2/2] Fetching...

Pending downloads:
--------------------------------------------------
Ghibli Chill – Studying, co...              106.9 MB
Lo-fi Beats for Deep Focus                   72.1 MB
--------------------------------------------------
Total: 2 files | 179.0 MB

Downloading:

▶ Ghibli Chill – Studying, co...
[██████████████████░░░░░░░░░░] 65.3% @ 3.2 MiB/s
```

## 📁 File Structure

```
ytdawn/
├── ytdawn.py           # Main program
├── ytdawn.bat          # Windows batch launcher
├── downloads.json      # Metadata cache & tracking
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## 🔧 Troubleshooting

**yt-dlp not found**  
→ `pip install yt-dlp`

**"No audio links found" when using CLI**  
→ Make sure you're running from correct directory or PATH is set

**Downloads won't resume**  
→ Already handled! `--continue` flag auto-resumes partial files

## 💡 Pro Tips

- Add links to JSON while downloader is running - it auto-reloads after each batch
- Metadata is cached - second run is instant, no re-fetching
- Press Ctrl+C to stop gracefully - downloads resume next time
- Use `-da` for hands-free batch downloading

## 📝 License

Free to use. Respect copyright laws.

## 🙏 Credits

Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

**Fast. Clean. Simple.** ⚡
