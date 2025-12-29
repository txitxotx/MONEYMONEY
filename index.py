from app import app

# Vercel necesita el objeto server, NO app
server = app.server
