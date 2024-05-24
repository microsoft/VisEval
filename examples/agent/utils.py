def show_svg(plt, svg_name: str):
    """Show a plot as a SVG inline."""
    from io import StringIO

    f = StringIO()
    plt.savefig(f, format="svg")
    if svg_name:
        plt.savefig(f"{svg_name}")
    plt.close()

    return f.getvalue()
