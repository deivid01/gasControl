#!/bin/bash
echo "Building Project for Vercel..."

# Install Backend Deps
echo "Installing Django Deps..."
pip install -r backend/requirements.txt

# Run migrations (Optional but good practice if not done manually)
echo "Running Migrations..."
python backend/manage.py migrate

# Build Frontend
echo "Building Vue Frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Build Completed!"
