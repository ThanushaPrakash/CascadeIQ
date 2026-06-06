from graph.mcp.mcp_server import mcp


def call_tool(
        tool_name,
        **kwargs):

    try:

        # ==========================
        # Risk Analysis
        # ==========================

        if tool_name == "risk":

            return mcp.risk_tool(
                kwargs["project_id"]
            )

        # ==========================
        # Monte Carlo
        # ==========================

        elif tool_name == "monte_carlo":

            return mcp.monte_carlo_tool(
                kwargs["project_id"]
            )

        # ==========================
        # Resource Analysis
        # ==========================

        elif tool_name == "resource":

            return mcp.resource_tool()

        # ==========================
        # Delay Propagation
        # ==========================

        elif tool_name == "delay":

            return mcp.delay_tool(

                kwargs["project_id"],

                kwargs["delay_days"]

            )

        else:

            return {

                "error":
                f"Unknown tool: {tool_name}"

            }

    except Exception as e:

        return {

            "error":
            str(e)

        }


# =====================================
# TESTING
# =====================================

if __name__ == "__main__":

    print("\n" + "=" * 50)
    print("MCP CLIENT TEST")
    print("=" * 50)

    # -------------------------
    # Risk Tool
    # -------------------------

    result = call_tool(

        "risk",

        project_id="P001"

    )

    print("\nRISK TOOL RESULT:\n")
    print(result)

    # -------------------------
    # Monte Carlo Tool
    # -------------------------

    result = call_tool(

        "monte_carlo",

        project_id="P001"

    )

    print("\nMONTE CARLO RESULT:\n")
    print({

        "average":
        result["average"],

        "p50":
        result["p50"],

        "p80":
        result["p80"],

        "p95":
        result["p95"]

    })

    # -------------------------
    # Resource Tool
    # -------------------------

    result = call_tool(
        "resource"
    )

    print("\nRESOURCE RESULT:\n")
    print(result[:3])

    # -------------------------
    # Delay Tool
    # -------------------------

    result = call_tool(

        "delay",

        project_id="P001",

        delay_days=20

    )

    print("\nDELAY RESULT:\n")
    print(result[:3])