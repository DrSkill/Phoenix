def format_block(content, language=''):
    """Formats text into a code block."""
    return f'```{language}\n{content}\n```'


def indented_entry_to_str(entries, indent=0, sep=' '):
    """Pretty formatting."""
    # Get the longest keys' width
    width = max([len(t[0]) for t in entries])

    output = []
    for name, entry in entries:
        if indent > 0:
            output.append(f'{"":{indent}}{name:{width}}{sep}{entry}')
        else:
            output.append(f'{name:{width}}{sep}{entry}')

    return '\n'.join(output)
