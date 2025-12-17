"""
Command-line interface for Turkiye API.

This module provides CLI commands for running the server and managing the application.
"""

import argparse
import os
import sys
from typing import Optional

import uvicorn
from dotenv import load_dotenv


def serve(host: Optional[str] = None, port: Optional[int] = None, reload: bool = False, workers: Optional[int] = None):
    """
    Start the Turkiye API server.

    Args:
        host: Host to bind to (default: from env or 0.0.0.0)
        port: Port to bind to (default: from env or 8181)
        reload: Enable auto-reload for development
        workers: Number of worker processes (production only)
    """
    load_dotenv()

    host = host or os.getenv("HOST", "0.0.0.0")
    port = port or int(os.getenv("PORT", 8181))

    print(f"🚀 Starting Turkiye API on {host}:{port}")
    print(f"📚 Documentation: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/docs")
    print(f"🔍 Health check: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/health")
    print()

    if workers and workers > 1:
        # Use Gunicorn for multi-worker production setup
        try:
            import multiprocessing

            from gunicorn.app.base import BaseApplication

            class StandaloneApplication(BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super().__init__()

                def load_config(self):
                    config = {
                        key: value
                        for key, value in self.options.items()
                        if key in self.cfg.settings and value is not None
                    }
                    for key, value in config.items():
                        self.cfg.set(key.lower(), value)

                def load(self):
                    return self.application

            options = {
                "bind": f"{host}:{port}",
                "workers": workers or (multiprocessing.cpu_count() * 2 + 1),
                "worker_class": "uvicorn.workers.UvicornWorker",
                "timeout": 30,
                "keepalive": 2,
            }

            from app.main import app

            StandaloneApplication(app, options).run()
        except ImportError:
            print("❌ Gunicorn not installed. Install with: pip install turkiye-api-py[server]")
            sys.exit(1)
    else:
        # Use Uvicorn for development or single-worker
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
        )


def version():
    """Display version information."""
    from app.settings import settings

    print(f"Turkiye API v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"Python: {sys.version.split()[0]}")


def info():
    """Display API information and statistics."""
    from app.services.data_loader import data_loader

    print("📊 Turkiye API Information")
    print("=" * 50)
    print(f"Provinces: {len(data_loader.provinces)}")
    print(f"Districts: {len(data_loader.districts)}")
    print(f"Neighborhoods: {len(data_loader.neighborhoods)}")
    print(f"Villages: {len(data_loader.villages)}")
    print(f"Towns: {len(data_loader.towns)}")
    print("=" * 50)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Turkiye API - Comprehensive REST API for Turkiye's administrative divisions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  turkiye-api serve                    Start development server
  turkiye-api serve --reload           Start with auto-reload
  turkiye-api serve --port 8000        Start on custom port
  turkiye-api serve --workers 4        Start with 4 workers (production)
  turkiye-api version                  Show version
  turkiye-api info                     Show API statistics
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the API server")
    serve_parser.add_argument("--host", type=str, help="Host to bind to (default: 0.0.0.0)")
    serve_parser.add_argument("--port", type=int, help="Port to bind to (default: 8181)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable auto-reload (development)")
    serve_parser.add_argument("--workers", type=int, help="Number of workers (production)")

    # Version command
    subparsers.add_parser("version", help="Show version information")

    # Info command
    subparsers.add_parser("info", help="Show API statistics")

    args = parser.parse_args()

    if args.command == "serve":
        serve(
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
        )
    elif args.command == "version":
        version()
    elif args.command == "info":
        info()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
