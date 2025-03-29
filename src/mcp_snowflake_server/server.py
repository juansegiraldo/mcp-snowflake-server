import snowflake.connector
from mcp_core import MCPServer, Resource, Tool
from typing import Dict, List, Any

class SnowflakeMCPServer(MCPServer):
    def __init__(self, account: str, warehouse: str, user: str, password: str,
                 role: str, database: str, schema: str):
        super().__init__()
        self.conn = snowflake.connector.connect(
            account=account,
            warehouse=warehouse,
            user=user,
            password=password,
            role=role,
            database=database,
            schema=schema
        )
        self.cursor = self.conn.cursor()
        self._setup_tools()
        self._setup_resources()

    def _setup_tools(self):
        @self.tool('read_query')
        def read_query(query: str) -> List[Dict[str, Any]]:
            """Execute a SELECT query to read data from Snowflake"""
            self.cursor.execute(query)
            columns = [col[0] for col in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

        @self.tool('write_query')
        def write_query(query: str) -> Dict[str, int]:
            """Execute an INSERT, UPDATE, or DELETE query in Snowflake"""
            self.cursor.execute(query)
            return {'affected_rows': self.cursor.rowcount}

        @self.tool('list_tables')
        def list_tables() -> List[str]:
            """Get a list of all tables in the current schema"""
            self.cursor.execute('SHOW TABLES')
            return [row[1] for row in self.cursor.fetchall()]

        @self.tool('describe_table')
        def describe_table(table_name: str) -> List[Dict[str, str]]:
            """Get column information for a specific table"""
            self.cursor.execute(f'DESCRIBE TABLE {table_name}')
            return [{
                'name': row[0],
                'type': row[1],
                'nullable': row[3] == 'Y'
            } for row in self.cursor.fetchall()]

    def _setup_resources(self):
        self.insights = []

        @self.resource('memo://insights')
        def get_insights() -> List[str]:
            return self.insights

        @self.tool('append_insight')
        def append_insight(insight: str):
            """Add a new insight to the memo resource"""
            self.insights.append(insight)
            self.notify_resource_update('memo://insights')
            return {'status': 'success'}

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()