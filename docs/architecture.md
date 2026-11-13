# Architecture and research map

The target segment stays visible beside the five work stages. Each stage creates a reviewable artifact before the next stage.

```mermaid
flowchart TD
    root(("Team 03 · Swvl GTM research"))
    segment["TARGET SEGMENT · Greater Cairo outsourced contact centers with employer-arranged late-shift rides"] --- root
    root --> define["1 · Define the task"]
    root --> validate["2 · Validate the segment"]
    root --> icp["3 · Build the ICP"]
    root --> offer["4 · Build the offer"]
    root --> score["5 · Score and hand off"]
    define --> inputs["Brief, rubric and evidence rules"]
    validate --> accounts["15–20 companies, local buyer routes, demand and Swvl delivery"]
    icp --> buying["Alternatives, buying committee and triggers"]
    offer --> stack["Value levers, obstacles and four-rung ladder"]
    score --> review["25 accounts, strict evaluations and team PR"]
```

## Tool handoffs and gates

```mermaid
flowchart TD
    saved["Brief and reusable evidence"] --> plan["Preflight and cost reservations"]
    plan --> clay["Clay · Company discovery"]
    clay --> web["Primary-source verification"]
    web --> missing{"Missing evidence?"}
    missing -->|Current local buyer| crust["Crustdata · Narrow indexed people search"]
    missing -->|Specific inaccessible source| treg["treg · Catalog, price and targeted retrieval"]
    missing -->|No| gate{"Segment acceptance"}
    crust --> gate
    treg --> gate
    gate -->|Insufficient| gaps["Evidence gaps and bounded repair"]
    gaps --> web
    gate -->|Supported for discovery| docs["ICP, offer and value ladder"]
    docs --> scores["Score and route 25 buying units"]
    scores --> machine["Offline deterministic checks"]
    machine --> human["Independent source and commercial review"]
    human -->|Pass| pr["Versioned team handoff"]
    human -->|Revise| gaps
```

REPLAY bypasses all external retrieval and uses the saved evidence snapshot. PREVIEW exercises the same gates on three accounts. FULL targets 25. REFRESH reopens only evidence that is stale, missing or contradicted.

Source observations flow into `run.json`. The scorecard is rendered from that file. Narrative files cite the same registry, and the evaluation report states which claims remain uncertain. Drive is an optional export destination after review.
