# Kuruc - Chat App

This was my maturita (final school) project, a chat web app built in PHP with a MySQL backend and Tailwind for styling. It supports login/register, friends, 1:1 chats, group chats, and a small photo gallery with likes.

Test login for the demo instance: `12341234` / `12341234`

## Features

- Register/login with hashed passwords (bcrypt via `password_hash`)
- Friend system: send requests, confirm/decline, friend list
- 1:1 private chats
- Group chats with multiple members
- Profile pictures/avatars, uploaded via the app
- A small photo gallery where users can upload photos and like each other's posts
- Search for other users

## How it's structured

`php/` has all the backend logic, each feature is its own endpoint file (`addfriend.php`, `sendGroupmessage.php`, `upload.php`, etc.) that the frontend calls via fetch. `db.php` handles the database connection, `functions.php` and the `.inc.php` files hold shared logic for login/register/logout.

`src/js/` has the frontend JS that talks to those PHP endpoints and updates the chat UI without reloading the page.

Styling is Tailwind, compiled from `src/input.css` to `src/output.css`.

## Database schema

`schema.sql` has the table structure (no real data, just for reference). Rough overview of how the tables connect:

- `user` - accounts, nickname + hashed password + avatar
- `friends` - accepted friendships (stored both directions)
- `friend_requests` - pending/confirmed/rejected friend requests
- `chat` - a 1:1 chat between two nicknames
- `message` - messages inside a `chat`
- `group_chat` - a group chat, just an id + name
- `group_chat_member` - which nicknames belong to which group chat
- `group_chat_message` - messages inside a group chat
- `photos` - uploaded gallery photos
- `photo_likes` - who liked which photo

## Note on security

The original version of this had the database password hardcoded directly in `db.php`. I've since moved it to environment variables (see `.env.example`) - if you're running this yourself, set `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` before connecting to a real database.

## Screenshots
you can find screenshot in this repository .


## What I'd do differently now

Looking back at it, a few things I'd change if I rebuilt this: use prepared statements consistently everywhere (some endpoints already do this, some don't), pull secrets out of code from the start instead of after the fact, and probably move to a proper framework instead of one PHP file per action.
