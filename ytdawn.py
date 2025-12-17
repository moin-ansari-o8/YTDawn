#!/usr/bin/env python3
"""
YTDawn - YouTube Audio/Video Downloader
Simple and clean downloader using yt-dlp with minimal console output
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


class YTDawn:
    def __init__(self, json_file="downloads.json"):
        self.json_file = json_file
        self.data = self.load_json()

    def load_json(self):
        """Load the downloads JSON file or create new one"""
        if not os.path.exists(self.json_file):
            default_data = {
                "audio": {"links": []},
                "video": {"links": []},
                "meta": {"default-path": "downloads"},
            }
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2)
            return default_data

        with open(self.json_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self):
        """Save data back to JSON file"""
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_download_path(self):
        """Get the download path from meta or use default"""
        default_path = self.data.get("meta", {}).get("default-path", "downloads")
        Path(default_path).mkdir(parents=True, exist_ok=True)
        return default_path

    def find_link(self, link, media_type):
        """Find a link in the specified media type list"""
        links = self.data.get(media_type, {}).get("links", [])
        for i, item in enumerate(links):
            if item.get("link") == link:
                return i, item
        return None, None

    def add_or_update_link(self, link, media_type):
        """Add new link or update existing one"""
        idx, existing = self.find_link(link, media_type)

        if existing is None:
            # Add new link
            new_entry = {
                "link": link,
                "title": "",
                "is_downloaded": False,
                "format": "opus" if media_type == "audio" else "",
                "path": "",
            }
            self.data[media_type]["links"].append(new_entry)
            self.save_json()
            return new_entry
        else:
            return existing

    def normalize_links(self, media_type):
        """Normalize manually added links - ensure all fields exist"""
        links = self.data.get(media_type, {}).get("links", [])
        modified = False

        for item in links:
            # Ensure required fields exist
            if "link" not in item:
                continue  # Skip invalid entries

            if "is_downloaded" not in item:
                item["is_downloaded"] = False
                modified = True

            if "format" not in item:
                item["format"] = "opus" if media_type == "audio" else ""
                modified = True

            if "path" not in item:
                item["path"] = ""
                modified = True

        if modified:
            self.save_json()

        return modified

    def get_video_title(self, link):
        """Fetch video title from YouTube using yt-dlp (silent, fast)"""
        try:
            cmd = [
                "yt-dlp",
                "--get-title",
                "--no-warnings",
                "--no-playlist",
                "--skip-download",
                link,
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10,  # 10 second timeout
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            title = result.stdout.strip()
            return title if title else ""
        except subprocess.TimeoutExpired:
            return "[Timeout]"
        except:
            return ""

    def get_video_metadata(self, link):
        """Fetch title and filesize from YouTube (silent)"""
        try:
            cmd = [
                "yt-dlp",
                "--no-warnings",
                "--no-playlist",
                "--dump-json",
                "-f",
                "bestaudio",
                link,
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=15,  # 15 second timeout
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            data = json.loads(result.stdout.strip())
            title = data.get("title", "")
            filesize = data.get("filesize") or data.get("filesize_approx", 0)
            return title, filesize
        except subprocess.TimeoutExpired:
            return "[Timeout]", 0
        except:
            return "", 0

    def scan_downloaded_files(self, download_path):
        """Scan directory and return set of normalized filenames"""
        if not os.path.exists(download_path):
            return set()

        downloaded = set()
        for file in Path(download_path).glob("*.opus"):
            # Normalize filename: remove extension and common yt-dlp suffixes
            name = file.stem
            # Remove [videoID] patterns
            name = re.sub(r"\s*\[[\w-]+\]\s*$", "", name)
            downloaded.add(name.lower().strip())

        return downloaded

    def is_already_downloaded(self, title, downloaded_files):
        """Check if a title matches any downloaded file"""
        if not title:
            return False
        normalized_title = title.lower().strip()
        # Also check partial matches (first 30 chars)
        title_prefix = (
            normalized_title[:30] if len(normalized_title) > 30 else normalized_title
        )

        for downloaded in downloaded_files:
            if normalized_title == downloaded or title_prefix in downloaded:
                return True
        return False

    def format_size(self, size_bytes):
        """Format bytes to MB or GB"""
        if size_bytes == 0:
            return "Unknown"
        mb = size_bytes / (1024 * 1024)
        if mb >= 1024:
            return f"{mb / 1024:.1f} GB"
        return f"{mb:.1f} MB"

    def download_audio(self, link, title=""):
        """Download audio using yt-dlp with minimal output"""
        download_path = self.get_download_path()

        # Display title (truncated to 30 chars)
        display_title = title if title else link
        if len(display_title) > 30:
            display_title = display_title[:30] + "..."
        print(f"\n▶ {display_title}")

        cmd = [
            "yt-dlp",
            "-x",
            "-f",
            "bestaudio",
            "--audio-format",
            "opus",
            "-P",
            download_path,
            "--no-warnings",
            "--no-playlist",
            "--quiet",
            "--progress",
            "--newline",
            link,
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )

            last_progress = ""
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue

                # Filter progress lines
                if "[download]" in line and "%" in line:
                    # Extract percentage
                    match = re.search(r"(\d+(?:\.\d+)?%)", line)
                    if match:
                        progress = match.group(1)
                        if progress != last_progress:
                            # Simple progress bar
                            percent = float(progress.rstrip("%"))
                            bar_length = 30
                            filled = int(bar_length * percent / 100)
                            bar = "█" * filled + "░" * (bar_length - filled)
                            print(f"\r[{bar}] {progress}", end="", flush=True)
                            last_progress = progress

            process.wait()

            if process.returncode == 0:
                print(f"\r[{'█' * 30}] 100%")
                print("Completed\n")
                return True, title
            else:
                print(f"\nFailed\n")
                return False, ""

        except FileNotFoundError:
            print("❌ Error: yt-dlp not found. Please install it first:")
            print("   pip install yt-dlp")
            return False, ""
        except Exception as e:
            print(f"\nFailed: {str(e)}\n")
            return False, ""

    def download_video(self, link):
        """Download video - Currently not implemented"""
        print("📹 Video download is not yet implemented.")
        print("   Currently only audio downloads are supported.")
        return False, ""

    def normalize_links(self, media_type):
        """Normalize manually added links - ensure all fields exist"""
        links = self.data.get(media_type, {}).get("links", [])
        modified = False

        for item in links:
            # Ensure required fields exist
            if "link" not in item:
                continue  # Skip invalid entries

            if "is_downloaded" not in item:
                item["is_downloaded"] = False
                modified = True

            if "format" not in item:
                item["format"] = "opus" if media_type == "audio" else ""
                modified = True

            if "path" not in item:
                item["path"] = ""
                modified = True

            # Title will be fetched automatically when downloading
            if "title" not in item:
                item["title"] = ""
                modified = True

        if modified:
            self.save_json()

        return modified

    def process_downloads(self, media_type):
        """Process all pending downloads with clean preview and download phases"""

        while True:  # Loop to check for new links
            # Reload JSON to get any newly added links
            self.data = self.load_json()
            links = self.data.get(media_type, {}).get("links", [])

            if not links:
                print(f"\n📭 No {media_type} links found in {self.json_file}")
                return

            # Normalize manually added links
            self.normalize_links(media_type)

            # Get download path and scan for existing files
            download_path = self.get_download_path()
            downloaded_files = self.scan_downloaded_files(download_path)

            # Collect pending links with metadata
            pending_items = []

            # Count total pending items for progress indication
            pending_count = sum(
                1 for item in links if not item.get("is_downloaded", False)
            )

            if pending_count > 0:
                print(f"\n⏳ Fetching metadata for {pending_count} link(s)...")

            processed = 0
            for item in links:
                # Skip if already marked as downloaded in JSON
                if item.get("is_downloaded", False):
                    continue

                link = item["link"]
                processed += 1

                # Show progress
                print(
                    f"\r  [{processed}/{pending_count}] Checking...", end="", flush=True
                )

                # Fetch metadata silently
                title, filesize = self.get_video_metadata(link)

                # Update title in JSON if empty
                if title and not item.get("title"):
                    idx, _ = self.find_link(link, media_type)
                    if idx is not None:
                        self.data[media_type]["links"][idx]["title"] = title

                # Check if file already exists in directory
                if self.is_already_downloaded(title, downloaded_files):
                    # Mark as downloaded in JSON
                    idx, _ = self.find_link(link, media_type)
                    if idx is not None:
                        self.data[media_type]["links"][idx]["is_downloaded"] = True
                        self.data[media_type]["links"][idx]["title"] = title
                        self.data[media_type]["links"][idx]["path"] = download_path
                    continue

                pending_items.append(
                    {
                        "item": item,
                        "link": link,
                        "title": title if title else link,
                        "filesize": filesize,
                    }
                )

            # Save any updates (files detected as already downloaded and titles updated)
            self.save_json()

            # Clear progress line
            if pending_count > 0:
                print("\r" + " " * 50 + "\r", end="", flush=True)

            if not pending_items:
                print(f"✅ All {media_type} links are already downloaded!")
                return  # Exit the loop - no more pending downloads

            # ===== PREVIEW PHASE =====
            print("\nPending downloads:")
            print("-" * 50)

            total_size = 0
            max_title_len = 30  # Maximum title display length

            for item in pending_items:
                title = item["title"]
                size = item["filesize"]

                # Truncate long titles
                if len(title) > max_title_len:
                    display_title = title[: max_title_len - 3] + "..."
                else:
                    display_title = title

                size_str = self.format_size(size)

                # Right-align size in a 12-char field
                print(f"{display_title:<30} {size_str:>12}")
                total_size += size

            print("-" * 50)
            print(f"Total: {len(pending_items)} files | {self.format_size(total_size)}")

            # ===== DOWNLOAD PHASE =====
            print("\nDownloading:")

            for item in pending_items:
                link = item["link"]
                title = item["title"]

                if media_type == "audio":
                    success, fetched_title = self.download_audio(link, title)
                elif media_type == "video":
                    success, fetched_title = self.download_video(link)
                else:
                    success, fetched_title = False, ""

                if success:
                    # Update the link status
                    idx, _ = self.find_link(link, media_type)
                    if idx is not None:
                        self.data[media_type]["links"][idx]["is_downloaded"] = True
                        self.data[media_type]["links"][idx]["path"] = download_path
                        if fetched_title:
                            self.data[media_type]["links"][idx]["title"] = fetched_title
                        elif title and title != link:
                            self.data[media_type]["links"][idx]["title"] = title
                        self.save_json()

            print("\n✅ Batch completed! Checking for new links...")
            # Loop continues - will reload JSON and check for new links
        """Interactive link addition"""
        print(f"\n➕ Add new {media_type} link")
        link = input("Enter URL (or 'back' to return): ").strip()

        if link.lower() == "back" or not link:
            return

        self.add_or_update_link(link, media_type)
        print(f"✅ Added {media_type} link: {link}")

    def show_menu(self):
        """Show main menu"""
        while True:
            print("\n" + "=" * 60)
            print("🎬 YTDawn - YouTube Downloader")
            print("=" * 60)
            print("\n📂 Current download folder:", self.get_download_path())

            audio_count = len(self.data.get("audio", {}).get("links", []))
            video_count = len(self.data.get("video", {}).get("links", []))

            audio_pending = len(
                [
                    l
                    for l in self.data.get("audio", {}).get("links", [])
                    if not l.get("is_downloaded", False)
                ]
            )
            video_pending = len(
                [
                    l
                    for l in self.data.get("video", {}).get("links", [])
                    if not l.get("is_downloaded", False)
                ]
            )

            print(f"🎵 Audio links: {audio_count} total, {audio_pending} pending")
            print(f"📹 Video links: {video_count} total, {video_pending} pending")
            print(f"\n💡 Tip: You can manually add links to {self.json_file}")
            print('   Just add: {{"link": "YOUR_URL"}} and run option 1 or 2')

            print("\n" + "-" * 60)
            print("1. Download Audio")
            print("2. Download Video (not implemented)")
            print("3. Add Audio Link")
            print("4. Add Video Link")
            print("5. View All Links")
            print("6. Change Download Path")
            print("7. Exit")
            print("-" * 60)

            choice = input("\nSelect option (1-7): ").strip()

            if choice == "1":
                self.process_downloads("audio")
            elif choice == "2":
                self.process_downloads("video")
            elif choice == "3":
                self.add_link_interactive("audio")
            elif choice == "4":
                self.add_link_interactive("video")
            elif choice == "5":
                self.view_all_links()
            elif choice == "6":
                self.change_download_path()
            elif choice == "7":
                print("\n👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid option. Please try again.")

    def view_all_links(self):
        """Display all links from JSON"""
        print("\n" + "=" * 60)
        print("📋 All Links")
        print("=" * 60)

        # First, check and fetch missing titles
        for media_type in ["audio", "video"]:
            links = self.data.get(media_type, {}).get("links", [])
            missing_titles = [item for item in links if not item.get("title")]

            if missing_titles:
                print(
                    f"\n⏳ Fetching {len(missing_titles)} missing {media_type} title(s)..."
                )
                for idx, item in enumerate(missing_titles, 1):
                    print(
                        f"\r  [{idx}/{len(missing_titles)}] Fetching...",
                        end="",
                        flush=True,
                    )

                    # Use get_video_title with timeout (faster than get_video_metadata)
                    title = self.get_video_title(item["link"])

                    if title and title != "[Timeout]":
                        # Find and update the item in the main list
                        link_idx, _ = self.find_link(item["link"], media_type)
                        if link_idx is not None:
                            self.data[media_type]["links"][link_idx]["title"] = title
                    elif title == "[Timeout]":
                        # Mark timeout but continue
                        link_idx, _ = self.find_link(item["link"], media_type)
                        if link_idx is not None:
                            self.data[media_type]["links"][link_idx][
                                "title"
                            ] = "[Failed to fetch]"

                print("\r" + " " * 50 + "\r", end="", flush=True)
                self.save_json()
                print(f"✅ Updated {len(missing_titles)} title(s)")

        # Now display all links with titles
        for media_type in ["audio", "video"]:
            links = self.data.get(media_type, {}).get("links", [])
            print(f"\n{media_type.upper()} ({len(links)} links):")

            if not links:
                print("  (none)")
            else:
                for i, item in enumerate(links, 1):
                    status = "✅" if item.get("is_downloaded", False) else "⏳"
                    title = item.get("title", "")
                    # Truncate long titles to 40 chars for viewing
                    if title:
                        display_title = (
                            title if len(title) <= 40 else title[:40] + "..."
                        )
                        print(f"  {i}. {status} {display_title}")
                    else:
                        print(f"  {i}. {status} {item['link']}")

    def change_download_path(self):
        """Change the default download path"""
        current = self.get_download_path()
        print(f"\n📂 Current path: {current}")
        new_path = input(
            "Enter new download path (or press Enter to keep current): "
        ).strip()

        if new_path:
            self.data["meta"]["default-path"] = new_path
            self.save_json()
            Path(new_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ Download path updated to: {new_path}")


def main():
    """Main entry point"""
    try:
        print("🚀 Starting YTDawn...")

        # Check if yt-dlp is installed
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            print("\n❌ Error: yt-dlp is not installed!")
            print("\n📦 To install yt-dlp, run:")
            print("   pip install yt-dlp")
            print("\n   Or visit: https://github.com/yt-dlp/yt-dlp")
            sys.exit(1)
        except subprocess.CalledProcessError:
            pass  # yt-dlp exists but returned non-zero, that's ok

        app = YTDawn()
        app.show_menu()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
