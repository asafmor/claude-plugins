# Europe Travel Vaccine Risk

Assess vaccination relevance for a specific European trip. Build the recommendation from the traveler's actual itinerary, current vaccination status, current disease activity, and the destination's own public-health guidance.

This skill is for pre-travel vaccination decision support. It does not diagnose illness, replace urgent care after an exposure, or provide medical clearance for pregnancy, immune suppression, severe vaccine allergy, prior serious vaccine reactions, or other individualized contraindications.

## Core principles

1. **Assess the itinerary, not merely the country.** Risk can vary sharply by region, season, altitude, habitat, activity, accommodation, and access to medical care.
2. **Do not use a fixed “Europe vaccine list.”** Start from current destination guidance, then test every potentially relevant vaccine against the itinerary.
3. **Separate three different questions:**
   - Is routine vaccination up to date?
   - Does this itinerary create an additional vaccine indication?
   - Is any vaccine or certificate required for entry, exit, transit, work, study, or another administrative reason?
4. **Prefer destination authorities.** National or regional public-health guidance for the place visited has priority for local disease activity and local vaccination policy.
5. **Use European traveler-oriented sources for interpretation.** ECDC, current national travel-medicine guidance, and recognized travel-health services help translate local disease data into traveler relevance.
6. **Use current data.** Search for the newest guidance, surveillance, outbreak notice, risk map, and vaccine schedule available at execution time. State the dates of the material relied on.
7. **Do not confuse resident policy with traveler policy.** A vaccine recommended or funded for residents is evidence of local risk but is not automatically a recommendation for a short-term visitor.
8. **Do not confuse disease presence with meaningful traveler risk.** The final recommendation must account for exposure type and duration.
9. **Do not invent precise probabilities.** If no validated traveler attack rate exists for the specific setting, use a qualitative assessment rather than deriving a number from population incidence.
10. **Do not assume that “Europe” means low risk for every vaccine-preventable disease.** Eastern, southeastern, northern, alpine, rural, and outbreak-affected areas can have different recommendations.
11. **Do not let an old travel-clinic page override newer surveillance or policy.** Resolve conflicts by authority, specificity, and freshness.
12. **Report uncertainty plainly.** Lack of reported cases, a blank ECDC table, or absence from one travel-health page is not proof of zero risk.

## Step 1 — Identify the user's decision

Typical questions include:

- Which vaccines should I get for this trip?
- Are there vaccines Europeans recommend for this trek?
- Do I need anything beyond routine vaccines?
- Is TBE, hepatitis A, hepatitis B, rabies, or another vaccine worth considering?
- Does the month, route, camping, altitude, or remoteness change the recommendation?
- Which vaccines are requirements versus optional protection?

If the user asks only about geographic disease risk, do not ask for unrelated medical history.

If the user wants a vaccination recommendation, gather the minimum traveler-specific facts in Steps 2 and 3.

## Step 2 — Build the trip exposure record

Create an internal record with these fields:

| Field | Required? | How to obtain it |
|---|---|---|
| Countries visited and transited | Yes | Infer from itinerary; ask only if ambiguous |
| Exact route / region | Yes for outdoor trips | Infer from route name, link, GPX, coordinates, or itinerary; research administrative regions |
| Travel dates or month | Yes | Ask if missing |
| Trip duration | Yes | Infer from itinerary; otherwise ask |
| Main activities | Yes | Infer hiking/cycling/camping/etc.; otherwise ask |
| Outdoor exposure | Yes for outdoor trips | Research route and infer; ask only when materially uncertain |
| Accommodation | Helpful | Ask if camping/bivouac versus huts/hotels can change exposure or access to care |
| Urban versus rural proportion | Helpful | Research/infer |
| Food/water context | Helpful | Ask only if local food, basic sanitation, remote villages, or long stays could change hepatitis A/typhoid relevance |
| Animal exposure | Helpful | Ask if rabies could be decision-changing: animal work, caves/bats, dogs, cycling/running, remote areas |
| Access to medical care | Helpful | Research remoteness; important for rabies pre-exposure decisions |
| Work/volunteering | Helpful | Ask if healthcare, animal, laboratory, childcare, refugee-camp, humanitarian, or other occupational exposure is possible |
| Planned mass gathering | Helpful | Ask only if relevant to meningococcal, influenza, measles, mpox, or event-specific requirements |

### Question discipline

Do not ask the user for facts that can be researched reliably from a named route or destination.

Ask the smallest useful batch of missing questions, normally no more than 2–4 at once. Examples:

- What dates or month will you travel?
- Is this the standard route, or can you share the GPX/link?
- Are you camping/bivouacking or sleeping in huts/hotels?
- Will you have meaningful animal contact, caving/bat exposure, or work with animals?

Research first when enough information already exists to make progress.

## Step 3 — Build the vaccination record

For a recommendation rather than a purely geographic assessment, establish as much of the following as needed:

- age band;
- country whose routine immunization schedule the traveler grew up under, if relevant to interpreting likely prior doses;
- documented doses or known history for tetanus/diphtheria/pertussis, polio, MMR, varicella, hepatitis A, hepatitis B, TBE, rabies, influenza, COVID-19, and other relevant vaccines;
- dates of the most recent tetanus-containing dose and any TBE/rabies doses when those vaccines are under consideration;
- prior natural disease only where accepted by current guidance as evidence of immunity;
- repeat/future travel to similar destinations, when it materially changes the value of a multi-dose series.

Do **not** assume vaccination merely because the traveler is of a certain age or nationality. If records are uncertain, say that the routine-status conclusion is provisional.

If pregnancy, immune suppression, severe allergy, prior serious vaccine reaction, anticoagulation, or another medical issue relevant to vaccine administration is mentioned, continue the itinerary risk assessment but leave vaccine suitability and schedule adaptation to a clinician/travel-medicine service.

## Step 4 — Resolve the exact geography and exposure

For a named trail, trek, cycling route, park, or rural itinerary:

1. Identify start/end and major waypoints.
2. Identify countries and relevant regions/districts crossed.
3. Determine route elevation range when relevant.
4. Characterize habitat and exposure: urban, agricultural, forest, forest edge, meadow/pasture, scrub, alpine terrain, caves, freshwater, farms, villages, etc.
5. Identify areas where medical care or rabies post-exposure prophylaxis may be difficult to access.
6. If the route crosses epidemiologically different areas, assess them separately before producing a trip-level conclusion.
7. If a GPX is supplied and tools permit, use it to improve location/elevation assessment. Do not claim GIS-level intersection unless it was actually performed.

Use route sources for geography and exposure only. Do not use hiking blogs as primary vaccine epidemiology sources when official sources exist.

## Step 5 — Research sources in priority order

Read [references/europe-travel-vaccine-risk/source-strategy.md](references/europe-travel-vaccine-risk/source-strategy.md).

For every country/region, try to obtain:

1. current country-specific traveler vaccine recommendations;
2. current national/regional disease surveillance or risk maps for diseases where geography matters;
3. current routine/catch-up immunization schedule when the user's baseline status matters;
4. current outbreak notices for measles, polio, hepatitis A, meningococcal disease, mpox, or other vaccine-preventable diseases;
5. current entry/transit vaccination-certificate rules if relevant;
6. timing/schedule guidance for any vaccine that appears relevant.

Search in the destination country's language as well as English when useful.

## Step 6 — Screen vaccine categories

Do not stop after finding one vaccine. Screen all categories below, but report only those that are relevant or useful to verify.

### A. Routine and catch-up vaccines

At minimum consider:

- tetanus, diphtheria, pertussis;
- measles, mumps, rubella (MMR);
- polio;
- varicella where appropriate;
- influenza based on season/risk/current recommendations;
- COVID-19 based on current destination and personal recommendations.

Use ECDC and the traveler's home-country schedule only as aids to reconstruct routine status. The destination's resident schedule does not determine what the traveler personally received.

### B. Common itinerary-driven European travel vaccines

Explicitly evaluate when geographically or behaviorally relevant:

- **Tick-borne encephalitis (TBE)** — region, season, habitat, outdoor exposure, altitude, route duration, repeated future exposure;
- **Hepatitis A** — destination endemicity, outbreaks, food/water conditions, rural/basic travel, duration;
- **Hepatitis B** — destination prevalence plus sexual exposure, medical/dental care, blood exposure, tattoos/piercing, long stay, occupational risk;
- **Rabies** — country/region animal risk, planned animal/bat exposure, cycling/running, children, remoteness, access to post-exposure vaccine and rabies immunoglobulin.

For TBE-specific assessment, use the detailed disease methodology in [references/europe-travel-vaccine-risk/vaccine-framework.md](references/europe-travel-vaccine-risk/vaccine-framework.md).

### C. Less common but possible vaccines/requirements

Evaluate only when destination guidance, itinerary, outbreak, work, or transit makes them plausible:

- typhoid;
- meningococcal vaccines;
- cholera;
- yellow fever certificate/vaccination requirements related to arrival from another country;
- additional polio dose or certificate requirements;
- BCG for selected prolonged/high-risk exposure under current national guidance;
- mpox vaccination for defined exposure groups or outbreak-specific advice;
- any new or country-specific vaccine recommendation found in current authoritative guidance.

Do not recommend these merely because they appear on a general travel-vaccine list.

## Step 7 — Classify each vaccine independently

For every vaccine worth mentioning, assign one status:

### **Routine status to verify / catch up**
Use when the main issue is whether standard immunization is complete, rather than a special travel indication.

### **Recommended for this itinerary**
Use only when current traveler guidance directly recommends vaccination for a traveler matching the destination/exposure profile, or when an authoritative destination authority gives an equivalent clear recommendation.

### **Reasonable to consider**
Use when authoritative guidance describes vaccination as optional/considerable for the exposure, or where the traveler is near a threshold and individual preferences matter.

### **Usually not indicated by this itinerary**
Use when the disease/vaccine was assessed and current evidence does not support routine vaccination for the described trip.

### **Administrative requirement / certificate issue**
Use when vaccination or documentation is required or may be requested for entry, exit, transit, employment, study, or another non-clinical reason. Keep this separate from medical benefit.

If the evidence is insufficient, say **Insufficient evidence for a confident recommendation** instead of forcing a category.

## Step 8 — Apply disease-specific exposure logic

Read [references/europe-travel-vaccine-risk/vaccine-framework.md](references/europe-travel-vaccine-risk/vaccine-framework.md).

Important examples:

- **TBE:** local human transmission and official risk areas matter more than generic tick presence; hiking/camping in suitable habitat during the local season raises exposure.
- **Hepatitis A:** distinguish general country recommendation from recommendation only for specific traveler types; consider outbreak status.
- **Hepatitis B:** destination prevalence alone is not enough; map it to actual exposure routes and duration.
- **Rabies:** pre-exposure vaccination is especially affected by remoteness, animal/bat exposure, activity type, and reliable access to post-exposure treatment. Never imply that pre-exposure vaccination removes the need for urgent care after a bite/scratch/bat exposure.
- **Tetanus:** treat as routine/catch-up unless current guidance specifies a travel-related booster due to elapsed time and limited access to care.
- **MMR/measles:** check current outbreak/transmission information and documented immunity; travel can increase the consequence of incomplete routine vaccination.
- **Polio:** distinguish routine booster advice from temporary WHO/IHR certificate rules affecting people arriving from or departing certain countries.

## Step 9 — Check timing feasibility

For each vaccine categorized as Recommended or Reasonable to consider:

1. find the current approved or officially recommended schedule;
2. determine how many doses can realistically be given before departure;
3. identify accelerated schedules only if supported by current authoritative guidance or the current product information;
4. state when meaningful protection is expected only if the source provides it;
5. distinguish a trip-protective partial series from completion of the long-term primary series;
6. never invent a shortened schedule because travel is soon.

If the trip is imminent, still provide useful options rather than assuming it is “too late.”

## Step 10 — Check entry and transit requirements separately

If the itinerary includes transit through or arrival from countries that can trigger certificate rules, research current International Health Regulations and destination rules.

Keep wording explicit:

- **Medical recommendation:** protects the traveler based on disease risk.
- **Administrative requirement:** required documentation for border/visa/work/study reasons.

Do not conflate the two.

## Step 11 — Resolve source conflicts

When sources disagree:

1. prefer the destination's current national/regional public-health authority for local epidemiology;
2. prefer current traveler-specific guidance over a resident-only schedule for traveler recommendations;
3. prefer a newer authoritative source over an older clinic page;
4. prefer geographically precise surveillance over country-wide generalizations;
5. preserve differences in wording such as “recommended,” “consider,” and “not routinely recommended” instead of flattening them;
6. explain the conflict if it changes the conclusion.

Do not silently average contradictory recommendations.

## Step 12 — Assign confidence

Report confidence separately for each material conclusion or for the overall assessment.

### High confidence

Use when:

- current destination-specific traveler guidance is available;
- local surveillance/risk data are recent where needed;
- route, dates, activities, and vaccination history are clear;
- authoritative sources agree.

### Medium confidence

Use when:

- guidance is official but geographically coarse;
- vaccination history is uncertain;
- the route crosses the edge of a risk area;
- recent local surveillance is incomplete;
- sources differ slightly but point in the same general direction.

### Low confidence

Use when:

- disease surveillance is weak or old;
- traveler-specific guidance is absent;
- sources conflict materially;
- key itinerary or vaccination facts remain unknown.

## Step 13 — Output format

Start with a concise bottom line, then use a compact table.

Recommended structure:

### Bottom line

State which vaccines fall into these groups:

- **Recommended / strongest case**
- **Reasonable to consider**
- **Routine status to verify**
- **Not indicated by this itinerary** only when the user explicitly asked about those vaccines
- **Administrative requirements**, if any

### Vaccine assessment

| Vaccine | Status | Why it matters for this trip | Evidence / geography | What would change the answer |
|---|---|---|---|---|
| TBE | ... | ... | ... | ... |
| Hepatitis A | ... | ... | ... | ... |

Do not clutter the table with every vaccine known to medicine. Include routine vaccines that need verification and itinerary-driven vaccines that were genuinely plausible.

### Trip-specific reasoning

Explain the decisive exposure facts: destination/subregion, season, route habitat, remoteness, food/water context, animal exposure, duration, outbreaks, and current official recommendations.

### Timing

If departure timing matters, show the feasible schedule and any limitations.

### Confidence

State **High / Medium / Low** and explain the main uncertainty in 1–3 sentences.

### Sources

Cite the current primary and cross-check sources inline. Prefer direct links to the exact official country page, surveillance report, outbreak notice, or vaccine recommendation rather than generic homepages.

## Safety boundaries

- Do not diagnose illness or interpret post-travel symptoms as a vaccine-preventable disease without appropriate clinical caution.
- A possible rabies exposure requires urgent medical assessment even after pre-exposure vaccination.
- A tick bite does not itself prove TBE infection; vaccination after a tick bite is not a substitute for medical advice where symptoms or exposure warrant it.
- Do not advise a traveler with a serious contraindication, pregnancy, immune suppression, or prior severe vaccine reaction that a vaccine is personally “safe for you.” Provide the itinerary indication and refer vaccine suitability to a clinician.
- Do not tell a traveler to skip a required vaccine/certificate based on a risk-benefit argument; administrative requirements must be checked separately.
- Do not use antibody testing as a generic shortcut for uncertain vaccination history unless current authoritative guidance supports that test for that vaccine and purpose.

## Final quality check

Before answering, confirm:

- [ ] I assessed the exact destination/route rather than Europe generically.
- [ ] I checked current destination-specific traveler guidance.
- [ ] I checked recent outbreak/surveillance information where it could alter the recommendation.
- [ ] I separated routine catch-up, itinerary-driven vaccination, and administrative requirements.
- [ ] I did not infer vaccination status from age/nationality alone.
- [ ] I did not automatically recommend every travel vaccine.
- [ ] I mapped hepatitis B and rabies recommendations to actual exposure, not just country presence.
- [ ] I handled TBE at subnational level where possible.
- [ ] I checked timing and schedules only from current authoritative sources.
- [ ] I labeled uncertainty and source conflicts clearly.
