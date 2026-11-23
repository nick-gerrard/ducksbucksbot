# Build a Duck$y feature from your phone 🦆📱

Duck$y is our Discord bot. You can teach it new tricks (a `/roast` command, a trivia game, a
daily duck fact, a leaderboard) **without knowing how to code**. An AI writes the code, you
send it to Nick with a couple of taps, and once he merges it, it's live in Discord a few
minutes later.

This guide has everything you need, start to finish. Bookmark it.

---

## Contents

1. [One-time setup](#1-one-time-setup-5-minutes)
2. [Pick an idea](#2-pick-an-idea)
3. [Build it: Path A (AI does the GitHub part)](#3a-path-a-the-ai-does-the-github-part)
4. [Build it: Path B (any AI app + GitHub's website)](#3b-path-b-any-ai-app--githubs-website)
5. [After you open the pull request](#4-after-you-open-the-pull-request)
6. [Changing your feature or picking it up later](#5-changing-your-feature-or-picking-it-up-later)
7. [What features can and can't do](#6-what-features-can-and-cant-do)
8. [Problems and fixes](#7-problems-and-fixes)
9. [Words you'll see](#8-words-youll-see)

---

## 1. One-time setup (5 minutes)

1. **Make a GitHub account** at [github.com/signup](https://github.com/signup), if you don't
   have one. It's free. GitHub is where the bot's code lives.
2. **Optional: install the GitHub app** (iPhone or Android). Everything also works in your
   phone's browser.
3. **Choose how you'll build** (you can switch any time):

   | You have… | Use |
   |---|---|
   | The **Claude** app on a paid plan (Claude Code) | Path A |
   | **ChatGPT** on a paid plan (Codex) | Path A |
   | **Gemini**, and you're up for trying Google's **Jules** (jules.google) | Path A |
   | Any AI app, free or paid: Claude, ChatGPT, Gemini… | Path B (always works) |

   Not sure? **Use Path B.** It's a few more taps, but it works with anything.

That's all. You don't need permission from Nick, a password, or a computer.

---

## 2. Pick an idea

- **Your own idea:** anything fun that starts with a slash command, a button, or a daily
  post. Examples: `/magic8`, `/roast @someone`, `/trivia` with answer buttons, "who owes the
  most DucksBucks", a countdown to the next big game, a daily duck fact at 9am.
- **Grab one from the idea board:** the [Ideas list](https://github.com/nick-gerrard/ducksbucksbot/issues?q=is%3Aopen+label%3Aidea).
  Comment "I'm on it" so nobody else starts the same one. Post your own ideas there too
  (**New issue → Feature idea**).

---

## 3A. Path A: the AI does the GitHub part

**First time only:**

1. Open [github.com/nick-gerrard/ducksbucksbot](https://github.com/nick-gerrard/ducksbucksbot)
   and tap **Fork**, then **Create fork**. You now have your own copy, called "your fork".
2. Connect your AI to GitHub and give it access to your fork:
   - **Claude app:** open **Code**, connect GitHub, and choose your `ducksbucksbot` fork.
   - **ChatGPT:** open **Codex**, connect GitHub, and choose your fork.
   - **Jules:** sign in at jules.google, connect GitHub, and choose your fork.

**Every time:**

1. On your fork's GitHub page, tap **Sync fork → Update branch** if it says you're behind.
   This gets everyone's latest features.
2. Start a new task in your AI on your fork and paste this, with your idea at the end:

   > Read AI_START.md in this repo and follow it exactly. I'm not a programmer, so keep it
   > simple. My idea: **(describe your idea here)**

3. Answer its questions. When it's done, it'll either open the pull request itself or tell you
   it pushed a branch.
4. If it only pushed a branch: open your fork on GitHub, tap **Contribute → Open pull
   request**, and make sure it says `base repository: nick-gerrard/ducksbucksbot`, `base:
   main`. Fill in the template and tap **Create pull request**.

Then go to [step 4](#4-after-you-open-the-pull-request).

---

## 3B. Path B: any AI app + GitHub's website

**1. Brief the AI.** Start a new chat and paste:

> Read https://raw.githubusercontent.com/nick-gerrard/ducksbucksbot/main/AI_START.md and follow
> it exactly. You're the chat assistant without GitHub access. I'm not a programmer and I'm on
> my phone. My idea: **(describe your idea here)**

If the AI says it can't open links, open
[AI_START.md](https://raw.githubusercontent.com/nick-gerrard/ducksbucksbot/main/AI_START.md),
select all, copy, paste it into the chat, and add "My idea: …" at the end.

**2. Chat until it's right.** Answer its questions. At the end it gives you three things: a
**file name**, the **code**, and **pull request text**.

**3. Add the file on GitHub:**

1. Open [the features folder](https://github.com/nick-gerrard/ducksbucksbot/tree/main/ducksy/features).
2. Tap **Add file → Create new file**. On a phone browser, if you don't see it, tap the **⋯**
   menu or switch to the desktop site.
3. GitHub says you're making changes in a project you don't have write access to and that it
   will make a fork for you. That's expected.
4. In the name box, type the file name: just the part after `ducksy/features/`, e.g.
   `magic_8_ball.py`.
5. Paste the code into the big box: use the AI's copy button, then long-press → Paste.
6. Tap **Commit changes…** (or **Propose changes**) → **Propose changes**.
7. On the next screen, tap **Create pull request**. Paste the AI's pull request text and tap
   **Create pull request** again.

---

## 4. After you open the pull request

Your pull request ("PR") page shows checks at the bottom:

| Check | What it means |
|---|---|
| 🦆 **Safety** | Makes sure the feature only does allowed things. It comments in plain English. |
| **test** | Makes sure the bot still starts and all the commands are valid. |

- **Both green ✅:** you're done. Nick gets notified, has a look, and merges it. A few minutes
  later, type `/` in Discord and your command shows up. (It can take a minute or two to
  appear the first time.)
- **"Approve and run" / waiting:** GitHub makes Nick press a button before tests run for some
  new accounts. Give him a nudge in Discord if it sits there.
- **Something red ❌:**
  1. For Safety: copy the 🦆 comment. For test: tap **Details** next to it and copy the red
     error lines.
  2. Paste it into the same AI chat with "This check failed, please fix it."
  3. Update the PR: in Path A, ask the agent to push the fix. In Path B, see
     [Changing your feature](#5-changing-your-feature-or-picking-it-up-later).
  4. The checks run again by themselves.
- Nick might leave a comment asking for a change. Treat it the same way: paste it to your AI.

---

## 5. Changing your feature or picking it up later

Your work never disappears: an open pull request stays open until it's merged or closed, and
your fork keeps everything.

**Pick up an unfinished PR (both paths):** open your pull request on GitHub (on your profile
or the repo's **Pull requests** tab). To get the AI back up to speed, paste:

> Read AI_START.md in nick-gerrard/ducksbucksbot. I'm continuing my pull request. Here's my
> current file: (paste it) and here's what I want to change: …

**Update an open PR:**
- **Path A:** open the same task in your agent, or start a new one on the same branch, and
  ask for the change.
- **Path B:** in your PR, tap **Files changed**, then **⋯** next to your file → **Edit file**.
  Paste the new full version and tap **Commit changes**.

**Change a feature that's already live:** treat it like a new feature, but tell the AI
"change the existing file `ducksy/features/<name>.py`". Paste the current version from GitHub.
- **Path B:** open the file on GitHub, tap the ✏️ pencil, paste the new version, then
  **Propose changes → Create pull request**.
- **Path A:** sync your fork first, then ask the agent.

**Coming back weeks later:** sync your fork first (Path A), or just start fresh from the main
repo (Path B). Everything else in this guide stays the same.

---

## 6. What features can and can't do

**Can:**
- Slash commands with options: pick a person, a number, or from a list
- Buttons, menus, and fancy "embed" messages
- Randomness, dates and times, math, text games
- Remember things between restarts: scores, streaks, counters
- Read today's games and open bets from the DucksBucks site
- Post on a schedule in the main channel

**Can't** (the safety check blocks these):
- Visit other websites, so no GIF search, weather, or live scores (yet)
- Read or write files, or run programs
- Read normal chat messages (Duck$y only sees slash commands and buttons)
- Ping @everyone or roles, kick or ban people, or make the bot leave
- Change the bot's core, other people's features, or anything outside `ducksy/features/`

Want something on the "can't" list? Post it as an idea and tag Nick: he can add a safe
building block (for example, "fetch a random GIF"), and then anyone can use it.

House rule: keep it fun for the whole group. Nothing hateful, sexual, or about people outside
the group.

---

## 7. Problems and fixes

| Problem | Fix |
|---|---|
| The AI wants me to install Python, use a terminal, or edit other files | Say: "I'm on my phone. Follow AI_START.md: one file in `ducksy/features/`, nothing else." |
| The AI wrote "…rest of the code stays the same" | Say: "Give me the complete file, every line." |
| Safety says a file is "outside the features folder" | Your PR changed another file by accident. Ask the AI which ones, then delete those changes in **Files changed**, or start over with only your feature file. |
| test says "two features use the same command name" | Ask the AI to rename your command. |
| test says "needs a short description" | Ask the AI to add or shorten the command's description. |
| I can't find **Add file** on my phone | Use the browser's **Request desktop site** option, or the **⋯** menu on the folder page. |
| My command doesn't show in Discord after merge | Wait 5 minutes, then restart Discord. Still missing? Tell Nick. |
| The command says "Quack! Something went wrong" | It crashed. Tell your AI exactly what you typed and what happened, and ask Nick for the error (he can see the logs). |
| I messed everything up | Close the PR (bottom of the PR page) and start again. Nothing breaks. |

---

## 8. Words you'll see

- **Repo:** the project's folder of code on GitHub.
- **Fork:** your personal copy of the repo. Your changes go there first.
- **Branch:** a separate line of changes inside a repo, so work-in-progress doesn't mix with
  the live version.
- **Pull request (PR):** "Nick, please add my changes." It shows the changes, the checks, and
  the comments.
- **Merge:** Nick accepting a PR. It's live a few minutes later.
- **Sync fork:** bring your copy up to date with everyone else's latest work.
- **Check:** an automatic test that runs on every PR.
- **Slash command:** a command you type in Discord starting with `/`.
