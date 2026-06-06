def generate_risk_narrative(
        risk,
        recommendations):

    narrative = f"""
EXECUTIVE RISK SUMMARY

Project:
{risk['project_id']}

Risk Score:
{risk['risk_score']}

Risk Level:
{risk['risk_level']}

Portfolio Analysis:

Project {risk['project_id']} is currently
classified as {risk['risk_level']}.

The project contains
{risk['dependencies']} dependency relationships,
{risk['resources']} assigned resources,
and {risk['critical_tasks']} critical path tasks.

This combination indicates elevated schedule
and delivery risk.

Recommended Actions:
"""

    for rec in recommendations:

        narrative += f"\n• {rec}"

    return narrative