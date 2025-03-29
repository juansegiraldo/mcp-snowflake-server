import click
from .server import SnowflakeMCPServer

@click.command()
@click.option('--account', required=True, help='Snowflake account identifier')
@click.option('--warehouse', required=True, help='Snowflake warehouse name')
@click.option('--user', required=True, help='Snowflake username')
@click.option('--password', required=True, help='Snowflake password')
@click.option('--role', required=True, help='Snowflake role')
@click.option('--database', required=True, help='Snowflake database name')
@click.option('--schema', required=True, help='Snowflake schema name')
@click.option('--port', default=8080, help='Port to run the server on')
def main(account, warehouse, user, password, role, database, schema, port):
    """Start the Snowflake MCP server"""
    server = SnowflakeMCPServer(
        account=account,
        warehouse=warehouse,
        user=user,
        password=password,
        role=role,
        database=database,
        schema=schema
    )
    server.run(port=port)

if __name__ == '__main__':
    main()