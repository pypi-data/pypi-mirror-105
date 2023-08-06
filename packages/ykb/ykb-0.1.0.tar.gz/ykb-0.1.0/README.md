# `ykb` - Your Knowledge Base

`ykb` is the brand new (!! :-)) note taking tool for the command line.
It allows to take either quick or elaborated notes by editing the text with the default editor. It uses the editor specified by the `EDITOR` environment variable.
The note can be in free form, although the preferred format should be Markdown.
Notes are saved by default in the directory `~/.ykb/`. Every new note is saved in its own file. The filename is a random unique ID (UUID).

Notes are organized in *notebooks*. A notebook is a directory with two sub-directory: `notes` contains the active notes, while `archive` contains the archived notes.
Notes can be archived and unarchived. `ykb`s commands normally operate on active notes only, unless otherwise specified using dedicated flags.

In-text tags are supported in the form `@tag`.

`ykb` is written in Python. While the language does not lead to the fastest program, it allows a really quick implementation of the functionalities.

## Add a new note

Command:

    ykb new

Adds a new note. Opens the default editor to allow the editing of the text.

## Edit an existing note

Command:

    ykb edit ID

Opens the default editor to edit the note specified by the unique ID.
The ID can be either the full UUID or a shorter beginning part of the ID, as long as the ID does not match with more than one full UUID.

For example:

    ykb edit 6b

will open a note with full ID equal to (e.g.) `6b63d178-4a57-4bd5-b990-c8d510c25a72` (notice the two matching characters at the beginning of the full ID), as long as there isn't another ID beginning with `6b`.

## List all notes

Command:

    ykb list

List all the notes in the default note directory, listing the abbreviated ID and the first line of text (truncated if too long).

## Search in notes

Command:

    ykb search string

Search `string` in all the notes. Shows colored results.

## List all tags

Command:

    ykb tags

List all the tags found in the notes with their frequencies.

## Show one or more notes

Command:

    ykb show ID

Displays all the notes whose UUID starts with ID. 

# Future works, TODOs (in no specific ordering)

[X] Add search command
[X] Add cat/show command (support to cat multiple notes if nore than one is matching)
[ ] Add configuration options (e.g., default directory)
[ ] Add per-note encryption
[X] Add custom sorting of tags (alphabetically or by frequency)
[ ] Add global flag to specify custom note dir (notebook)
[ ] Add `archive`/`unarchive` support
[ ] Add `move` command to move notes in another notebook
[ ] Add `link` command to add a double-link between two notes
[ ] Add `status` feature in the preamble? E.g., for TODOs
[ ] Add a title, somehow (e.g., first line with `# ...`)

## Internal refactoring

[X] Revamp the logic to parse the header and the body (split into reusable functions)
[ ] Introduce some basic classes (for single notes and a collection of notes)

