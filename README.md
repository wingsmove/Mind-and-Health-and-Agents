# Mind-and-Health-and-Agents

A mental-health & wellness assistant powered by a two-agent pipeline built on the
OpenAI Agents SDK. The user describes their situation, and the backend runs two
agents in sequence:

1. **Message Agent** — replies to the user with helpful, non-diagnostic guidance
   (may use screening forms such as PHQ-9, GAD-7, PHQ-2).
2. **Report Agent** — using the user input and the Message Agent's reply,
   generates a Markdown research report intended for researchers/professionals
   (should not be shown to the user but shown on the frontend for now for debug usage).

> Disclaimer: this project does not provide medical diagnosis or treatment.

## Tech Stack

- **Frontend**: React 19 + TypeScript + Vite (`frontend/`)
- **Backend**: Python + FastAPI + OpenAI Agents SDK (`backend/`)

## Project Structure

```
.
├── frontend/            # React frontend
│   ├── src/
│   │   ├── api.ts       # Backend base URL + response types
│   │   ├── App.tsx      # Chat UI: input, agent reply, and report
│   │   └── App.css
│   └── vite.config.ts
└── backend/             # FastAPI backend
    ├── app/
    │   ├── main.py               # App entry point (CORS, routes, /analyze)
    │   ├── schemas.py            # AnalyzeRequest / AnalyzeResponse models
    │   ├── core/config.py        # Environment variable configuration
    │   ├── api/routes.py         # Routes (/api/health, /api/info)
    │   └── services/agent.py     # Agent framework + message/report agents
    ├── requirements.txt
    └── .env.example
```

## API

- `POST /analyze` — body `{ "message": "..." }`, returns `{ "content": "...", "report": "..." }`
- `GET /api/health` — health check
- `GET /api/info` — basic runtime info (app name, model, whether the key is configured)

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env   # then fill in OPENAI_API_KEY (and optionally OPENAI_MODEL)

# Start the dev server (defaults to http://127.0.0.1:8000)
uvicorn app.main:app --reload
```

API docs: after starting, visit http://127.0.0.1:8000/docs

### Environment variables (`backend/.env`)

- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (default `gpt-4o-mini`)
- `OPENAI_BASE_URL` (optional, for proxies / OpenAI-compatible providers)
- `CORS_ORIGINS` (comma-separated allowed frontend origins)

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev   # defaults to http://localhost:5173 (falls back to 5174 if in use)
```

The frontend calls the backend directly at `http://localhost:8000` (see `src/api.ts`),
so the backend must allow the frontend's origin via `CORS_ORIGINS`. If Vite starts on
a different port (e.g. 5174), add that origin to `CORS_ORIGINS`.

## Notes

- `/analyze` runs two agents sequentially, so a single request can take a while
  depending on the model.
- Never commit `backend/.env`; it contains your real API key (it is already
  covered by `.gitignore`).

## Running Sample

Not in MD but the actual output is in MarkDown
input
```
I feel like my friends are talking bad about me when I am not around. It always feel like they do not like me in some ways. I think they play with me only because I kept asking them to play with me.
I cannot be stable for even one day thinking about this. I am too afraid of talking to them at some point thinking that they may just leave me behind.
Sometimes they do not reply my message I will be anxious for hours.
```

message
```
I’m really sorry you’re going through this. Feeling like people might not like you—or worrying they’re talking about you—can be exhausting and make everyday things (like sending a message) feel scary. Your feelings make sense given what you’ve described.

What you shared suggests a strong fear of being rejected or left out and a lot of anxiety when there’s uncertainty (like delayed replies). We can work on both the thoughts and the habits that keep the worry going—without trying to diagnose anything.

What might help right now

Ground your body when the anxiety spikes:
Box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s. Repeat 3–5 times.
5-4-3-2-1 grounding: name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.
Create a message-checking plan:
Pick set check-in times (e.g., every 45–60 minutes) instead of constantly checking.
If you want to follow up, wait one full check interval before sending a brief, kind follow-up.
Reduce reassurance-seeking that backfires:
Try inviting friends once, then give it space. Repeated asks can increase your anxiety and pressure the friendship.
Diversify your activities (games, hobbies, exercise, chat with another friend) so your mood isn’t tied to one response.
Test your thoughts gently:
Ask: “What’s the evidence they don’t like me?” vs. “What are 3 neutral reasons they might be slow to reply?” (busy, low battery, social energy, time zones, notifications off).
Write the worry: “They must be talking bad about me.” Then write a balanced alternative: “I don’t have direct proof; delays often mean nothing. If there’s an issue, I can handle a calm conversation.”
A simple way to bring it up (if you feel ready):
“Hey, I value our friendship. Sometimes I overthink when I don’t hear back and get anxious. If you’re busy, no worries—just letting you know I might be slower to double-text while I work on it.”
Pick one person you trust first. Keep it short and non-accusatory.
Track patterns for 1 week:
When the fear hits, note: trigger, worry (exact words), anxiety 0–10, what you did, outcome. This helps you see what helps and what keeps the cycle going.
A few gentle questions (answer any you want)

Has anything specific happened that makes you think they’re talking badly about you (e.g., you overheard something, changes in behavior), or is it mostly a feeling?
When messages go unanswered, roughly how long are the gaps that trigger hours of anxiety?
Is there one friend you feel safer checking in with?
How is this affecting sleep, appetite, school/work, or concentration?
Quick anxiety check (GAD-7) if you want Over the last 2 weeks, how often have you been bothered by the following? Reply with: Not at all / Several days / More than half the days / Nearly every day. I’ll total it for you.

Feeling nervous, anxious, or on edge
Not being able to stop or control worrying
Worrying too much about different things
Trouble relaxing
Being so restless that it’s hard to sit still
Becoming easily annoyed or irritable
Feeling afraid as if something awful might happen
If you’d like, we can also track how much this interferes with daily life (not at all, somewhat, very, extremely).

When to consider extra support

If this fear is disrupting sleep, school/work, or keeps you from socializing, talking with a licensed mental health professional can really help you build skills for uncertainty and rejection fears. If you want, I can help you prepare what to say at an appointment.
If you ever feel unsafe or have thoughts about harming yourself, seek immediate help (local emergency number, crisis line, or someone you trust). You deserve support right away.
You’re not alone in feeling this way, and it’s workable. If you share a bit more (or complete the GAD-7 above), I’ll tailor the next steps specifically to you.
```

Report
```
Report on User Interaction
User's situation
The user reports persistent worry that friends speak negatively about them when they are absent and may not truly like them.
They believe friends only engage with them because the user repeatedly initiates (“kept asking them to play with me”).
They feel unable to remain emotionally stable for even one day due to these concerns.
They fear initiating conversations with friends, worried they may be abandoned or left behind.
When messages go unanswered, they experience hours of anxiety.
No mention of self-harm, suicidal ideation, or aggression.
No mention of prior diagnosis, treatment, or medication.
User's symptoms
Anxiety related to interpersonal contexts (especially uncertainty around messaging and social inclusion).
Rumination and intrusive worry about friends’ opinions and potential rejection.
Intolerance of uncertainty (strong distress when replies are delayed).
Cognitive patterns consistent with:
Mind-reading (assuming others’ negative thoughts without direct evidence).
Catastrophizing (fear of being abandoned/left behind).
Personalization (interpreting neutral events—delayed replies—as evidence of rejection).
Behavioral patterns:
Reassurance-seeking and repeated invitations to engage with friends.
Message checking and heightened monitoring of friends’ responses.
Avoidance of initiating contact at times due to fear of rejection.
Functional impact: hours-long anxiety episodes; difficulty maintaining emotional stability day-to-day.
User's existing diagnosis
None reported.
User's current treatment
None reported (no mention of therapy, counseling, or medication).
Results from forms completed (based on user’s input)
Note: The user did not provide time-bound ratings (e.g., “over the last 2 weeks”). Items below are inferred as present/absent only where supported by the user’s statements. Frequency and severity cannot be scored reliably from the available information.

GAD-7 (screening inference; not scored):

Feeling nervous, anxious, or on edge: Present (anxious for hours when messages are unanswered; “cannot be stable for even one day thinking about this”).
Not being able to stop or control worrying: Present (ongoing, persistent worry and rumination).
Worrying too much about different things: Unclear (worry appears focused on friendships and responses).
Trouble relaxing: Not clearly reported.
Being so restless that it’s hard to sit still: Not reported.
Becoming easily annoyed or irritable: Not reported.
Feeling afraid as if something awful might happen: Present (fear friends will leave/abandon them).
Functional interference: Present (hours of anxiety, avoidance/tension in initiating communication).
Total score: Not calculated due to missing frequency/timeframe data.
PHQ-2 (depression screen; inference only):

Little interest or pleasure in doing things: Not reported.
Feeling down, depressed, or hopeless: Not reported.
Result: Insufficient information; no depression symptoms explicitly endorsed.
Safety screen (informal):

Suicidal ideation, self-harm, or harm to others: Not reported.
Conclusion based on the user’s situation
The presentation is characterized by persistent, situationally triggered anxiety centered on fear of social rejection and negative evaluation from friends, with substantial worry during periods of uncertainty (e.g., delayed messages). There is evidence of cognitive distortions (mind-reading, catastrophizing) and behaviors (reassurance-seeking, avoidance, frequent checking) that likely maintain the anxiety cycle.
There is functional impact (hours-long anxiety, difficulty initiating conversations, feeling emotionally unstable daily).
No current indicators of imminent risk were disclosed. No prior diagnosis or treatment reported.
While this pattern aligns with features commonly seen in social/interpersonal anxiety and rejection sensitivity, no diagnosis is made here. Further assessment by a licensed mental health professional would clarify severity, duration, and comorbidities, and help plan care.
Your thoughts and reasoning process
I mapped the user’s statements to common anxiety features: persistent worry, intolerance of uncertainty, and fear of rejection. The content is narrowly focused on friendships and messaging, which suggests a specific interpersonal trigger rather than generalized worry about many domains.
The user’s line “cannot be stable for even one day” suggests frequent symptoms, yet without a 2-week timeframe or frequency anchors I avoided scoring standardized tools.
Cognitive features (mind-reading, catastrophizing, personalization) are inferred from the user assuming friends talk badly about them despite limited evidence and expecting abandonment from delayed replies.
Behavioral maintenance factors include repeated invitations (reassurance-seeking) and frequent message monitoring, which can temporarily reduce anxiety but increase preoccupation over time.
Differential considerations (descriptive only): features overlap with social anxiety phenomena and rejection sensitivity; there is no indication of psychotic-level conviction (the user frames worries as fears, not fixed beliefs). No depressive symptoms are clearly endorsed. Further exploration would include sleep, appetite, concentration, history of bullying/rejection, attachment experiences, and broader functioning.
Risk level of the user's situation
Acute risk (self-harm/suicide): Low based on current information (no ideation reported).
Psychosocial risk: Mild-to-moderate due to functional interference (hours of anxiety, avoidance, potential strain on friendships).
Recommendation for safety: Continue monitoring for any emergence of self-harm thoughts; none reported at present.
Why the user may be behaving this way and seeking help
Likely strong need for belonging and fear of rejection, potentially shaped by prior experiences (unknown) and maintained by digital communication ambiguity (delayed replies).
Reassurance-seeking and frequent checking can inadvertently increase salience of social cues and strengthen anxious interpretations.
The user may be seeking validation, practical strategies to cope with uncertainty, and a way to communicate needs to friends without damaging relationships.
Thoughts about the other agent’s response
Strengths:
Empathic, validating tone that normalizes the user’s experience.
Practical CBT-informed strategies: grounding, structured message-checking, reducing reassurance-seeking, cognitive balancing, and behavioral experiments (bringing it up calmly).
Encourages data gathering (tracking triggers, anxiety ratings, outcomes) to identify maintaining factors.
Asks clarifying questions and offers a standardized screen (GAD-7) without diagnosing.
Includes brief safety guidance if the user feels unsafe.
Potential gaps or considerations:
The plan includes many steps; some users may benefit from prioritizing 1–2 skills first (e.g., grounding + message-checking schedule) to reduce overwhelm.
It could explicitly note that delayed replies are common and often unrelated to relationship quality, to further normalize uncertainty.
Additional gentle exploration might include history of social rejection/bullying, sleep and concentration impacts, and supports outside this friend group to diversify social reinforcement.
The GAD-7 invitation is appropriate, though the user’s original message lacks timeframe; following up to obtain frequency data would allow accurate scoring.
Overall assessment: The response is high-quality, aligned with evidence-based self-help principles, and appropriately avoids diagnosis while offering actionable, compassionate guidance.
```

## Develop notes
This is my second time trying Full-Stack programming.
This time I only used a generated framework and done most of the work by myself.
AI models only helped with debugging in this project.
I want to make this project a more useful one and hopefully start doing an actual research based on this topic.
