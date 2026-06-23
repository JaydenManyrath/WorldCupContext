# WorldCupContext
A CLI tool that generates hype and context for World Cup matches based on your favorite teams. Given a match date, it identifies which of your favorite teams are playing, pulls match data from a football API, generates an AI-powered pre-match breakdown, and surfaces YouTube highlight videos from previous encounters.
Status: Work in Progress — Core structure and scaffolding are in place. Several features are planned but not yet implemented (see Roadmap below).

Features
Favorite team tracking — On first run, prompts you to enter your favorite national teams and saves them to a local SQLite database.
Match lookup by date — Query upcoming or past World Cup matches for a specific date.
Smart match selection — If one of your favorites is playing, it surfaces that match. If multiple favorites are playing, it lets you pick. If none are playing, the AI selects the most interesting match for you.
AI match hype — Uses Google Gemini to generate a pundit-style pre-match summary with historical context, rivalry background, and players to watch.
YouTube highlights — Finds the most recent highlight video of the two teams facing off via the YouTube Data API.
Result caching — Stores match data locally to avoid redundant API calls.
