"""
Main Application Entry Point
------------------------------
This is where the app starts

For Viva:
- Starlette: Web framework (handles HTTP requests)
- GraphQLApp: Connects GraphQL to web framework
- Uvicorn: Server that runs the app
"""

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette_graphene3 import GraphQLApp
from queries.root import schema
from database import init_db, db_session
import uvicorn


# Initialize database (create tables if they don't exist)
init_db()


# Self-contained GraphiQL HTML page (loads from CDN - no blank page issue)
def graphiql_html(request: Request):
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GraphiQL - Smart Electricity Billing</title>
    <link rel="stylesheet" href="https://unpkg.com/graphiql@3.0.9/graphiql.min.css" />
</head>
<body style="margin: 0;">
    <div id="graphiql" style="height: 100vh;"></div>

    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/graphiql@3.0.9/graphiql.min.js"></script>

    <script>
        const fetcher = GraphiQL.createFetcher({
            url: '/graphql',
        });

        const root = ReactDOM.createRoot(document.getElementById('graphiql'));
        root.render(
            React.createElement(GraphiQL, {
                fetcher: fetcher,
                defaultEditorToolsVisibility: true,
            })
        );
    </script>
</body>
</html>
""")


# Create Starlette app
app = Starlette(
    debug=True,  # Enable debug mode (shows detailed errors)
    routes=[
        # GraphiQL UI - opens in browser
        Route("/graphql", graphiql_html, methods=["GET"]),
        # GraphQL API endpoint - handles actual queries/mutations
        Route("/graphql", GraphQLApp(schema=schema), methods=["POST"]),
    ],
)


# Cleanup: Close database session after each request
@app.on_event("shutdown")
def shutdown_event():
    db_session.remove()


# For Viva: Explain this
# When you run: python main.py
# This starts the server on http://localhost:8000
if __name__ == "__main__":
    print("🚀 Starting Smart Electricity Billing System")
    print("📊 GraphiQL UI: http://localhost:8000/graphql")
    print("\n💡 To test in Postman/Thunder Client:")
    print("   POST http://localhost:8000/graphql")
    print("   Body: { \"query\": \"your graphql query here\" }\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,
        reload=True  # Auto-reload when code changes (useful during development)
    )
