# Working notes (for Claude sessions)

Site: Cloudflare Worker serving `public/` (thequietclimbsg.com + pocketlocalsg.com). Push to `main` deploys automatically.
- Check deploy: `gh api repos/thequietclimb/thequietclimb/commits/<sha>/check-runs`
- If the build doesn't trigger, push an empty commit.
- Cloudflare limit is ~25 MB per file.

## Trading page (thequietclimbsg.com/trading)
- Data: `public/trading.json`; screenshots in `public/img/trading/YYYY-MM-DD-*.jpg`.
- Kev sends FXIFY + 5ers MT5 screenshots daily. Add an entry with progress figures and the lesson in Kev's own words.
- Story card: `tools/story/make_story2.py`.

## Pocket Local pages
- `public/pocketlocal.html`, guides in `public/guides/` (built via `tools/build_guides.py` from `tools/guides.json`), sitemap `public/pl-sitemap.xml`.

## Video tools
- `tools/video/`, `tools/posts/`, music in `tools/music/` (pl_music.mp3 for Pocket Local).

## Getting files to Higgsfield / TikTok
- Direct media upload is blocked. Workaround: commit the file to `public/img/`, wait for deploy, `media_import_url`, then `git rm` it. Videos work; images import as PNG (TikTok rejects), so for photos use `media_upload_widget` and let Kev pick files.

## Posting tips (browser pane on Kev's Mac)
- IG web: crop to 4:5 for carousels, 9:16 for Reels; turn on the AI label when visuals are AI.
- XHS (creator.rednote.com): put the caret at the end before typing #tags; pick each tag from the dropdown.
- FB group comments: shift+Enter for line breaks, Enter posts.
