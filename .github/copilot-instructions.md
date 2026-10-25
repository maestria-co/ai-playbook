# Global Task Tracking

Before processing any request, check for active tasks:

1. Read `~/.copilot/active-tasks.json` directly (load file and parse JSON)
2. Filter tasks where `repo` matches current repository root
3. If user mentioned a task ID (e.g., "mje0006") → auto-resume that task
4. If user said "show active" → list all active tasks for current repo
5. Otherwise → proceed normally

Active tasks are stored globally in `~/.copilot/active-tasks.json` and filtered by repository path.
Hooks automatically update timestamps and archive old tasks, but Manager makes all task selection decisions.

# Core Values (always apply)

Every suggestion must follow Maestria's core values in `CORE_VALUES.md`. If one would be violated, tell the user before proceeding.

- **Free and Frugal** — We operate at the free tier at all costs. We only spend when it is our last option.
- **Off The Shelf** — We only build product solutions. We use off the shelf products for our non-product needs.
- **Cruise Control** — We believe in automated solutions to get the job done. People are there to ensure the automation is monitored and corrected.
- **Bury The Treasure** — We believe in protecting people's information.
