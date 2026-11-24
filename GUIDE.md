# Build a Duck$y feature from your phone 🦆📱

Duck$y is our Discord bot. You can teach it new tricks (a `/roast` command, a trivia game, a
daily duck fact, a leaderboard) **without knowing how to code**. You describe your idea to an
AI agent on your phone. It writes the code and opens a pull request ("PR"), which is a request
for Nick to add your change. Nick approves it, and it's live in Discord a few minutes later.

No computer, no copy-pasting code, no terminal. Bookmark this page.

---

## Contents

1. [One-time setup](#1-one-time-setup-10-minutes)
2. [Pick an idea](#2-pick-an-idea)
3. [Build it](#3-build-it)
4. [After the PR is open](#4-after-the-pr-is-open)
5. [Picking it up later, or changing a live feature](#5-picking-it-up-later-or-changing-a-live-feature)
6. [What features can and can't do](#6-what-features-can-and-cant-do)
7. [Problems and fixes](#7-problems-and-fixes)
8. [Words you'll see](#8-words-youll-see)

---

## 1. One-time setup (10 minutes)

**1. Get a GitHub account.** Sign up free at [github.com/signup](https://github.com/signup).
GitHub is where the bot's code lives. The GitHub app (iPhone or Android) is handy but optional.

**2. Send Nick your GitHub username.** This is the only thing you ever need to ask him for. He
adds you to the project, and you get an invite by email and in the GitHub app. Tap
**Accept invitation**, or open
[github.com/nick-gerrard/ducksbucksbot/invitations](https://github.com/nick-gerrard/ducksbucksbot/invitations).

**3. Pick your AI agent and connect it to GitHub.** Any one of these works:

| Agent | Where | Plan | Connect it |
|---|---|---|---|
| **Claude Code** | Claude app → **Code** | Claude Pro or Max | Tap **Code**, connect GitHub, choose `nick-gerrard/ducksbucksbot` |
| **Codex** | ChatGPT app → **Codex** | ChatGPT Plus or higher | Open Codex, connect GitHub, choose `nick-gerrard/ducksbucksbot` |
| **Jules** (Google) | [jules.google](https://jules.google) in your phone's browser | Has a free tier | Sign in with Google, connect GitHub, choose `nick-gerrard/ducksbucksbot` |

If the repo doesn't show up when connecting, make sure you accepted Nick's invite (step 2),
then try again. If GitHub says the app needs approval, tell Nick: it's a one-click approval
on his side.

You're set up. From here on, you never need Nick except to approve your PRs.

---

## 2. Pick an idea

- **Your own:** anything fun that starts with a slash command, a button, or a daily post.
  Examples: `/magic8`, `/roast @someone`, `/trivia` with answer buttons, "who owes the most
  DucksBucks", or a daily duck fact at 9am.
- **From the idea board:** browse the
  [Ideas list](https://github.com/nick-gerrard/ducksbucksbot/issues?q=is%3Aopen+label%3Aidea)
  and comment "I'm on it" so nobody doubles up. Add your own ideas there too
  (**New issue → Feature idea**).

---

## 3. Build it

1. In your agent, start a **new task** on `nick-gerrard/ducksbucksbot` (branch `main`).
2. Send it this, with your idea at the end:

   > Read AI_START.md in this repo and follow it exactly. I'm not a programmer and I'm on my
   > phone. When it's ready, open a pull request. My idea: **(describe your idea here)**

3. Answer its questions. It'll suggest names and jokes; you're the boss.
4. **Open the PR** when it's done. Most agents do this themselves. If not:
   - **Claude Code:** tap **Create PR** on the changes card.
   - **Codex:** tap **Create PR**.
   - **Jules:** tap **Publish branch**, then pick **Publish PR** from the menu next to it.

That's it. You'll get a link to your PR.

---

## 4. After the PR is open

Your PR page shows two automatic checks at the bottom:

| Check | What it means |
|---|---|
| 🦆 **Safety** | The feature only does allowed things. It comments in plain English. |
| **test** | The bot still starts, and all the commands are valid. |

- **Both green ✅:** Nick gets notified, looks it over, and approves. Then it merges, and a few
  minutes later you can type `/` in Discord and see your command. It can take a minute or two
  to show up the first time.
  - Tip: tap **Enable auto-merge** on your PR. It then merges by itself the moment Nick
    approves.
- **Something red ❌:** go back to the same task in your agent and say:
  > The checks on my pull request failed. Look at the PR's checks and the 🦆 Safety comment,
  > fix it, and push the fix to the same pull request.

  If it says it can't see them, tap **Details** next to the red check (or open the 🦆 comment)
  and send it a screenshot. The checks re-run by themselves after every fix.
- **Nick left a comment:** same thing. Tell your agent what he asked for, or send a screenshot.

---

## 5. Picking it up later, or changing a live feature

Nothing gets lost. Open PRs stay open until they're merged or closed, and your agent keeps
its task history.

- **Continue an unfinished PR:** open the old task in your agent and keep chatting. If it's
  gone, start a new task and say:
  > Read AI_START.md and follow it. Continue my open pull request "(its title)": check out its
  > branch, then (what you want changed). Push to the same pull request.
- **Change a feature that's already live:** start a new task (on `main`) and say:
  > Read AI_START.md and follow it. Change the existing feature `ducksy/features/(name).py` so
  > that (what you want). Open a pull request.
- **Coming back after weeks away:** just start a new task. It always starts from the latest
  version of everything, including everyone else's features.

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
- **Read normal chat messages.** Duck$y only sees slash commands, buttons, and schedules, so
  no "reply whenever someone says Vegas", no auto-reactions, and no "type your answer in
  chat" games. The closest you can get is a command (`/vegas @someone`) or buttons.
- Ping @everyone or roles, kick or ban people, or make the bot leave
- Change the bot's core, other people's features, or anything outside `ducksy/features/`

Want something on the "can't" list? Post it as an idea and tag Nick. He can add a safe
building block (for example, "fetch a random GIF"), and then anyone can use it.

House rule: keep it fun for the whole group. Nothing hateful, sexual, or about people outside
the group.

---

## 7. Problems and fixes

| Problem | Fix |
|---|---|
| The agent can't find the repo | Accept Nick's invite (section 1, step 2), then reconnect GitHub in the agent. |
| The agent wants you to install things or use a terminal | Say: "I'm on my phone. Follow AI_START.md: one file in `ducksy/features/`, then open a PR." |
| Safety says a file is "outside the features folder" | Say: "Undo every change outside `ducksy/features/` and push again." |
| test says "two features use the same command name" | Ask the agent to rename your command. |
| test says "needs a short description" | Ask the agent to add or shorten the command's description. |
| The checks show "Approve and run" or just wait | Rare for collaborators. Nudge Nick in Discord. |
| Your command doesn't show in Discord after the merge | Wait 5 minutes and restart Discord. Still missing? Tell Nick. |
| The command says "Quack! Something went wrong" | It crashed. Tell Nick which command and what you typed; he can see the error and pass it to you for your agent. |
| Can Duck$y reply automatically when someone says a word? | No: it can't read chat (section 6). Make it a command instead, like `/vegas @someone`. |
| You messed everything up | Close the PR (bottom of the PR page) and start a new task. Nothing breaks: only Nick can put things live. |

---

## 8. Words you'll see

- **Repo:** the project's folder of code on GitHub.
- **Branch:** a separate copy of the code where your change lives until it's merged.
- **Pull request (PR):** "Nick, please add my change." It shows the change, the checks, and
  comments.
- **Merge:** your change joins the live bot. It's in Discord a few minutes later.
- **Check:** an automatic test that runs on every PR.
- **Collaborator:** someone Nick has added to the project, so their agent can open PRs.
- **Slash command:** a Discord command starting with `/`.
