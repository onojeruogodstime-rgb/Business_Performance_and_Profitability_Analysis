# The Domino Effect: NHS Waiting Lists, Workforce Pressure and Patient Outcomes

**Project type:** Systems analysis and system-dynamics modelling  
**Domain:** Healthcare operations · workforce planning · feedback systems  
**Tools:** Rich Picture · CATWOE/SSM · Iceberg Model · Causal Loop Diagrams · Vensim PLE

[← Portfolio index](../../PORTFOLIO_INDEX.md)

## Executive summary

This project frames NHS waiting lists as an emergent outcome of interacting demand, workforce, capacity, policy and patient-flow mechanisms rather than as a problem that can be solved by increasing activity alone. The supplied manuscript combines Soft Systems Methodology (SSM) tools with causal-loop analysis and a stock-and-flow model in Vensim.

Its central hypothesis is that reinforcing pressures—particularly staff burnout, reduced productivity, delayed treatment and patient deterioration—can amplify backlogs faster than slower balancing mechanisms such as funding and recruitment can relieve them. The work uses scenario and sensitivity analysis to examine assumptions and identify candidate intervention points.

**Evidence boundary:** the qualitative framework and model interpretation are documented in the supplied manuscript. This repository does not yet contain a clean, independently runnable model file and its outputs, and the model is not presented as a calibrated or policy-validated representation of the NHS.

## Problem framing

Waiting-list size is a stock shaped by the balance between inflows (referrals and other additions) and outflows (completed treatment and other removals). The system is affected by multiple stakeholders and delayed responses. A narrow focus on backlog size may overlook the mechanisms that reproduce the backlog.

## Feedback structures

### Reinforcing loop: workforce pressure

Waiting-list pressure → workload and staff burnout → lower productivity → reduced treatment throughput → longer waiting lists.

This loop can amplify the original pressure. Interventions focused only on adding short-term activity may not interrupt the mechanisms that reduce effective capacity over time.

### Balancing loop: capacity response

Waiting-list pressure → policy attention → funding → recruitment and workforce capacity → treatment throughput → reduced waiting-list pressure.

This loop is constrained by decision, funding, recruitment and implementation delays. Funding does not automatically translate into immediate effective clinical capacity.

### Connected system effects

The manuscript also considers patient deterioration, emergency-demand displacement, diagnostic delays, discharge constraints, bed occupancy and referral behaviour. These interactions suggest that local improvements can shift bottlenecks elsewhere in the patient pathway.

## Analytical approach

1. **Rich Picture and stakeholder framing:** describe the situation and competing perspectives.
2. **CATWOE / Soft Systems Methodology:** define the transformation, actors and wider environment.
3. **Iceberg analysis:** distinguish visible events and patterns from structural drivers and mental models.
4. **Causal Loop Diagram:** identify reinforcing and balancing feedback.
5. **Stock-and-flow model:** formalise selected relationships, stocks, flows and delays in Vensim PLE.
6. **Scenario and sensitivity analysis:** examine how outcomes change under alternative assumptions.
7. **Theory of Constraints check:** identify the limiting throughput mechanism before proposing interventions.

## Candidate leverage points

| Leverage point | Why it matters | Example direction |
|---|---|---|
| Workforce wellbeing and retention | Retention protects experienced capacity and may reduce the burnout spiral | Improve retention, wellbeing and workload design |
| Diagnostic throughput | Delays can block downstream appointments and treatment | Improve diagnostic capacity and pathway coordination |
| Discharge and social-care interface | Delayed discharge can constrain beds and elective throughput | Strengthen discharge coordination and integrated care |
| Recruitment and capacity planning | Funding has delayed effects and must translate into deployable staff | Model recruitment lead times and effective capacity |
| Preventive and integrated care | May reduce future pressure on acute services | Test longer-horizon pathway scenarios |

These are candidate leverage points from the systems analysis, not proven causal effects or quantified policy recommendations.

## Model assumptions and validation

The manuscript explicitly recognises that passing qualitative plausibility checks is **not equivalent to formal statistical validation**. Before using the model for decision support, a stronger technical release should include:

- the Vensim model file and complete variable/equation dictionary;
- units, initial values, parameter sources and a clear separation of measured values from illustrative assumptions;
- dimensional-consistency checks and extreme-condition tests;
- reproduction of baseline, scenario and sensitivity charts from the model file;
- sensitivity analysis across plausible parameter ranges;
- comparison with independent NHS time-series or operational evidence where appropriate.

Numerical constants should not be represented as measured NHS parameters unless their sources and calibration are documented.

## Professional and academic integrity

The underlying manuscript was prepared in an academic context. Before publishing any diagrams, text, simulation outputs or assessment artefacts, check the University's rules and any supervisor or publisher requirements. This page is a portfolio summary; it does not reproduce the full manuscript or claim publication status.

## Status

**Status: systems framework documented; model package and quantitative results require a reproducibility pass.**

See [the portfolio index](../../PORTFOLIO_INDEX.md).
