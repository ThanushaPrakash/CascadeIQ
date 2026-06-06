import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )

from mcp.server.fastmcp import FastMCP

from graph.algorithms.risk_score import (
    calculate_risk
)

from graph.algorithms.monte_carlo import (
    monte_carlo_summary
)

from graph.algorithms.resource_analysis import (
    get_overloaded_resources
)

from graph.algorithms.delay_propagation import (
    propagate_delay
)

mcp = FastMCP(
    "CascadeIQ"
)


@mcp.tool()
def risk_tool(
        project_id: str):

    return calculate_risk(
        project_id
    )


@mcp.tool()
def monte_carlo_tool(
        project_id: str):

    return monte_carlo_summary(
        project_id
    )


@mcp.tool()
def resource_tool():

    return get_overloaded_resources()


@mcp.tool()
def delay_tool(
        project_id: str,
        delay_days: int):

    return propagate_delay(
        project_id,
        delay_days
    )


if __name__ == "__main__":

    mcp.run()