# Source Strategy — European Travel Vaccination Assessment

Use this file for source discovery and validation. Websites, national policies, and vaccine recommendations change, so verify the current material at execution time.

## 1. Source hierarchy

Use the most specific authoritative source that answers the question.

### Tier 1 — Destination national or regional public-health authority

Use the destination country's ministry of health, national public-health institute, vaccination authority, or regional authority for:

- local disease surveillance;
- outbreak notices;
- official endemic/risk areas;
- resident vaccination programmes that help establish local epidemiology;
- local traveler advice when published;
- local vaccine schedules and contraindication guidance.

Examples include:

- Germany — Robert Koch Institute (RKI) / STIKO
- France — Santé publique France and Ministry of Health
- Italy — Istituto Superiore di Sanità (ISS/EpiCentro), Ministry of Health, and relevant regional health authorities
- Slovenia — National Institute of Public Health (NIJZ)
- Austria — Ministry of Health / official Austrian vaccination plan and AGES
- Switzerland — Federal Office of Public Health (BAG/FOPH)
- Sweden — Folkhälsomyndigheten
- Finland — Finnish Institute for Health and Welfare (THL)
- Norway — Norwegian Institute of Public Health (FHI)
- Greece — National Public Health Organization (EODY)
- Croatia — Croatian Institute of Public Health (HZJZ)
- Romania — National Institute of Public Health and Ministry of Health
- Poland — National Institute of Public Health / Chief Sanitary Inspectorate as applicable
- Czechia — State Health Institute (SZÚ) / Ministry of Health
- Slovakia — Public Health Authority of the Slovak Republic
- United Kingdom — UK Health Security Agency (UKHSA) and NaTHNaC/TravelHealthPro

This is a discovery list, not a whitelist. For any country, identify its current equivalent.

### Tier 2 — ECDC

Use ECDC for EU/EEA-wide surveillance, outbreak context, and comparison between national vaccination schedules.

Useful starting points:

- Vaccine Scheduler: https://vaccine-schedule.ecdc.europa.eu/
- ECDC infectious disease topics and surveillance: https://www.ecdc.europa.eu/en

The ECDC Vaccine Scheduler is built from data reported by EU/EEA Member States, but ECDC itself advises consulting national sources for the most up-to-date details and nuances.

For focal diseases such as TBE, use disease-specific surveillance and locally acquired case maps rather than only national schedule tables.

### Tier 3 — Traveler-specific national guidance

Use a recognized public travel-health authority when destination authorities do not directly translate epidemiology into traveler recommendations.

Preferred European examples:

- UK NaTHNaC / TravelHealthPro country pages: https://travelhealthpro.org.uk/countries
- Germany STIKO + German Society for Tropical Medicine, Travel Medicine and Global Health (DTG) travel-vaccination recommendations, published via RKI. For 2026 the recommendations were published in July 2026; always retrieve the newest edition at execution time.
- NHS Scotland Fit for Travel where current and applicable: https://www.fitfortravel.nhs.uk/

TravelHealthPro is particularly useful because its country pages separate vaccines recommended for most travelers from those for selected travelers and describe the rationale for hepatitis A, hepatitis B, rabies, TBE, typhoid, and other recommendations.

Do not allow one foreign country's administrative or reimbursement policy to substitute for the destination's epidemiology.

### Tier 4 — WHO

Use WHO for:

- International Travel and Health guidance;
- vaccine-preventable disease background and traveler risk;
- International Health Regulations (IHR) context;
- polio temporary recommendations where applicable;
- yellow fever certificate rules and country requirements when applicable.

Current starting point:

- WHO International Travel and Health, Module 4: Vaccine-preventable diseases and vaccines (published 6 September 2025): https://www.who.int/publications/i/item/9789240113350

Always verify whether a newer WHO module or country requirement list exists.

### Tier 5 — Product information / medicines regulator

Use official Summary of Product Characteristics (SmPC), EMA/national medicines regulator material, or other official product information for:

- approved age ranges;
- dose intervals;
- accelerated schedules;
- contraindications;
- timing details not clearly stated in public-health guidance.

Do not use commercial clinic marketing copy as the authority for a dosing schedule when official product information is available.

### Tier 6 — Peer-reviewed research

Use recent peer-reviewed studies when official sources leave a meaningful evidence gap, for example:

- emerging TBE foci;
- fine-scale rabies epidemiology;
- outbreak reconstruction;
- vaccine effectiveness in special settings;
- seroprevalence or vector infection data.

Do not let a small study override newer official surveillance without explaining the discrepancy.

### Tier 7 — Secondary sources

Hospital travel clinics, private clinics, tourism sites, hiking sites, Wikipedia, blogs, forums, and news articles may help locate routes or identify a question to verify. They should not determine the final vaccine recommendation when authoritative sources exist.

## 2. Search strategy

For each destination, search both English and the local language where useful.

Useful patterns:

- `[country] travel vaccination recommendations official 2026`
- `[country] [disease] vaccination travelers official`
- `[region] [disease] cases 2025 2026 public health`
- `site:[official-domain] travel vaccine [disease]`
- `site:[official-domain] [local-language disease term] [region]`
- `site:travelhealthpro.org.uk [country] vaccine`
- `site:ecdc.europa.eu [disease] [country] 2026`
- `site:who.int [country] polio travel vaccination requirements`

For route-based trips, first resolve the administrative regions crossed, then search those names rather than only the country.

## 3. What to extract from a traveler-guidance source

Record:

- authority;
- page/report title;
- publication/update date;
- country/region covered;
- whether guidance is for residents, travelers, or both;
- vaccine recommendation wording exactly at the policy level: recommended / consider / selected travelers / not routinely recommended;
- exposure conditions attached to the recommendation;
- relevant schedule or booster guidance;
- caveats and contraindication referrals;
- administrative certificate requirements, if any.

## 4. What to extract from surveillance/outbreak sources

Record:

- disease;
- surveillance authority;
- publication/update date;
- geographic resolution;
- locally acquired versus imported cases;
- time period;
- incidence/case counts when available;
- outbreak status;
- official risk-area classification;
- important reporting limitations.

Do not convert population incidence directly into a traveler's personal infection probability.

## 5. Freshness rules

- Prefer current-year traveler guidance and current national vaccination recommendations.
- Check current outbreaks even if the base country page is older.
- For stable routine schedules, use the newest national/ECDC schedule available.
- For TBE, rabies, measles, polio, hepatitis A outbreaks, and other changing risks, seek current or recent surveillance rather than relying only on evergreen disease pages.
- If local epidemiology is more than 3 years old and no current authority confirms it, lower confidence.
- Note publication date separately from the time period described by the data.

## 6. How to use TravelHealthPro carefully

NaTHNaC/TravelHealthPro is a high-value traveler-oriented cross-check, especially where national sources do not provide visitor-specific wording.

Its country methodology considers, among other factors:

- hepatitis A endemicity/incidence/outbreak evidence;
- hepatitis B population prevalence;
- rabies animal risk and access to post-exposure care;
- TBE human/animal cases, serology, virus detection, national surveillance, vaccination programmes, habitat, and proximity to known foci.

Use the current country page and disease page. Preserve the distinction between “most travellers” and “some travellers.”

## 7. Administrative requirements

Check these independently from medical risk:

- yellow fever certificate rules based on country of origin/transit;
- temporary polio certificate rules under WHO/IHR;
- vaccination requirements for work, education, healthcare placements, mass gatherings, or visas;
- current destination-specific COVID or other border requirements if any.

The traveler may be medically advised to vaccinate without a border requirement, or required to document vaccination despite low disease risk during the trip. Do not merge the two.

## 8. Minimum evidence standard

For a confident destination-specific recommendation, aim for:

1. one current national/regional official source for local epidemiology or policy; and
2. one independent traveler-oriented or European cross-check such as TravelHealthPro, ECDC, WHO, or current STIKO/DTG guidance.

For a focal disease or active outbreak, add a current surveillance/outbreak source for the exact region whenever possible.

If this cannot be achieved, continue with the best available evidence but label confidence as medium or low and explain why.
