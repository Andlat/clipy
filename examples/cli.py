import clipy


@clipy.App(usage="mypackage <command> [options] [arg] ...", description="Example CLI app")
@clipy.Option("verbose", help="Example of global option")
@clipy.Command(
    "list",
    usage="mypackage list [options]",
    description="List all items",
    options=[
        clipy.Option("long", help="Use the long listing format"),
        clipy.Option("all", help="List all items, including hidden files", action="store_true"),
    ],
)
@clipy.Command(
    "show",
    usage="mypackage show [options] <item>",
    description="Show details about an item",
    options=[clipy.Option("json", help="Output the item details in JSON format")],
)
def main(command: clipy.CommandDefinition):
    # For demonstration, just print the command name and the parsed options.
    print(f"Command: {command.name}")
    print("Options:")
    for key, value in command.options.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
