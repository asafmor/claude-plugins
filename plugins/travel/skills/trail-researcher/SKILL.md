---
name: trail-researcher
description: Deep-research a named trail, trek, hike, or route and return a comprehensive, current, source-backed Markdown planning report using the fixed 17-section structure, including an embedded GeoMap JSON artifact. Use for route research, trek planning, stage analysis, logistics, safety, historical weather, mobile connectivity, pronunciation, accommodation, transport, gear, costs, current status, and pre-departure verification.
---

# Trail Researcher

Deep-research a named trail, trek, hike, or route in depth and return one comprehensive Markdown report that follows the fixed structure in this skill.

## Invocation and scope

- The user's trail/trek/hike/route name is the primary input. Use any supplied dates, pace, direction, accommodation preference, transport constraints, or other trip context when they materially affect the report.
- Do not ask follow-up questions when a reasonable assumption can be made. State important assumptions in the relevant section and lower confidence where needed.
- If the route name is genuinely ambiguous, research the most likely intended route and explicitly identify that interpretation near the start of section 1.1.
- Use the platform's Deep Research capability when it is available. Otherwise perform an extensive live web research workflow using multiple independent sources. Do not rely on model memory for current conditions, regulations, schedules, prices, closures, accommodation operations, water availability, or other time-sensitive facts.
- Research the whole route before writing the final report. Do not produce a shallow section-by-section answer from the first source found.

## Research workflow

1. Establish the route's canonical identity, official or customary start/finish, standard direction, stage pattern, and managing organizations.
2. Build a source set using this preference order where appropriate: official trail/park/government and meteorological sources; official transport operators, mobile-network operators, regulators, and primary accommodation/service providers; authoritative mapping and language sources; established specialist hiking publications and YouTube videos; recent firsthand reports.
3. For consequential claims, cross-check multiple independent sources when practical, especially distance/elevation, difficult stages, regulations, access, emergency information, historical weather, cellular reception, water, closures, transport, accommodation, and costs. Distinguish modeled mobile coverage from observed reception and transliteration from pronunciation.
4. Distinguish relatively stable route facts from time-sensitive information. Attach an explicit checked date to time-sensitive facts.
5. Prefer the most recent authoritative source, but do not silently discard disagreement. Report material conflicts where they occur and reflect them in the confidence rating.
6. Use current, route-specific evidence for the final-status section. If no recent status information exists, say so clearly and identify the best official resource to re-check.
7. Never invent a route fact, price, schedule, closure, booking rule, GPX link, map link, phone number, emergency instruction, or source. If a fact cannot be established, mark it as unknown or uncertain.
8. Before finalizing, verify that every required heading appears exactly once, in the required order and at the required Markdown level, and that no additional level 1–3 headings were introduced.

## Output contract

- Return a single Markdown document only. Do not add a preamble, methodology note, summary, or appendix outside the prescribed structure.
- Replace `# [Trail / Route Name]` with the researched route's name. Preserve every other heading exactly as written below.
- Do not remove, rename, reorder, or change heading levels up to level 3. You can manage level 4-6 headings as desired.
- Fill every bracketed placeholder with actual researched content. Do not leave instructional placeholders in the final report.
- Keep content useful for trip planning rather than generic hiking education. Route-specific facts and decisions come first.
- Use metric units by default. When a source uses another unit, convert it and optionally show the original in parentheses if useful.
- For stages, use consistent `km`, `↑`, `↓`, and `h` notation when it improves scanning.
- For prices, show currency and the checked date. If meaningful, distinguish per-person, per-room, per-stage, or total.
- For current-status information, state the exact research/check date, not merely “current” or “latest”.
- Citation placement should be claim-level whenever practical. Prefer descriptive Markdown links and platform-native citations when available. The source register in section 17.8 must include every significant source used.
- If an authoritative online image materially improves orientation or comprehension and a stable attributable image is available, embed it sparingly with descriptive alt text and source attribution. If not, omit the image rather than using decorative or unreliable imagery.

## Required presentation guidelines

* **Preserve the provided report structure exactly:** make content within each predefined section easy to scan using concise paragraphs, short lists, tables, whitespace, and other inline Markdown elements.
* **Prefer Markdown tables for comparable information:** use them for stages, distances, ascent/descent, accommodation, transport, seasonal conditions, costs, and similar structured data; keep tables compact and use symbols such as `↑`, `↓`, `km`, and `h` consistently where they improve scanning.
* **Establish a small, fixed visual vocabulary of icons:** use recurring symbols such as `⚠️` hazard, `💧` water, `🍴` food, `🛏️` accommodation, `🚌` transport, and `📍` location consistently and sparingly rather than decorating ordinary prose.
* **Use blockquotes for meaningful callouts:** reserve patterns such as `> ⚠️ **Warning:**`, `> 💡 **Tip:**`, and `> 📅 **Check before departure:**` for information that genuinely deserves extra attention.
* **Use emphasis selectively:** apply **bold** to decision-critical facts, recommendations, warnings, and key values, and *italics* only for occasional secondary emphasis; avoid making the document visually noisy.
* **Make time-sensitive information visually distinct:** mark changing facts with a consistent `📅` indicator and an explicit date such as **Checked: 5 September 2026**, especially for trail conditions, closures, prices, schedules, water availability, regulations, and accommodation.
* **Make recommendations immediately recognizable and explain why:** use a consistent pattern such as `✓ **Recommended:**` followed by concise route-specific reasoning rather than generic hiking advice.
* **Make links descriptive and actionable:** use Markdown links instead of raw URLs, place them beside the information they support, and prefer consistent labels such as `[Official website]`, `[Book]`, `[Timetable]`, `[Map]`, and `[Download GPX]`.
* **Surface uncertainty where it occurs:** use a consistent convention such as `**Confidence: High**`, `**Confidence: Medium**`, or `⚠️ **Confidence: Low**`, and briefly explain conflicting or incomplete evidence in the relevant section rather than hiding it elsewhere.
* **Optimize every section for trip planning and visual scanning:** lead with the useful answer, use prose for explanation, lists for choices or steps, tables for comparison, and callouts for exceptional information; embed relevant online images when they materially improve orientation or comprehension—such as route maps, elevation profiles, trail markings, terrain examples, transport diagrams, or accommodation locations—and use descriptive alt text, restrained placement, and preferably authoritative or clearly attributable sources rather than decorative imagery.

---

## Fixed report structure

# [Trail / Route Name]

## 1. Route Overview

### 1.1 Identity & Geography

[Describe where the route is located, its official start and finish, total distance, cumulative elevation gain and loss, highest point, typical duration, and usual direction of travel.]

### 1.2 Character & Experience

[Describe what makes the route distinctive, including its scenery, landscapes, settlements, cultural character, atmosphere, popularity, and major highlights.]

### 1.3 At a Glance

[Summarize the route's difficulty, ideal season, typical accommodation model, daily walking demands, and the most significant considerations a hiker should know before deciding to undertake it.]

---

## 2. Route & Stage Breakdown

### 2.1 Standard Itinerary

[Present the commonly followed itinerary with each stage's start and finish, distance, ascent, descent, estimated walking time, and overnight location.]

### 2.2 Stage-by-Stage Analysis

[Analyze every stage individually, covering terrain, physical demands, notable climbs and descents, landmarks, scenery, water, food, services, difficult sections, and anything hikers should anticipate during that day.]

### 2.3 Alternative Itineraries

[Describe practical faster and slower itineraries and explain where standard stages can reasonably be combined, shortened, or split.]

### 2.4 Variants & Detours

[Describe official variants, commonly used alternatives, shortcuts, optional side trips, and worthwhile detours together with their effects on distance, difficulty, and logistics.]

[Provide links to authoritative descriptions or maps of important route variants and detours.]

---

## 3. Difficulty & Trail Conditions

### 3.1 Physical Difficulty

[Assess the route's overall physical demands, typical daily workload, cumulative fatigue, required fitness level, and the hardest days.]

### 3.2 Technical Difficulty

[Explain the technical demands including trail surfaces, steep terrain, exposure, scrambling, river crossings, fixed aids, or other obstacles encountered on the route.]

### 3.3 Elevation

[Explain the route's elevation profile, highest and lowest points, major climbs and descents, sustained steep sections, and any relevant effects of altitude.]

### 3.4 Trail Condition

[Describe typical trail quality and maintenance together with erosion, mud, snow, damaged sections, or other conditions that can materially affect progress.]

---

## 4. Season & Weather

### 4.1 Hiking Season

[Explain when the route is normally hikeable, the usual opening and closing periods for trail infrastructure, the best months, and the implications of travelling during shoulder season.]

### 4.2 Weather Patterns

[Describe typical temperatures, precipitation, thunderstorms, wind, snow, visibility, and other significant weather patterns throughout the hiking season.]

### 4.3 Historical Weather for the Planned Travel Window

[Use the user's planned dates or calendar window to present historical weather for the same time of year in the route area. Use authoritative climate normals and, when useful, recent-year observations from representative low- and high-elevation locations or stages. Cover typical minimum/mean/maximum temperatures, precipitation frequency and amount, snow cover or depth when relevant, wind, thunderstorms, and other decision-relevant conditions. Name the dataset period, station or gridded source, distance and elevation relationship to the route, and important limitations. Keep historical climate evidence separate from a trip forecast; if the user supplied no dates, use the likely hiking window and state that assumption.]

### 4.4 Seasonal Trade-offs

[Compare the main hiking periods in terms of weather, crowds, daylight, trail conditions, accommodation availability, transport, and services.]

[Provide links to reliable regional weather forecasts, mountain forecasts, webcams, snow information, or other useful weather resources.]

---

## 5. Navigation & Route Finding

### 5.1 Waymarking

[Describe the route's signage and markings, how consistently they can be followed, and locations where hikers commonly experience navigation problems.]

### 5.2 Maps & Digital Navigation

[Identify the best paper maps, digital maps, navigation applications, official route maps, and reliable GPX tracks for the route.]

[Provide direct links to recommended maps, GPX downloads, official mapping resources, and other useful navigation resources.]

### 5.3 Navigation Preparation

[Explain what should be downloaded or prepared for offline use and what backup navigation methods are sensible for this route.]

---

## 6. Accommodation & Overnight Planning

### 6.1 Accommodation System

[Explain the types of accommodation available along the route, their geographic distribution, typical facilities, sleeping arrangements, meal options, and expected comfort level.]

### 6.2 Booking Strategy

[Explain which accommodation requires reservations, how competitive bookings are, how far ahead hikers should book, and any important cancellation or modification rules.]

[Provide direct links to official accommodation websites, reservation systems, booking pages, or reliable contact information.]

### 6.3 Overnight Logistics

[Describe practical overnight details such as meals, packed lunches, showers, laundry, drinking water, electricity, charging, Wi-Fi, check-in times, and operating hours.]

### 6.4 Camping

[Explain whether camping is practical and legal along the route, where campsites or designated areas exist, and what restrictions apply.]

[Provide links to official campsites, reservation pages, and authoritative camping regulations where applicable.]

---

## 7. Food, Water & Resupply

### 7.1 Water

[Describe where drinking water can normally be obtained, its reliability and treatment requirements, and identify any long sections where hikers must carry additional water.]

### 7.2 Food

[Explain where hikers can obtain meals, groceries, snacks, packed lunches, and other food along each part of the route.]

### 7.3 Resupply Strategy

[Describe practical resupply points, distances between them, sections without services, and how much food and water hikers should normally carry between opportunities.]

[Provide links to particularly useful route-specific resupply information or services where available.]

---

## 8. Access & Transportation

### 8.1 Reaching the Route

[Explain practical ways to reach the trailhead from relevant airports, railway stations, cities, and regional transport hubs.]

[Provide links to official public transport operators, schedules, ticketing systems, and other useful transportation resources.]

### 8.2 Leaving the Route

[Explain how to travel from the official finish back to relevant airports, cities, railway stations, or other major transport hubs.]

[Provide links to the relevant official transport schedules, operators, and ticketing systems.]

### 8.3 Along-the-Route Transport

[Describe buses, trains, taxis, cable cars, boats, roads, or other transport connections that can be used to skip stages, shorten the trek, or leave and later rejoin the route.]

[Provide links to useful transport operators, schedules, and booking services.]

### 8.4 Pre- and Post-Trek Logistics

[Describe useful accommodation, luggage storage, luggage-transfer services, parking, and other practical arrangements around the start and finish.]

[Provide links to relevant luggage storage, transfer, parking, or other route-specific logistical services.]

---

## 9. Safety & Risk Management

### 9.1 Main Hazards

[Identify the route's significant objective hazards including terrain, exposure, weather, heat, cold, snow, water crossings, wildlife, falling rock, or other environmental risks.]

### 9.2 Emergency Planning

[Explain emergency numbers, rescue arrangements, how the coverage gaps established in section 12.3 affect emergency calls and messaging, backup communication options, and what hikers should do if assistance is required. Keep the carrier comparison and purchasing recommendation in section 12.3.]

[Provide links to official emergency, mountain rescue, park authority, or safety information.]

### 9.3 Bailout & Escape Options

[Identify practical escape points, road access, settlements, transport connections, and sections where abandoning the route would be particularly difficult.]

### 9.4 Health & Insurance

[Explain route-relevant health considerations, travel-vaccination risk, and what travel, medical, evacuation, or mountain-rescue insurance hikers should verify before departure. Before drafting this subsection, the master agent must spawn exactly two research sub-agents and give both the route identity and geography, countries and administrative regions crossed, intended dates or likely hiking season, trip duration, stage pattern, elevation range, habitat exposure, accommodation model, and other known traveler context:

1. The **Europe travel-vaccine-risk sub-agent** must read and follow [the Europe travel-vaccine-risk instructions](references/europe-travel-vaccine-risk/europe-travel-vaccine-risk.md), [their source strategy](references/europe-travel-vaccine-risk/source-strategy.md), and [their vaccine assessment framework](references/europe-travel-vaccine-risk/vaccine-framework.md). It must perform current, itinerary-specific research covering routine-vaccine status that should be verified, vaccines potentially indicated by this trip, current outbreaks or surveillance signals, and entry/transit certificate requirements. It must screen TBE but leave the fine-grained TBE conclusion to the specialist sub-agent. If any part of the route lies outside Europe, it must identify the Europe-specific framework's limit and apply equivalent current destination-authority and traveler-health guidance for that part.
2. The **TBE travel-risk sub-agent** must read and follow [the TBE travel-risk instructions](references/tbe-travel-risk/tbe-travel-risk.md) and [their source strategy](references/tbe-travel-risk/source-strategy.md). It must resolve the route to the finest practical administrative geography and assess current local TBE activity, season, habitat, duration/repetition, elevation and micro-environment, traveler exposure intensity, overall qualitative TBE concern, vaccination relevance, and evidence confidence. It must distinguish human disease evidence from tick-vector presence and must not invent a precise infection probability or a supposedly risk-free elevation cutoff.

Each sub-agent must return research findings rather than final report prose: dated evidence, direct authoritative source links, claim-level citations, material conflicts, confidence, and unresolved gaps. The master agent must wait for both findings, compare their overlapping TBE evidence, resolve or explicitly preserve material disagreements by authority, geographic specificity, and recency, and consolidate them into one coherent subsection without duplicating conclusions. Present a concise trip-specific bottom line; a compact assessment of only relevant routine, itinerary-driven, or administrative vaccine issues; a clearly identifiable TBE assessment; other route-relevant health considerations; and insurance requirements or verification points. Separate background disease activity from this itinerary's exposure, resident vaccination policy from traveler guidance, medical recommendations from administrative requirements, and evidence confidence from risk severity. Do not provide individualized medical clearance or invent facts when dates or vaccination history are missing; state what the traveler should verify with a qualified travel-health clinician. Carry only the resulting actionable rechecks into sections 14.2 and 14.3, and include every significant health and vaccination source in section 17.8. Provide links to authoritative insurance requirements, rescue policies, and official health guidance where relevant.]

---

## 10. Rules, Access & Trail Management

### 10.1 Access Requirements

[Explain permits, entrance fees, registrations, reservations, quotas, or other formal requirements for hiking the route.]

[Provide direct links to official permit, registration, payment, or reservation systems.]

### 10.2 Regulations

[Explain applicable rules concerning camping, fires, protected areas, wildlife, waste, drones, dogs, seasonal access, and other activities relevant to hikers.]

[Provide links to authoritative regulations from park authorities, governments, or trail-management organizations.]

### 10.3 Trail Etiquette

[Describe local trail conventions, hut etiquette, environmental practices, and other behavioural expectations hikers should know.]

---

## 11. Gear & Packing

### 11.1 Route-Specific Gear Strategy

[Recommend an overall gear strategy appropriate for the route's terrain, weather, accommodation system, season, and expected degree of self-sufficiency.]

### 11.2 Footwear

[Explain what footwear characteristics are appropriate for the route based on terrain, surfaces, weather, technical difficulty, and expected daily distances.]

### 11.3 Clothing & Layering

[Describe an appropriate layering system for the expected temperature range, wind, precipitation, sun exposure, and changes in elevation.]

### 11.4 Rain & Weather Protection

[Explain the level of waterproofing, wind protection, sun protection, and other weather-specific equipment appropriate for the route.]

### 11.5 Sleeping & Accommodation Gear

[Explain what sleeping or hut equipment hikers need to carry and what is normally supplied by accommodation providers.]

### 11.6 Food & Water Equipment

[Describe the containers, treatment equipment, cooking equipment, or other food and water gear that is useful or necessary.]

### 11.7 Navigation, Electronics & Charging

[Describe appropriate navigation devices, phones, battery capacity, charging equipment, adapters, and other electronics for the route.]

### 11.8 Safety & Emergency Equipment

[Identify first-aid, emergency, signalling, lighting, repair, and route-specific safety equipment worth carrying.]

### 11.9 Pack Weight

[Provide realistic target pack-weight ranges and identify where hikers can reduce unnecessary weight without compromising safety or practicality.]

---

## 12. Costs & Practicalities

### 12.1 Trek Budget

[Estimate realistic low, typical, and higher daily and total costs covering accommodation, meals, resupply, transport, permits, and other significant expenses.]

### 12.2 Money

[Explain card acceptance, cash requirements, ATM availability, currencies, tipping practices, and where carrying cash is particularly important.]

### 12.3 Mobile Networks & Connectivity

[Identify the concrete mobile-network operators serving every country or region crossed and, when relevant, the underlying host network used by a proposed MVNO or travel eSIM. Compare route-specific cellular coverage and actual reception using official or regulator coverage maps plus recent local or hiker evidence; distinguish modeled coverage from observed reception. Note relevant voice/SMS and 2G/4G/5G availability, known gaps by stage, valley, pass, refuge, or settlement, roaming/eSIM limitations, Wi-Fi, and offline needs. Give a clear recommended primary network/SIM/eSIM with reasons, state whether a second-network backup or satellite messenger is warranted, date the findings, link directly to coverage maps and suitable plans where useful, and report uncertainty rather than inventing precision.]

### 12.4 Everyday Practicalities

[Describe toilets, showers, laundry, shops, pharmacies, charging, waste disposal, and other everyday services hikers are likely to need.]

---

## 13. Planning the Trek

### 13.1 Recommended Itinerary

[Propose a balanced itinerary with daily stages and overnight locations based on the preceding research and explain the main reasons for the chosen schedule.]

### 13.2 Reservations & Timeline

[Create a practical planning timeline showing what should be reserved or arranged, in what order, and approximately how far before departure.]

[Provide direct links to the key booking and reservation resources needed to execute the plan.]

### 13.3 Travel Plan

[Combine arrival, transport to the trailhead, the trek itself, accommodation, and departure into a coherent end-to-end travel plan.]

### 13.4 Contingency Planning

[Describe practical alternatives for bad weather, injury, fatigue, missed transport, closed accommodation, delayed travel, rest days, and shortening or abandoning the trek.]

---

## 14. Current Conditions & Final Preparation

### 14.1 Latest Route Status

[Research and summarize the latest available information about closures, diversions, trail damage, snow, construction, accommodation changes, transport disruptions, and other developments that could affect the trek.]

[Provide dated links to official status pages, trail organizations, park authorities, accommodation notices, or other reliable sources for current conditions.]

### 14.2 Pre-Departure Verification

[List the information that should be checked again shortly before departure, including weather, trail conditions, transport, accommodation, reservations, and relevant local warnings.]

[Provide links to the primary resources that should be checked again immediately before the trip.]

### 14.3 Final Checklist

[Provide a concise final checklist covering bookings, documents, transport, navigation resources, equipment, food, water, money, communications, and emergency information.]

---

## 15. Route-Specific Considerations

### 15.1 Special Characteristics

[Add subsections here for important characteristics, requirements, hazards, infrastructure, or logistical issues that are specific to this route and do not fit naturally elsewhere in the report.]

### 15.2 Local Knowledge

[Capture useful route-specific practices, advice, conventions, and practical knowledge that experienced hikers or local organizations consistently identify as valuable.]

[Provide links to high-quality local resources, official organizations, or particularly useful firsthand sources supporting this route-specific knowledge.]

### 15.3 Names & Pronunciation

[Provide a compact table for the trail name and the place names a traveler is most likely to say aloud, such as trailheads, stage towns, huts or refuges, passes, peaks, transport hubs or stops, and major landmarks. Include the local spelling, place type or context, language, an easy phonetic-English respelling with the stressed syllable clearly marked, and a short usage note. Distinguish pronunciation from transliteration; add IPA only when reliably sourced and helpful. Verify pronunciation using authoritative dictionaries, official or native audio, or credible multi-source evidence. Do not guess: mark uncertainty, explain important regional variants, and omit low-value names that cannot be supported.]

### 15.4 Research Gaps & Uncertainties

[Identify information that could not be established confidently, conflicting information found during research, and facts that need to be verified closer to departure.]

---

## 16. Maps

### 16.1 [Trail / Route Name]

[Build and embed one machine-readable GeoMap artifact for the researched route. Before drafting this section, the master agent must spawn exactly one dedicated **GeoMap builder sub-agent**. The sub-agent must read and follow [the GeoMap builder instructions](references/geomap-builder/geomap-builder.md).

The master agent must give the GeoMap builder enough context to resolve geographic entities correctly, including the canonical route identity and geography, the recommended/standard stage sequence, meaningful variants and detours, and the geographic findings already established elsewhere in the report. It must also provide:

- a deliberate list of map-worthy POIs derived from the report, with a category for every POI and `routeSection` where useful; include relevant overnight stops, accommodations, settlements, sights, passes, route junctions, water features, transport access/exit points, and useful detours, while avoiding trivial or redundant points;
- every authoritative or useful GPX URL discovered during route research that should appear on the map, especially official route/stage tracks and important variants;
- any relevant remote GeoJSON URLs discovered during research;
- enough local context to distinguish ambiguous names, similarly named features, buildings versus entrances, settlements versus stops, and route landmarks versus nearby namesakes.

The GeoMap builder sub-agent owns coordinate research and geographic normalization for this section. It must research POI coordinates, use route geometry for disambiguation/cross-checking where useful, download every supplied GPX/GeoJSON source it can reliably access, convert GPX content to standard GeoJSON according to its reference instructions, and return **only** the raw GeoMap JSON object defined by that reference, with `layers` as its root array property. It must omit unresolved POIs and failed remote datasets rather than fabricate geometry.

The master agent must not rewrite, reinterpret, summarize, or manually reconstruct the returned GeoMap JSON. It may validate that it is parseable JSON and satisfies the reference contract, but the geographic artifact itself must remain the sub-agent's result. Embed that raw JSON directly in this section inside exactly one fenced code block whose info string is `geomap`:

````text
```geomap
{"layers":[...raw layer wrappers returned by the GeoMap builder sub-agent...]}
```
````

Do not add prose, tables, explanations, captions, or additional code fences inside section 16. The `geomap` fence is the entire section body. The GeoMap is for visualization and planning context, not turn-by-turn navigation. Significant coordinate or dataset sources introduced by the GeoMap sub-agent must also be represented in section 17.8's source register when they are not already present.]

---

## 17. Research Sources & Confidence

### 17.1 Research Method

[Explain how the route was researched, including the types of sources consulted, the research date, how conflicting information was resolved, and how time-sensitive information was distinguished from relatively stable route information.]

### 17.2 Source Hierarchy

[Classify sources by authority and fitness for the claim, prioritizing official trail and park authorities, government and transport operators, primary service providers and mapping sources, established specialist publications, and recent firsthand reports in that order where appropriate.]

### 17.3 Source Recency

[Record publication, dataset period, update, or access dates where relevant and explicitly identify information whose reliability depends strongly on recency, such as closures, snow, transport schedules, cellular coverage and plans, prices, accommodation operations, water availability, and regulations.]

### 17.4 Cross-Verification

[For consequential claims, compare multiple independent sources where possible and explicitly flag disagreements rather than silently choosing one version.]

### 17.5 Confidence Ratings

[Assign High, Medium, or Low confidence to important findings based on source authority, recency, directness, consistency across independent sources, and whether the information could reasonably have changed since publication.]

#### High Confidence

[Use High when the claim is supported by authoritative or primary sources, is current enough for the subject, and is corroborated where corroboration is useful.]

#### Medium Confidence

[Use Medium when the available evidence is credible but incomplete, older, dependent on firsthand reports, or contains minor unresolved inconsistencies.]

#### Low Confidence

[Use Low when evidence is sparse, outdated, conflicting, indirect, anecdotal, or otherwise insufficient to support the claim without meaningful uncertainty.]

### 17.6 Confidence in Recommendations

[Distinguish factual confidence from recommendations, since a recommendation may combine well-established facts with subjective judgments about difficulty, comfort, risk tolerance, pace, or hiking style.]

### 17.7 Claim-Level Citation Standard

[Attach citations directly to consequential factual claims whenever practical, especially for safety, regulations, route status, transport, accommodation, water, navigation, permits, costs, and other information a hiker may act upon.]

### 17.8 Source Register

[Provide a consolidated source register containing each significant source's title or organization, link, source type, relevant report sections, publication, dataset, or update date when available, access date, and a short note explaining what information it supports. Include the significant weather datasets or stations, mobile coverage maps and reception evidence, and pronunciation references used.]

[Provide direct links to all significant sources used in the research, preferring the original or primary source rather than aggregators or secondary reproductions.]

### 17.9 Conflicts, Unknowns & Verification List

[Summarize unresolved source conflicts, low-confidence findings, missing information, assumptions, and facts that should be checked again before the trek.]

### 17.10 Research Freshness

[State when the report was researched and identify which sections should be refreshed shortly before departure because their information can materially change.]

---
