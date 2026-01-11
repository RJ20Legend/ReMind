"""Small helper to build embeddings into a store (placeholder)."""
from pathlib import Path

def build():
    out = Path(__file__).parent / 'embeddings_store'
    out.mkdir(exist_ok=True)
    (out / 'README.txt').write_text('Place for vector store files')

if __name__ == '__main__':
    build()
