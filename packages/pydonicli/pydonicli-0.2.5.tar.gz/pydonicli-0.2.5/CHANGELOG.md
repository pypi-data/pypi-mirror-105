# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
PR Title Template: Release YYYYMMDD.VVV

## V.V.V (YYYY-MM-DD)
### Added
### Modified
### Addressed
### Fixed
### Removed
-->

## 0.2.5 (2021-05-12)
### Added
### Modified
- Requirements
### Addressed
### Fixed
### Removed
- .github directory

## 0.2.4 (2021-05-11)
### Added
- Integration with `pip-tools`
### Modified
- gitignore
- Command `split_batch_exported_timelapse` from submodule opsys to photo
- Module setup
- Changelog versioning history
### Addressed
### Fixed
- Backend postgres database failed command logging
### Removed

## 0.2.3 (2021-04-13)
### Added
### Modified
### Addressed
### Fixed
### Removed
- Removed gitignored files from git

## 0.2.2 (2021-04-13)
### Added
- Various 'common' modules in photo workflow
- Ellipsis handling in iMessage workflow
### Modified
- Code aesthetic harmony among click command python code
- Minor folder structure updates
- Renamed Photo 'workflow_elt' to 'workflow'
- iMessage workflow assess untracked/modified/removed files
- Aesthetic updates to dashboard, and several new visualizations
### Addressed
### Fixed
- CLI app fixed for major/minor command compatibility (i.e. if command = `imessage workflow-elt`, then `major` = `imessage`, and `minor` = `workflow-elt`
### Removed
- Click commands designed to be held privately

## 0.2.1 (2021-04-02)
### Added
- `rsync` option for backup
- Began photo workflow. Intiial views set up
- Moved `pydoni.scripts` to this repo
### Modified
- Higher degree of completion for `imessage_current` schema
- iMessage Dashboard
  - Tiled layout
  - Target Contact dashboard redesign
- Updated license year
### Addressed
### Fixed
- Historical table bug in iMessage workflow
- Incorrect FFMPEG call in compress()
### Removed

## 0.2.0 (2021-01-24)
### Added
- iMessage dashboard
- Support for in-band, manually maintained tables
- Option `--no-startup-message`
- Support for importing table objects in workflow code from 'staged_table_objects.py'
- `ColorTag` object to handle colorized prefix tags printed to console in Workflow verbose mode
- Greatly simplified code and added clarifications to verbose logging in command `data backup`
- Debug mode for `data backup`
- Debug mode for `notes ph_refresh`
### Modified
- iMessage Workflow ELT Pydonicli backend command logging compatibility
- iMessage Workflow ELT enhanced verbosity
- Split Postgres schemas: one for architectural chat.db tables, and the other for user tables and views
### Addressed
### Fixed
- iMessage Workflow ELT bug fixes with `--full-refresh` off
### Removed
- iMessage `page_count_vw`

## 0.1.9 (2020-12-27)
### Added
- Workflow ELT Pipeline
- CLI subgroups
- SQL view definitions and integration into pipeline
### Modified
### Addressed
### Fixed
### Removed

## 0.1.7 (2020-10-21)
### Added
- PH Refresh commmand
### Addressed
- #19
### Fixed
- Minor verbose bug fixes
### Removed

## 0.1.6 (2020-10-10)
### Added
- pbar support to Verbose
- Info, warn, error verbose output
### Modified
- App logo
- Updated license year
- Version notation system {year}{month}{day}.{major}{minor}
### Addressed
- #16
### Fixed
- Pydoni backend registration
### Removed

## 0.1.5 (2020-05-23)
### Added
- Pydoni-CLI backend postgres integration for all commands. Records starting arguments and results for every command
- Verbose class in global app functions. Accounts for `verbose` parameter in each command
- Uniform verbose logging behavior to console
- Error handling functionality in DB backend. If a command errors out, the error will be caught, recorded in the postgres backend table, then raised in console
### Modified
- Slight logo redesign
### Addressed
### Fixed
- Minor bug fixes and cosmetic code improvements
### Removed

## 0.1.4 (2020-05-01)
### Added
- data-git-sync now accepts 'ignore' parameter
- Logo to README
### Modified
- Allow copy pasting multiline entry in add-moments-entry (#9)
- Commandline call now built as list, not string
- Support for click 'multiple' parameters
- Vastly simplified data-backup
### Addressed
- #5
- #6
- #9
### Fixed
### Removed

## 0.1.3 (2020-05-06)
### Added
- Catch error in add-events-log and print to console if command fails for any reason
### Modified
- Revamped app command parameters to be their own class as requested in #2
- add-moments-log renamed to add-events-log
- Refreshed requirements
### Fixed
### Removed

## 0.1.2 (2020-04-29)
### Added
- Commands:
    - data-pg-dump
    - os-open-most-recent-file-in-dir
- One-click app (ignored)
- Pipeline for interacting with Postgres app backend on exit using `atexit` module
### Modified
### Fixed
- `sys.path.append` for `pydoni` module
- Accounted for `\x08` separator in data-pg-dump
### Removed

## 0.1.1 (2020-04-14)
### Added
### Modified
- Name in setup.py changed to "pydonicli" from "pydoni-apps"
### Fixed
- Lots of bug fixes
### Removed

## 0.1.0 (2020-03-14)
### Added
- Initial release!
- Commands
    - apple-make-meeting-entry
    - audio-compress-file
    - audio-join-files
    - audio-m4a-to-mp3
    - data-add-moments-entry
    - data-backup
    - data-git-sync
    - movie-refresh-imdb-table
    - photo-instagram-hashtags
    - photo-rename-mediafile
    - photo-website-extract-image-titles
    - run-app
### Modified
### Fixed
### Removed
