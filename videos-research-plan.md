# IndyDevDan Course Structuring Plan

## Goal
Use public IndyDevDan content + tactical-agentic-coding landing-page content to derive a practical curriculum outline for internal dev-team training and Zach's spin-up product.

## Recommended pipeline

1. **Harvest metadata (URLs + titles + publish dates + durations + descriptions).**
   - YouTube channel: `https://www.youtube.com/@indydevdan`
   - Landing/curriculum context: `https://agenticengineer.com/tactical-agentic-coding`

2. **Transcript-first extraction (preferred, cheapest):**
   - Prefer official captions/transcript for each target video.
   - Store raw transcript + normalized text + timestamps.

3. **Optional MP4 archival (when transcripts are weak):**
   - Download MP4s only as fallback.
   - Transcribe with Whisper/VTT and align timestamps.

4. **Use `/process-meeting`-style processing pattern for content segmentation:**
   - Parse each transcript into:
     - concepts
     - learning objectives
     - tools/frameworks mentioned
     - sequence dependencies
     - implementation recipes
   - Build “module -> lesson -> checkpoint” hierarchy.

5. **Synthesize Course Blueprint:**
   - Beginner -> Intermediate -> Advanced progression
   - Build 1) internal team curriculum, 2) client-delivery roadmap
   - Map each module to deliverables + practical exercises.

## Why this works
- Transcript-first is much cheaper/faster than full video downloads.
- MP4 fallback is only needed for videos with poor/blocked captions.
- Reuses proven pattern from `/process-meeting` (segment, extract actionables, generate structured artifacts).

## Suggested artifact outputs
- `courses/indydevdan-raw-index.json` (video list + metadata)
- `courses/indydevdan-transcripts/*.txt`
- `courses/indydevdan-transcripts/*.vtt`
- `courses/module-blueprint.md`
- `courses/learning-path.csv` (week-by-week)

## Next action
Create a practical script bundle in one repo so you can run:

```bash
./scripts/course-miner/run-course-research.sh
```

It will:
- gather videos
- fetch transcripts
- generate module draft
- export to markdown for Zach pitch deck / internal strategy docs.
