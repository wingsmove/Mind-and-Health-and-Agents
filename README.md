# Mind-and-Health-and-Agents

A mental-health & wellness assistant powered by a two-agent pipeline built on the
OpenAI Agents SDK. The user describes their situation, and the backend runs two
agents in sequence:

1. **Message Agent** — replies to the user with helpful, non-diagnostic guidance
2. **Report Agent** — using the user input and the Message Agent's reply,
   generates a Markdown research report intended for researchers/professionals.

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

Not in MarkDown here but the actual output is in MarkDown
Input
```
I feel like my friends are talking bad about me when I am not around. It always feel like they do not like me in some ways. I think they play with me only because I kept asking them to play with me.
I cannot be stable for even one day thinking about this. I am too afraid of talking to them at some point thinking that they may just leave me behind.
Sometimes they do not reply my message I will be anxious for hours.
```

Message
```
Response
I’m really sorry you’re going through this. Feeling like friends might be talking about you or might leave you out can be exhausting and make every unread message feel scary. You’re not alone in this, and there are practical ways to steady yourself and check what’s actually happening without beating yourself up.

Possible interpretation
It sounds like anxiety and “mind‑reading” (assuming you know what others think) are creating a loop: you worry → you seek signs (like delayed replies) → the worry grows. That doesn’t mean your feelings aren’t valid—just that the conclusions might be possibilities, not facts.
Rejection sensitivity could also be part of this: when you care about people, small signals (like a slow response) can feel huge. That’s common and workable.
Practical next steps
In-the-moment calm when messages don’t come

Try the “physiological sigh” 5 times: inhale normally, quick top‑off inhale, then a long slow exhale. It can lower the body’s alarm response in under a minute.
5‑4‑3‑2‑1 grounding: name 5 things you see, 4 feel, 3 hear, 2 smell, 1 taste.
Label it: “I’m feeling anxious and my brain is predicting rejection.” Simply naming it often turns the volume down.
Untangling thoughts

Write a quick thought note: Situation (no reply for 2 hours) → Automatic thought (“They don’t like me”) → Feelings → Evidence for/against → A balanced thought (“Delays happen; if there’s an issue, I can handle a direct convo.”).
Add “I’m having the thought that…” in front of scary beliefs. It reminds you thoughts are not facts.
Messaging plan to reduce spiral

Set a short “no‑check” window after sending (e.g., 15–20 minutes) and do a small task (shower, short walk, one chore). Use a timer so you’re not white‑knuckling your phone.
Batch checks (e.g., on the hour) and mute just the notification preview for the anxious chat so pings don’t trigger a surge.
If read receipts/typing indicators make it worse, consider turning them off.
Reality-testing your friendships (gentle, not punitive)

For the next 1–2 weeks, jot down:
Who initiates, roughly how often
Average reply times
Positive moments (jokes, invites, warmth) This helps you see patterns over impressions.
Try one small experiment: give a little more space for a few days while you plan your own activities. See if anyone reaches out on their own. Do this while keeping your life full so you’re not just waiting.
Opening a kind, low-pressure conversation

With one trusted friend: “Hey, I value our friendship and I’ve been overthinking lately. If I ever do something that bugs you, I’d want to know. If not, I just wanted to be honest that slow replies can spin me out, and I’m working on it—no pressure to text faster.”
If you worry you’re pushing to hang out: “I love spending time together, but I don’t want to overwhelm you. It’s totally okay to say no—no hard feelings.”
Self‑support while you wait

Do one mood‑safe activity list you can pick from when anxiety spikes (music, a short game, stretching, a show you’ve seen before).
Offer yourself the same tone you’d use with a friend: “It’s hard to not know. I’m doing my best. I can handle this.”
When to seek additional help
If this level of anxiety lasts most days for more than a couple of weeks, disrupts sleep/school/work, or causes panic attacks, a mental health professional could help with tools like CBT or ACT to reduce rumination and fear of rejection.
If you ever feel in immediate danger or have thoughts of harming yourself, seek urgent help. In the United States, you can call or text 988 for the Suicide & Crisis Lifeline, or use 988lifeline.org. If you can, also reach out to someone you trust nearby.
Limitations
I’m not a therapist and I don’t know the full picture of your friendships. I can’t tell from here what your friends think; these are general strategies to reduce anxiety and get clearer information kindly. If you want to share more context, I’m here to listen, but you don’t have to.
```

Report
```
Interaction Research Report
User's situation
Explicit information:
The user feels their friends talk badly about them when they are not present.
The user feels their friends do not like them in some ways.
The user believes friends play with them only because the user keeps asking.
The user reports being unable to feel “stable” for even one day due to these thoughts.
The user is afraid to talk to friends, fearing they may be left behind.
When friends do not reply to messages, the user feels anxious for hours.
Supported interpretation:
The user appears distressed about peer relationships and experiences prolonged anxiety linked to messaging delays and fear of rejection. Rationale: repeated statements about anxiety for hours, fear of being left behind, and ongoing instability.
Research hypothesis:
The user might be experiencing rumination about social acceptance and interpreting ambiguous cues (e.g., delayed replies) as negative. This cannot be confirmed without further data.
Unknown:
Duration beyond “cannot be stable for even one day.”
Context of friendships, frequency of interactions, cultural/communication norms in the friend group.
Any prior mental-health history, diagnoses, or supports.
User's reported symptoms or concerns
Explicit information:
Anxiety for hours when messages are not returned.
Fear that friends will abandon or exclude the user.
Persistent preoccupation causing day-to-day instability.
Supported interpretation:
Possible cognitive patterns such as “mind reading” or catastrophizing about peers’ intentions, inferred from statements like “I feel like my friends are talking bad about me” and “they do not like me.” Evidence is linguistic; not diagnostic.
Unknown:
Sleep, appetite, concentration, academic/work impact, panic symptoms, or safety concerns.
Existing diagnosis
Not provided.
Current treatment
Not provided.
Interaction style
Supported interpretation:
Indirect help-seeking: the user does not ask a direct question but shares emotional concerns, possibly seeking validation or understanding. Evidence: descriptive narrative without an explicit request.
Emotion-forward, first-person language showing vulnerability and worry. Evidence: “I feel like…,” “I am too afraid…,” “I will be anxious for hours.”
Ambiguity about intentions: no stated goal or desired outcome from the AI beyond sharing distress.
Possible reasons for interacting with the AI
Hypothesis: Seeking validation/reassurance that their fears about friends may be unfounded.

Supporting evidence: Emphasis on others “talking bad,” not liking them, and anxiety when messages are delayed; disclosure of fear without a direct solution request.
Alternative explanation: The user may be seeking concrete strategies to reduce anxiety rather than reassurance.
Confidence: Medium.
Hypothesis: Looking for low-risk, anonymous space to process fears about social rejection.

Supporting evidence: Willingness to state “too afraid of talking to them,” suggesting AI may be a safer outlet.
Alternative explanation: The user might simply be venting momentarily and not specifically choosing AI for anonymity.
Confidence: Medium.
Hypothesis: Desire for practical guidance on managing message-related anxiety and perceived social exclusion.

Supporting evidence: Specific trigger described (unreplied messages causing hours of anxiety), which often prompts requests for coping strategies.
Alternative explanation: The user may only want the AI to confirm whether their friends are “bad” friends rather than to receive coping skills.
Confidence: Low–medium.
Safety review
Provisional classification: Possible elevated concern.
Supporting evidence: Reports of sustained anxiety (“for hours”), ongoing instability (“cannot be stable for even one day”), fear-driven avoidance of communication. These indicate noteworthy distress and possible functional impact.
Missing information: Presence/absence of self-harm thoughts, duration in weeks/months, sleep or work/school impairment, substance use, social supports, any acute interpersonal conflict.
Confidence: Medium.
Review of the other agent's response
Summary of its approach
Supported interpretation:
The agent acknowledges distress, normalizes the experience, and frames the issue with cognitive patterns (e.g., “mind-reading,” “rejection sensitivity”) as possibilities rather than facts.
Provides stepwise coping strategies (breathing, grounding, labeling thoughts), cognitive restructuring tools, behavioral plans to reduce compulsive checking, gentle reality-testing via tracking, and scripts for low-pressure communication with a trusted friend.
Includes criteria for when to seek additional help and provides crisis resources (988 in the U.S.).
States limitations and avoids claiming to know the friends’ perspectives.
What it did well
Supported interpretation:
Empathic, nonjudgmental validation of feelings.
Offers a coherent mix of immediate coping (breathing/grounding), cognitive strategies (“I’m having the thought that…”), and behavioral experiments (message-check windows, logs).
Encourages respectful, low-stakes communication with friends, aligning with the user’s fear of being overwhelming.
Provides clear “when to seek help” thresholds and crisis information, showing safety awareness.
Uses cautious language (“could,” “might”) rather than definitive diagnoses.
Unsupported assumptions or problems
Supported interpretation:
The term “rejection sensitivity” is introduced as a possibility; while framed cautiously, it edges toward pathologizing without user-provided history.
The physiological claim that a specific breathing technique lowers alarm “in under a minute” may be overconfident without citations; still low risk but somewhat specific.
Crisis resource (988) is U.S.-specific; the user’s location is not explicitly stated in the conversation, so geographic fit is uncertain.
The volume of strategies may be cognitively demanding for a highly anxious user; the response could risk overwhelm without prioritization.
Unknown:
Whether the user prefers brief validation versus a long skill list.
Cultural or linguistic factors that might affect the suitability of direct scripts with friends.
Appropriateness for the user's apparent needs
Supported interpretation:
Largely appropriate: It matches an anxiety-driven, reassurance-seeking narrative with validation plus practical tools.
The inclusion of behavioral experiments and communication scripts is responsive to fears about being left out and over-requesting time with friends.
A brief prioritization (e.g., “try one or two steps first”) might have further reduced potential overwhelm.
Research hypotheses
If the user implements scheduled message-checking and disables anxiety-amplifying cues (read receipts/typing indicators), reported anxiety duration after unanswered messages will decrease. Data needed: baseline and follow-up logs of check frequency, anxiety ratings, and response times.
Using a brief thought record may reduce the certainty of negative interpretations about friends. Data needed: pre/post belief strength ratings and frequency of catastrophic thoughts.
A gentle, scripted conversation with one trusted friend may improve perceived relationship security. Data needed: reports of conversation outcomes and subsequent contact patterns/initiations.
Tracking actual initiations and positive interactions will reduce discrepancy between impressions and observed behavior. Data needed: 1–2 weeks of structured interaction logs compared to the user’s prior subjective ratings.
Limitations
Single-message snapshot; cannot infer diagnosis, chronicity, or broader psychosocial context.
No confirmation of safety status or functional impairment beyond self-reported anxiety and instability.
Friendship dynamics are unobserved; AI cannot verify whether negative beliefs are accurate.
Cultural norms for messaging and social engagement vary; applicability of guidance may differ without contextual data.
```

## Develop notes
This is my second time trying Full-Stack programming.
This time I only used a generated framework and done most of the work by myself.
AI models only helped with debugging in this project.
I want to make this project a more useful one and hopefully start doing an actual research based on this topic.
