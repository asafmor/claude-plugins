---
name: tbe-travel-risk
description: Assess tick-borne encephalitis (TBE) risk for a specific trip, hike, trek, campsite, or outdoor itinerary. Use when a user asks whether TBE is a concern at a destination, whether TBE vaccination is worth considering, or how season, altitude, route, habitat, and time outdoors affect risk. Gather only missing trip facts, research the most authoritative current national/regional surveillance sources, cross-check with ECDC/CDC/WHO, and return an evidence-based qualitative assessment without inventing a precise infection probability.
compatibility: Requires current web access. Works best when the agent can search the web and inspect maps, route pages, PDFs, or GPX files when supplied.
metadata:
  version: "1.0"
  domain: "travel-health"
---

# TBE Travel Risk

Assess the risk of tick-borne encephalitis (TBE) for a specific traveler and itinerary. The result must be grounded in current, location-specific epidemiology and the user's actual exposure pattern.

This skill is for travel-risk assessment and vaccination decision support. It is not for diagnosing symptoms after a tick bite or replacing a clinician when a medical contraindication, pregnancy, immune condition, prior severe vaccine reaction, or other individual medical issue is relevant.

## Core principles

1. **Assess the route, not merely the country.** TBE transmission is highly focal. Country-level labels can hide major differences between neighboring districts, valleys, or mountain areas.
2. **Prefer local public-health evidence.** Use the national or regional public-health authority for the destination whenever it publishes TBE surveillance, risk maps, vaccination areas, or case data.
3. **Use current data.** Search for the newest available risk map, surveillance report, alert, or annual data. State the date of the evidence used.
4. **Separate disease activity from traveler exposure.** A highly endemic district does not imply the same risk for an urban visitor and a multi-day hiker in woodland.
5. **Do not derive a fake probability.** Human case incidence is affected by vaccination coverage, surveillance quality, local behavior, diagnostic practice, and the size of the population denominator. Do not convert population incidence directly into a traveler's chance of infection.
6. **Tick presence is not TBE-virus presence.** Vector-distribution maps are supporting evidence only. Never conclude that TBE is endemic merely because *Ixodes ricinus* or another competent vector is present.
7. **Altitude modifies risk; it is not a safety cutoff.** Do not claim that a route is safe simply because it is above 1,000, 1,500, or 2,000 m. Evaluate habitat and locally documented transmission. CDC has documented recognized TBE foci at elevations up to about 2,100 m; verify the latest guidance at execution time.
8. **Season must be local.** Use locally documented transmission/tick season when available. If none is available, the broad European April-November transmission season may be used as a fallback and must be labeled as such.
9. **Activity usually matters more than trip length alone.** Hiking, camping, hunting, fishing, forestry, off-trail movement, berry/mushroom gathering, and repeated time in forest-edge or vegetated habitat raise exposure compared with city travel.
10. **Report uncertainty plainly.** Absence of reported cases is not proof of absence, especially where surveillance is weak or geographically coarse.

## Step 1 — Establish the user's question

Identify which decision the user is trying to make:

- "What is my TBE risk on this trip?"
- "Should I consider TBE vaccination for this trip?"
- "Which of these routes has more TBE risk?"
- "Does the month, elevation, or type of trail change the risk?"
- "Is this destination considered endemic?"

If the user only wants geographic risk, do not ask for personal medical history.

If the user wants a vaccination decision, first assess trip exposure. Only then consider the limited personal factors in Step 3.

## Step 2 — Build the trip exposure record

Create an internal trip record with these fields:

| Field | Required? | How to obtain it |
|---|---|---|
| Destination country | Yes | Infer from named route/place where possible |
| Exact route / area | Yes | Infer from route name, link, map, GPX, coordinates, or itinerary; ask only if ambiguous |
| Administrative regions crossed | Yes | Research; do not ask the user unless the route itself is unclear |
| Travel dates or month | Yes | Ask if missing |
| Activity type | Yes | Infer if the user says hike/trek/camp; otherwise ask |
| Days exposed outdoors | Yes | Infer from itinerary; otherwise ask |
| Typical hours outdoors per day | Helpful | Infer from route stages when practical; otherwise ask only if it could change the assessment |
| Route elevation range | Yes for mountain trips | Research from a reliable route/topographic source or supplied GPX |
| Habitat along route | Yes | Research forest, forest edge, meadow, pasture, scrub, exposed alpine terrain, urban areas |
| Off-trail exposure | Helpful | Ask if materially uncertain |
| Overnight style | Helpful | Ask if camping/bivouac versus huts/hotels could materially change outdoor exposure |
| Repeated/future similar trips | Helpful for vaccine decision | Ask only when vaccination relevance is being assessed |

### Question discipline

Do not interrogate the user for facts that can be researched reliably.

If information is missing, ask the smallest useful batch of questions, normally no more than 2-4 at once. Good examples:

- What dates or month will you be there?
- Is this the standard route, or can you share the exact route/GPX/link?
- Will you mainly hike established trails, or spend meaningful time off-trail/in dense vegetation?
- Are you camping/bivouacking or sleeping in huts/hotels?

If enough information already exists to produce a useful result, research first instead of asking optional questions.

## Step 3 — Add personal modifiers only when the user asks about vaccination

Do not make these prerequisites for a geographic risk assessment.

Relevant decision modifiers include:

- age band, especially whether the traveler is 60 or older because severe disease risk increases with age;
- prior TBE vaccination and dates/doses;
- likelihood of future travel to endemic regions;
- personal tolerance for a rare but potentially severe disease versus vaccination burden and adverse-event risk.

If pregnancy, immune suppression, a history of severe vaccine allergy, a prior serious reaction, or another significant medical issue is mentioned, do not make a personalized medical clearance decision. Explain that the exposure assessment still applies, but vaccine suitability should be discussed with a clinician or travel-medicine service.

## Step 4 — Resolve the exact geography

For a named trail or destination:

1. Identify the route's start/end and major waypoints.
2. Identify every relevant country, province/state, district/county, and NUTS region crossed where practical.
3. Determine the elevation range and the approximate portions that pass through forest, forest edge, meadow/pasture, scrub, or exposed alpine terrain.
4. If the route crosses multiple epidemiologically different regions, assess them separately before creating a trip-level conclusion.
5. If a GPX file is supplied and tools permit, use it to establish coordinates/elevation and intersect conceptually with the relevant administrative/risk regions. Do not pretend to have performed GIS intersection if the available tools do not support it.

Prefer official geographic/topographic sources, protected-area sites, route operators, established mapping services, or the supplied GPX for route geometry. Route blogs may fill gaps but must not be used as TBE epidemiology sources.

## Step 5 — Research sources in this order

Use [references/tbe-travel-risk/source-strategy.md](references/tbe-travel-risk/source-strategy.md) for source discovery and validation.

For each affected region, try to obtain:

1. current official TBE risk classification or risk map;
2. recent locally acquired human case data and place of infection if available;
3. current vaccination recommendation for residents/travelers/outdoor exposure;
4. current seasonal pattern or tick activity guidance;
5. supporting vector distribution only when it helps interpret ecological plausibility.

Search in both English and the destination country's language when useful.

## Step 6 — Evaluate five evidence dimensions

Do not collapse the evidence into a formula. Assess each dimension separately.

### A. Local TBE activity

Classify as one of:

- **No established evidence** — no recognized local transmission in the route area in the available authoritative data.
- **Sporadic / uncertain** — isolated cases, emerging focus, adjacent-area transmission, or weak/coarse surveillance.
- **Established** — repeated locally acquired cases or official endemic/risk-area designation.
- **High local activity** — official high-risk classification, comparatively high recent incidence, or strong repeated surveillance evidence.

When the national authority has its own official categories, quote and preserve those categories rather than replacing them with this vocabulary.

### B. Season

Classify as:

- outside locally documented activity/transmission season;
- shoulder season;
- main season;
- peak period, if an authoritative local source supports a peak.

Weather can shift tick activity within a year. Do not use weather alone to override epidemiological seasonality.

### C. Habitat exposure

Classify as:

- **Minimal** — predominantly urban, paved, exposed rock/snow, or other poor tick habitat;
- **Low** — short or intermittent contact with suitable vegetation;
- **Moderate** — repeated trail travel through forest edge, meadow, pasture, scrub, or low vegetation;
- **High** — prolonged/repeated woodland or dense vegetated exposure, off-trail activity, field work, camping with extensive ground/vegetation contact, hunting, forestry, or similar exposure.

### D. Duration and repetition

Consider:

- total outdoor days;
- hours per day in suitable habitat;
- repeated visits during the same season;
- likely future trips to endemic regions.

Duration modifies exposure but should not override location and habitat.

### E. Elevation and micro-environment

Use elevation as context:

- lower wooded valleys may contribute more exposure than high exposed ridges;
- a high-altitude route can still include risky approach/exit sections;
- shaded, humid, vegetated terrain may support ticks at elevations where exposed terrain nearby does not;
- never infer a zero-risk elevation without authoritative local evidence.

## Step 7 — Produce the trip-level assessment

Return three separate judgments rather than one opaque score.

### 1. Background TBE activity

Use:

- **No established evidence**
- **Sporadic / uncertain**
- **Established**
- **High local activity**

### 2. Traveler exposure intensity

Use:

- **Minimal**
- **Low**
- **Moderate**
- **High**

### 3. Overall TBE concern for this itinerary

Use:

- **Very low** — little/no evidence of local transmission, or exposure is negligible.
- **Low** — some plausible local activity but limited exposure, or established transmission with strongly reduced exposure due to season/habitat.
- **Moderate** — established transmission plus meaningful outdoor exposure during the active season.
- **High** — established/high local activity plus extensive or repeated exposure in suitable tick habitat during the main/peak season.

These labels describe **relative travel concern**, not an estimated percentage chance of infection. Make this explicit.

Avoid **"zero risk"** except where an authoritative source explicitly supports absence of transmission and the context truly warrants it; normally prefer "very low" or "no established evidence."

## Step 8 — Translate the assessment into vaccination relevance

When the user asks whether vaccination is worth considering, apply the current recommendations of the relevant authorities.

Use this order:

1. destination national/regional authority if it provides traveler-specific guidance;
2. CDC/ACIP traveler guidance;
3. WHO general guidance;
4. specialist national travel-medicine guidance if official public-health sources are silent.

As a general CDC/ACIP framework, verify the current wording at execution time:

- vaccination is recommended for people traveling or moving to a TBE-endemic area who will have **extensive exposure to ticks** based on planned outdoor activities and itinerary;
- vaccination may be considered for people traveling to an endemic area who might engage in outdoor activities where ticks are likely to be found.

Do not automatically apply a resident vaccination policy to a short-term traveler. Explain when a local recommendation was written for residents rather than visitors.

Use one of these conclusions:

- **Usually not indicated by this itinerary alone**
- **Reasonable to consider**
- **Strong reason to consider**
- **Recommended under the cited traveler guidance**

If the applicable authority gives a more direct recommendation, use its wording instead.

## Step 9 — Assign evidence confidence

Report confidence separately from risk.

### High confidence

Use when most of these are true:

- official national/regional risk classification exists for the exact area;
- recent locally acquired case data are available at a useful geographic resolution;
- route location and dates are clear;
- multiple authoritative sources agree.

### Medium confidence

Use when:

- data are official but geographically coarse or somewhat old;
- route crosses the edge of a risk area;
- local case data are sparse;
- different sources use different geographic definitions but are broadly compatible.

### Low confidence

Use when:

- surveillance is weak or absent;
- only national-level data exist for a focal disease;
- local evidence is old;
- available sources conflict materially;
- route geography cannot be resolved precisely.

Do not raise confidence merely because many secondary websites repeat the same claim.

## Step 10 — Required output format

Keep the answer readable and evidence-led.

### Trip profile

A compact table with:

- route/area;
- dates;
- regions crossed;
- elevation range;
- main habitat/exposure pattern;
- outdoor duration.

### Assessment

A compact table:

| Dimension | Assessment | Why |
|---|---|---|
| Local TBE activity | ... | ... |
| Season | ... | ... |
| Habitat exposure | ... | ... |
| Duration/repetition | ... | ... |
| Elevation context | ... | ... |

Then state:

- **Background TBE activity:** ...
- **Traveler exposure intensity:** ...
- **Overall TBE concern:** ...
- **Confidence:** ...

### Vaccination relevance

Only include this section if asked or clearly useful. Cite the exact current guidance used and distinguish traveler guidance from resident policy.

### Evidence

List the 2-6 sources that materially support the conclusion. For each, provide:

- authority;
- publication/update date;
- what it establishes;
- direct link/citation.

Prefer a few primary sources over a long bibliography.

### What could change the result?

Mention only factors that could materially move the assessment, such as a different month, a lower forested route variant, several days of camping/off-trail exposure, or new local surveillance data.

## Comparing multiple trips

When comparing destinations, assess each independently using the same dimensions, then give a comparison table. Do not rank countries by national incidence alone.

Example structure:

| Trip | Local activity | Exposure | Overall concern | Confidence | Vaccine relevance |
|---|---|---|---|---|---|
| Route A | High local activity | High | High | High | Strong reason / recommended |
| Route B | Established | Low | Low | Medium | Usually not indicated / consider |

Explain the one or two factors that drive the difference.

## Handling weak or conflicting evidence

If sources conflict:

1. prefer the more local authority for local epidemiology;
2. prefer the newer source if methodology and authority are comparable;
3. check whether one source describes **tick distribution** while another describes **human TBE cases**;
4. check whether the geographic units differ;
5. check whether one source is a resident vaccination map rather than a disease-transmission map;
6. show the disagreement rather than silently choosing a convenient source.

If no strong local evidence exists, say so and lower confidence. Do not fill the gap with a precise estimate.

## Common mistakes to avoid

- Treating an entire country as homogeneous.
- Using Lyme disease maps as a proxy for TBE.
- Treating *Ixodes ricinus* presence as proof of TBE-virus circulation.
- Treating zero cases in one year as proof that a focus disappeared.
- Ignoring vaccination coverage when interpreting resident case incidence.
- Declaring high alpine terrain risk-free based on a simple altitude threshold.
- Using total trip duration instead of actual time in suitable tick habitat.
- Recommending vaccination solely because the country appears on a generic travel-vaccine list.
- Giving a numerical infection probability without a defensible traveler-specific denominator.
- Citing commercial vaccine clinics as the primary evidence when official surveillance exists.

## Safety boundary

If the user reports a recent tick bite, fever, neurological symptoms, severe headache, neck stiffness, weakness, confusion, or another concerning symptom, switch from itinerary risk estimation to appropriate medical guidance. Do not use this skill's qualitative travel-risk labels to rule out disease in a symptomatic person.
