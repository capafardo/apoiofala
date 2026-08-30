"""
Script para geração e garantia de ícones/pictogramas SVG vetoriais offline do CAA-Lab.
"""

import os
from pathlib import Path

PICTOGRAMS = {
    "eu.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="30" r="16" fill="#3b82f6"/>
  <circle cx="50" cy="28" r="12" fill="#ffd1a4"/>
  <path d="M42 22 Q50 16 58 22" stroke="#2c3e50" stroke-width="4" fill="none"/>
  <circle cx="46" cy="27" r="1.5" fill="#2c3e50"/>
  <circle cx="54" cy="27" r="1.5" fill="#2c3e50"/>
  <path d="M47 33 Q50 36 53 33" stroke="#2c3e50" stroke-width="1.5" fill="none"/>
  <path d="M30 75 C30 52 70 52 70 75 Z" fill="#2563eb"/>
  <path d="M46 56 L38 68" stroke="#ffd1a4" stroke-width="5" stroke-linecap="round"/>
  <circle cx="38" cy="68" r="4" fill="#ffd1a4"/>
</svg>""",

    "quero.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 82 C20 62 10 44 10 28 C10 14 22 8 34 8 C42 8 47 13 50 18 C53 13 58 8 66 8 C78 8 90 14 90 28 C90 44 80 62 50 82 Z" fill="#ef4444" stroke="#b91c1c" stroke-width="3"/>
</svg>""",

    "beber.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 25 L38 85 C38 88 42 90 50 90 C58 90 62 88 62 85 L70 25 Z" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
  <path d="M34 50 L66 50 L63 80 C63 82 58 84 50 84 C42 84 37 82 37 80 Z" fill="#38bdf8"/>
  <path d="M52 10 L48 40 L60 8" stroke="#f59e0b" stroke-width="4" stroke-linecap="round" fill="none"/>
  <ellipse cx="50" cy="25" rx="20" ry="4" fill="none" stroke="#0284c7" stroke-width="2"/>
</svg>""",

    "banheiro.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="25" y="15" width="50" height="35" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="3"/>
  <ellipse cx="50" cy="55" rx="22" ry="12" fill="#e2e8f0" stroke="#64748b" stroke-width="3"/>
  <path d="M35 58 C35 78 65 78 65 58 Z" fill="#f8fafc" stroke="#64748b" stroke-width="3"/>
  <path d="M40 76 L36 90 L64 90 L60 76 Z" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
</svg>""",

    "gosto.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M35 50 L35 85 L20 85 L20 50 Z" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
  <path d="M35 50 C35 38 42 20 50 15 C56 12 60 16 58 25 L55 38 L80 38 C86 38 88 44 86 48 L78 80 C76 85 70 85 64 85 L35 85 Z" fill="#fcd34d" stroke="#d97706" stroke-width="3"/>
</svg>""",

    "comer.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 35 C40 20 20 25 20 48 C20 75 45 88 50 88 C55 88 80 75 80 48 C80 25 60 20 50 35 Z" fill="#ef4444" stroke="#991b1b" stroke-width="3"/>
  <path d="M50 35 Q50 15 62 12" stroke="#78350f" stroke-width="4" fill="none" stroke-linecap="round"/>
  <ellipse cx="64" cy="18" rx="8" ry="4" fill="#22c55e" transform="rotate(-30 64 18)"/>
</svg>""",

    "ir.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M15 40 L55 40 L55 20 L88 50 L55 80 L55 60 L15 60 Z" fill="#0284c7" stroke="#0369a1" stroke-width="3"/>
</svg>""",

    "nao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <line x1="20" y1="20" x2="80" y2="80" stroke="#dc2626" stroke-width="14" stroke-linecap="round"/>
  <line x1="80" y1="20" x2="20" y2="80" stroke="#dc2626" stroke-width="14" stroke-linecap="round"/>
</svg>""",

    "ajuda.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M22 65 C22 55 30 45 42 40 L52 48 L44 68 Z" fill="#fcd34d" stroke="#d97706" stroke-width="2"/>
  <path d="M78 65 C78 55 70 45 58 40 L48 48 L56 68 Z" fill="#fcd34d" stroke="#d97706" stroke-width="2"/>
  <circle cx="50" cy="30" r="10" fill="#ef4444"/>
  <line x1="45" y1="30" x2="55" y2="30" stroke="#ffffff" stroke-width="3"/>
  <line x1="50" y1="25" x2="50" y2="35" stroke="#ffffff" stroke-width="3"/>
</svg>""",

    "mais.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="42" y="15" width="16" height="70" rx="6" fill="#8b5cf6"/>
  <rect x="15" y="42" width="70" height="16" rx="6" fill="#8b5cf6"/>
</svg>""",

    "mae.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 50 C25 20 75 20 75 50 C75 75 68 85 50 85 C32 85 25 75 25 50 Z" fill="#475569"/>
  <circle cx="50" cy="48" r="22" fill="#ffd1a4"/>
  <circle cx="43" cy="45" r="2" fill="#1e293b"/>
  <circle cx="57" cy="45" r="2" fill="#1e293b"/>
  <path d="M45 56 Q50 60 55 56" stroke="#e11d48" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M30 85 C30 75 70 75 70 85 Z" fill="#ec4899"/>
</svg>""",

    "pai.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M28 35 C28 15 72 15 72 35 L72 45 C65 35 35 35 28 45 Z" fill="#1e293b"/>
  <circle cx="50" cy="48" r="22" fill="#ffd1a4"/>
  <circle cx="43" cy="45" r="2" fill="#1e293b"/>
  <circle cx="57" cy="45" r="2" fill="#1e293b"/>
  <path d="M45 56 Q50 60 55 56" stroke="#2c3e50" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M30 85 C30 72 70 72 70 85 Z" fill="#3b82f6"/>
</svg>""",

    "casa.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 15 L15 45 L25 45 L25 85 L75 85 L75 45 L85 45 Z" fill="#fbbf24" stroke="#b45309" stroke-width="3"/>
  <path d="M50 12 L10 46 L90 46 Z" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>
  <rect x="42" y="55" width="16" height="30" fill="#78350f"/>
  <circle cx="54" cy="70" r="1.5" fill="#fef08a"/>
</svg>""",

    "escola.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="40" width="60" height="45" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>
  <path d="M50 15 L15 42 L85 42 Z" fill="#475569" stroke="#1e293b" stroke-width="2"/>
  <circle cx="50" cy="30" r="6" fill="#fbbf24" stroke="#b45309" stroke-width="1.5"/>
  <rect x="42" y="60" width="16" height="25" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
  <rect x="26" y="50" width="10" height="10" fill="#bae6fd"/>
  <rect x="64" y="50" width="10" height="10" fill="#bae6fd"/>
</svg>""",

    "brincar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="38" fill="#f8fafc" stroke="#0f172a" stroke-width="3"/>
  <path d="M50 12 A38 38 0 0 1 88 50 L50 50 Z" fill="#ef4444"/>
  <path d="M88 50 A38 38 0 0 1 50 88 L50 50 Z" fill="#3b82f6"/>
  <path d="M50 88 A38 38 0 0 1 12 50 L50 50 Z" fill="#eab308"/>
  <path d="M12 50 A38 38 0 0 1 50 12 L50 50 Z" fill="#10b981"/>
  <circle cx="50" cy="50" r="8" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
</svg>""",

    "agua.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 20 L36 85 C36 88 42 90 50 90 C58 90 64 88 64 85 L70 20 Z" fill="#bae6fd" stroke="#0284c7" stroke-width="3"/>
  <path d="M34 45 C42 42 48 48 56 45 C60 43 64 45 66 45 L63 85 C63 87 58 88 50 88 C42 88 37 87 37 85 Z" fill="#38bdf8"/>
</svg>""",

    "suco.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 20 L36 85 C36 88 42 90 50 90 C58 90 64 88 64 85 L70 20 Z" fill="#ffedd5" stroke="#ea580c" stroke-width="3"/>
  <path d="M34 45 L66 45 L63 85 C63 87 58 88 50 88 C42 88 37 87 37 85 Z" fill="#f97316"/>
  <path d="M52 10 L48 40 L60 8" stroke="#16a34a" stroke-width="4" stroke-linecap="round" fill="none"/>
</svg>""",

    "leite.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="30" y="35" width="40" height="55" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="3"/>
  <path d="M30 35 L40 18 L60 18 L70 35 Z" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
  <rect x="30" y="50" width="40" height="20" fill="#38bdf8"/>
  <text x="50" y="65" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">LEITE</text>
</svg>""",

    "pao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M15 55 C15 35 35 25 60 25 C75 25 88 35 88 50 C88 65 75 75 55 75 C30 75 15 70 15 55 Z" fill="#f59e0b" stroke="#b45309" stroke-width="3"/>
  <path d="M30 40 Q40 50 45 60" stroke="#78350f" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M50 35 Q60 45 65 55" stroke="#78350f" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M70 38 Q78 48 80 55" stroke="#78350f" stroke-width="3" stroke-linecap="round" fill="none"/>
</svg>""",

    "arroz.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 50 C20 75 80 75 80 50 Z" fill="#f1f5f9" stroke="#64748b" stroke-width="3"/>
  <path d="M20 50 C20 38 40 30 50 30 C60 30 80 38 80 50 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <ellipse cx="45" cy="40" rx="3" ry="1.5" fill="#94a3b8"/>
  <ellipse cx="55" cy="42" rx="3" ry="1.5" fill="#94a3b8"/>
  <ellipse cx="50" cy="46" rx="3" ry="1.5" fill="#94a3b8"/>
</svg>""",

    "feijao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 50 C20 75 80 75 80 50 Z" fill="#78350f" stroke="#451a03" stroke-width="3"/>
  <path d="M20 50 C20 38 40 30 50 30 C60 30 80 38 80 50 Z" fill="#92400e" stroke="#451a03" stroke-width="2"/>
  <ellipse cx="40" cy="42" rx="4" ry="2.5" fill="#451a03"/>
  <ellipse cx="52" cy="38" rx="4" ry="2.5" fill="#451a03"/>
  <ellipse cx="62" cy="44" rx="4" ry="2.5" fill="#451a03"/>
</svg>""",

    "carne.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 45 C15 30 35 15 55 25 C75 35 85 55 75 70 C65 85 35 85 25 70 C18 60 18 50 25 45 Z" fill="#ef4444" stroke="#991b1b" stroke-width="3"/>
  <ellipse cx="42" cy="48" rx="8" ry="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
</svg>""",

    "fruta.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 70 C20 50 35 25 55 35 C70 45 50 80 30 80 C26 80 25 75 25 70 Z" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
  <path d="M35 75 C55 80 80 65 85 40 C86 35 82 35 80 38 C75 55 55 68 35 68 Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
  <path d="M50 35 Q52 20 60 18" stroke="#15803d" stroke-width="3" stroke-linecap="round" fill="none"/>
</svg>""",

    "feliz.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="38" fill="#fef08a" stroke="#ca8a04" stroke-width="3"/>
  <circle cx="38" cy="42" r="4" fill="#854d0e"/>
  <circle cx="62" cy="42" r="4" fill="#854d0e"/>
  <path d="M34 56 Q50 74 66 56" stroke="#854d0e" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>""",

    "triste.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="38" fill="#bae6fd" stroke="#0284c7" stroke-width="3"/>
  <circle cx="38" cy="44" r="4" fill="#0369a1"/>
  <circle cx="62" cy="44" r="4" fill="#0369a1"/>
  <path d="M34 66 Q50 50 66 66" stroke="#0369a1" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>""",
}


def ensure_pictograms(base_dir: Path = None):
    """Cria os arquivos SVG nas pastas static e assets."""
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent

    target_dirs = [
        base_dir / "app" / "static" / "pictograms",
        base_dir / "assets" / "pictograms",
    ]

    for t_dir in target_dirs:
        os.makedirs(t_dir, exist_ok=True)
        for filename, svg_content in PICTOGRAMS.items():
            file_path = t_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(svg_content.strip())


if __name__ == "__main__":
    ensure_pictograms()
    print(f"Gerados {len(PICTOGRAMS)} pictogramas com sucesso.")
