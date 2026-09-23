def check_tool_call(messages, expected_tool) -> bool:
    called_tools = set()
    for m in messages:
        tool_calls = getattr(m, "tool_calls", None)
        if tool_calls:
            called_tools.update(c["name"] for c in tool_calls)

    if expected_tool is None:
        return len(called_tools) == 0
    return expected_tool in called_tools